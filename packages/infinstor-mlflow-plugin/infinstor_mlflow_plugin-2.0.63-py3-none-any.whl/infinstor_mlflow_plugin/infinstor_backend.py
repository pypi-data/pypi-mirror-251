import json
import yaml
import os
import logging
import posixpath
import docker
from os.path import expanduser
from os.path import sep as separator
import requests
from requests.exceptions import HTTPError
from urllib.parse import urlparse
import configparser
import base64
import urllib
import uuid

from mlflow.projects.backend.abstract_backend import AbstractBackend
import mlflow.tracking as tracking
from mlflow.entities import RunStatus
from mlflow.projects.submitted_run import SubmittedRun
from mlflow.projects.utils import (
    fetch_and_validate_project,
    get_or_create_run,
    load_project,
    get_entry_point_command,
    get_run_env_vars,
    MLFLOW_DOCKER_WORKDIR_PATH
)
import mlflow.projects
import mlflow.projects.docker
from mlflow.utils import process, file_utils
from mlflow.utils.mlflow_tags import (
        MLFLOW_PROJECT_ENV,
        MLFLOW_PROJECT_BACKEND,
        MLFLOW_DOCKER_IMAGE_URI,
        MLFLOW_DOCKER_IMAGE_ID
)
import mlflow.projects.kubernetes
from mlflow.projects.kubernetes import KubernetesSubmittedRun, _get_run_command, _load_kube_context
import kubernetes
from kubernetes.config.config_exception import ConfigException
from infinstor_mlflow_plugin.cognito_auth_rest_store import CognitoAuthenticatedRestStore
from infinstor_mlflow_plugin import tokenfile
import kubernetes
from kubernetes.config.config_exception import ConfigException

from .utils import _validate_infin_mlflow_tracking_uri_exit, _get_logger
_logger:logging.Logger = _get_logger(__name__)

verbose = True

def _get_git_commit(path):
    try:
        import git
    except ImportError as e:
        _logger.warning(
            "Failed to import Git (the Git executable is probably not on your PATH),"
            " so Git SHA is not available. Error: %s",
            e,
        )
        return None
    try:
        if os.path.isfile(path):
            path = os.path.dirname(path)
        repo = git.Repo(path, search_parent_directories=True)
        commit = repo.head.commit.hexsha
        return commit
    except (git.InvalidGitRepositoryError, git.GitCommandNotFound, ValueError, git.NoSuchPathError):
        return None

'''
For running in k8s, invoke as 'mlflow run . -b infinstor-backend --backend-config kubernetes_config.json'
kubernetes_config.json contains:
{
    "backend-type": "singlevm|eks",
    "kube-context": "minikube",
    "kube-job-template-path": "kubernetes_job_template.yaml",
    "kube-client-location": "local|backend",
    "repository-uri": "public.ecr.aws/l9n7x1v8/mlflow-projects-demo/full-image",
    "kube-namespace": "default",
    "resources.limits.cpu": "500m",
    "resources.limits.memory": "512Mi",
    "resources.limits.hugepages": "2Mi/80Mi",
    "resources.limits.nvidia.com/gpu": "4",
    "resources.requests.cpu": "250m",
    "resources.requests.memory": "256Mi",
    "resources.requests.hugepages": "2Mi/80Mi"
    "resources.requests.nvidia.com/gpu": "1"
}
Notes:
- If backend-type is not present, it is assumed to be singlevm
- repository-uri is the uri where the full container img, i.e. docker env for MLproject plus MLproject files will be pushed. Use only when kube-client-location is local
- docker env for the MLproject is pushed to by: cd to the MLproject and running
$ docker build .
$ docker tag <image_id_printed_from_prev_cmd> public.ecr.aws/l9n7x1v8/mlflow-projects-demo/base-image
$ docker push public.ecr.aws/l9n7x1v8/mlflow-projects-demo/base-image

kubernetes_job_template contains:
apiVersion: batch/v1
kind: Job
metadata:
  name: "{replaced with MLflow Project name}"
  namespace: default
spec:
  ttlSecondsAfterFinished: 100
  backoffLimit: 0
  template:
    spec:
      containers:
      - name: "{replaced with MLflow Project name}"
        image: "{replaced with URI of Docker image created during Project execution}"
        command: ["{replaced with MLflow Project entry point command}"]
        #env: ["{appended with MLFLOW_TRACKING_URI, MLFLOW_RUN_ID and MLFLOW_EXPERIMENT_ID}"]
        env: []
        resources:
          limits:
            memory: 512Mi
          requests:
            memory: 256Mi
      imagePullSecrets:
      - name: ecr-private-key
      restartPolicy: Never

You can specify the kubernetes_job_template.yaml file or the k8s.resources. If you specify the job template file, and if you are using ecr private registry, you must include the imagePullSecrets section.
'''

class InfinStorSubmittedRun(SubmittedRun):
    """
    A run that just does nothing
    """
    status = RunStatus.RUNNING

    def __init__(self, run_id):
        self._run_id = run_id

    def wait(self):
        return True

    def get_status(self):
        return status;

    def set_status(self, st):
        self.status = st;

    def cancel(self):
        pass

    @property
    def run_id(self):
        return self._run_id



def upload_objects(run_id, bucket_name, path_in_bucket, local_path):
    if (path_in_bucket[0] == '/'):
        path_in_bucket = path_in_bucket[1:]
    if (verbose):
        _logger.info('upload_objects: Entered. bucket=' + bucket_name
                + ', path_in_bucket=' + path_in_bucket + ', local_path=' + local_path)
    try:
        for path, subdirs, files in os.walk(local_path):
            path = path.replace("\\","/")
            directory_name = path.replace(local_path, "")
            for onefile in files:
                src_path = os.path.join(path, onefile)
                if (path_in_bucket.endswith('/')):
                    path_in_bucket = path_in_bucket[:-1]
                if (directory_name.startswith('/')):
                    directory_name = directory_name[1:]
                if (len(directory_name) > 0):
                    dst_path = path_in_bucket + '/' + directory_name
                else:
                    dst_path = path_in_bucket
                    dst_path = dst_path.rstrip('\n')
                if (verbose):
                    _logger.info('upload_objects: Uploading ' + src_path + ' to ' + dst_path)
                tracking.MlflowClient().log_artifact(run_id, src_path, dst_path)
    except Exception as err:
        _logger.info(str(err))

def extract_creds():
    home = expanduser("~")
    if (verbose):
        _logger.info("User's Home Directory is " + home);
    config = configparser.ConfigParser()
    credsfile = home + separator + ".aws" + separator + "credentials"
    config.read(credsfile)
    for section in config.sections():
        if (section == 'infinstor'):
            dct = dict(config[section])
            return dct['aws_access_key_id'], dct['aws_secret_access_key']
    return None, None

class PluginInfinStorProjectBackend(AbstractBackend):
    def run(self, project_uri, entry_point, params,
            version, backend_config, tracking_store_uri, experiment_id):

        if (verbose):
            _logger.info("PluginInfinStorProjectBackend: Entered. project_uri=" + str(project_uri)\
                + ", entry_point=" + str(entry_point)\
                + ", params=" + str(params)\
                + ", version=" + str(version)\
                + ", backend_config=" + str(backend_config)\
                + ", experiment_id=" + str(experiment_id)\
                + ", tracking_store_uri=" + str(tracking_store_uri))

        # ensure that we have MLFLOW_TRACKING_URI, without which get_or_create_run() below will not be handled by infinstor tracking backend.  It will be handled by some other tracking backend, which will not work with this infinstor project backend
        muri:str; pmuri:urllib.parse.ParseResult
        muri, pmuri = _validate_infin_mlflow_tracking_uri_exit(do_exit=True)
        
        work_dir = fetch_and_validate_project(project_uri, version, entry_point, params)
        if 'run-id' in backend_config:
            active_run = get_or_create_run(backend_config['run-id'], project_uri,
                    experiment_id, work_dir, version, entry_point, params)
        else:
            active_run = get_or_create_run(None, project_uri, experiment_id, work_dir, version,
                                       entry_point, params)
        if (verbose):
            _logger.info('active_run=' + str(active_run))
            _logger.info('active_run.info=' + str(active_run.info))

        artifact_uri = active_run.info.artifact_uri
        run_id = active_run.info.run_id

        # Note: this line is screen scraped/parsed in clientlib, to extract the run_id from the output of 'mlflow run -b infinstor_backend ...' command.  See clientlib::run_transform_eks(), clientlib::run_transform_singlevm()
        _logger.info('run_id=' + str(run_id))

        tags = active_run.data.tags
        if (tags['mlflow.source.type'] != 'PROJECT'):
            raise ValueError('mlflow.source_type must be PROJECT. Instead it is '\
                    + tags['mlflow.source.type'])

        if ('parent_run_id' in backend_config):
            parent_run_id = backend_config['parent_run_id']
            tracking.MlflowClient().set_tag(active_run.info.run_id,
                    'mlflow.parentRunId', parent_run_id)

        pdst = urlparse(artifact_uri)
        bucket_name = pdst.netloc
        if (pdst.path[0] == '/'):
            path_in_bucket = pdst.path[1:]
        else:
            path_in_bucket = pdst.path

        '''
        localdir = tags['mlflow.source.name']
        if ('mlflow.source.git.repoURL' in tags or
                'mlflow.gitRepoURL' in tags or
                'mlflow.source.git.commit' in tags):
            pl = urlparse(localdir)
            if (not pl.scheme == 'file'):
                raise ValueError('Cannot deal with scheme ' + pl.scheme + ' in source path')
            localdir = pl.path + separator + pl.fragment
        '''


        project = load_project(work_dir)
        tracking.MlflowClient().set_tag(active_run.info.run_id, MLFLOW_PROJECT_BACKEND, "infinstor")

        backend_type = backend_config.get('backend-type', 'singlevm')
        if backend_type == 'eks':
            return self.run_eks(run_id, backend_type, bucket_name, path_in_bucket, work_dir, project_uri, entry_point,
                    params, version, backend_config, tracking_store_uri, experiment_id, project, active_run)
        elif backend_type == 'singlevm':
            return self.run_singlevm(run_id, backend_type, bucket_name, path_in_bucket, work_dir, project_uri, entry_point,
                    params, version, backend_config, tracking_store_uri, experiment_id, project, active_run)
        else:
            _logger.info('Error. unknown backend type ' + backend_type)
            self.fail_run(run_id)
            rv = InfinStorSubmittedRun(active_run.info.run_id)
            rv.set_status(RunStatus.FAILED)
            return rv

    def run_singlevm(self, run_id, backend_type, bucket_name, path_in_bucket, work_dir, project_uri, entry_point, params,
            version, backend_config, tracking_store_uri, experiment_id, project, active_run):
        instance_type = backend_config['instance_type']
        if (verbose):
            _logger.info('running in singlevm in an instance of type: ' + instance_type)
        upload_objects(run_id, bucket_name, '.infinstor/project_files', work_dir)
        body = dict()
        body['backend_type'] = backend_type
        body['project_files_bucket'] = bucket_name
        body['project_files_path_in_bucket'] = path_in_bucket
        body['params'] = params
        body['run_id'] = run_id
        body['experiment_id'] = str(experiment_id)
        body['instance_type'] = instance_type
        if ('parent_run_id' in backend_config):
            body['parent_run_id'] = backend_config['parent_run_id']
        if ('last_in_chain_of_xforms' in backend_config):
            body['last_in_chain_of_xforms'] = backend_config['last_in_chain_of_xforms']

        if project.docker_env:
            body['docker_image'] = project.docker_env.get("image")

        key, secret = extract_creds()
        if (key != None):
            body['aws_access_key_id'] = key
            body['aws_secret_access_key'] = secret

        cog = CognitoAuthenticatedRestStore()
        headers = {
                'Content-Type': 'application/x-amz-json-1.1',
                'Authorization' : 'Bearer ' + cog.get_token_string()
                }
        url = 'https://' + cog.get_service() + '/api/2.0/mlflow/projects/run-project'

        try:
            response = requests.post(url, data=json.dumps(body), headers=headers)
            response.raise_for_status()
        except HTTPError as http_err:
            _logger.info(f'HTTP error occurred: {http_err}')
            raise
        except Exception as err:
            _logger.info(f'Other error occurred: {err}')
            raise
        else:
            return InfinStorSubmittedRun(active_run.info.run_id)

    def run_eks(self, run_id, backend_type, bucket_name, path_in_bucket, work_dir, project_uri, entry_point, params,
            version, backend_config, tracking_store_uri, experiment_id, project, active_run):
        kube_client_location = backend_config.get('kube-client-location', 'local')
        if kube_client_location == 'local':
            return self.run_eks_on_local(backend_type, project_uri, entry_point, params, version,
                    backend_config, tracking_store_uri, experiment_id, project, active_run, work_dir)
        elif kube_client_location == 'backend':
            return self.run_eks_on_backend(run_id, backend_type, bucket_name, path_in_bucket, work_dir, project_uri,
                    entry_point, params, version, backend_config, tracking_store_uri, experiment_id,
                    project, active_run)
        else:
            raise ValueError('kube_client_location must be either local or backend')

    def run_eks_on_backend(self, run_id, backend_type, bucket_name, path_in_bucket, work_dir, project_uri, entry_point, params,
            version, backend_config, tracking_store_uri, experiment_id, project, active_run):
        upload_objects(run_id, bucket_name, '.infinstor/project_files', work_dir)
        body = dict()
        body['backend_type'] = backend_type
        body['MLFLOW_TRACKING_URI'] = os.getenv('MLFLOW_TRACKING_URI')
        body['params'] = params
        body['run_id'] = run_id
        body['experiment_id'] = str(experiment_id)
        body['docker_image'] = project.docker_env.get("image")
        if not body['docker_image']:
            self.fail_run(run_id)
            raise ValueError('Error. docker image not specified in MLproject')

        if 'kube-job-template-path' in backend_config:
            _logger.info('Using kubernetes job template file ' + backend_config['kube-job-template-path'])
            body['kube_job_template_contents'] = base64.b64encode(
                    open(backend_config.get('kube-job-template-path'), "r").read().encode('utf-8')).decode('utf-8')
            with open(backend_config.get('kube-job-template-path'), "r") as yf:
                yml = yaml.safe_load(yf)
            if 'metadata' in yml and 'namespace' in yml['metadata']:
                body['namespace'] = yml['metadata']['namespace']
                _logger.info('namespace obtained from job template: ' + body['namespace'])
                if 'kube-namespace' in backend_config:
                    if body['namespace'] != backend_config['kube-namespace']:
                        _logger.info('Error. mismatch between namespace in backend configuration and job template')
                        self.fail_run(run_id)
                        rv = InfinStorSubmittedRun(active_run.info.run_id)
                        rv.set_status(RunStatus.FAILED)
                        return rv
            else:
                if 'kube-namespace' in backend_config:
                    body['namespace'] = backend_config['kube-namespace']
                    _logger.info('namespace obtained from backend configuration: ' + body['namespace'])
                else:
                    body['namespace'] = 'default'
        else:
            _logger.info('Using parameters provided in backend configuration to generate a kubernetes job template')
            if "resources.limits.cpu" in backend_config:
                body['resources.limits.cpu'] = backend_config['resources.limits.cpu']
            if "resources.limits.memory" in backend_config:
                body['resources.limits.memory'] = backend_config['resources.limits.memory']
            if "resources.limits.hugepages" in backend_config:
                body['resources.limits.hugepages'] = backend_config['resources.limits.hugepages']
            if "resources.limits.nvidia.com/gpu" in backend_config:
                body['resources.limits.nvidia.com/gpu'] = backend_config['resources.limits.nvidia.com/gpu']
            if "resources.requests.cpu" in backend_config:
                body['resources.requests.cpu'] = backend_config['resources.requests.cpu']
            if "resources.requests.memory" in backend_config:
                body['resources.requests.memory'] = backend_config['resources.requests.memory']
            if "resources.requests.hugepages" in backend_config:
                body['resources.requests.hugepages'] = backend_config['resources.requests.hugepages']
            if "resources.requests.nvidia.com/gpu" in backend_config:
                body['resources.requests.nvidia.com/gpu'] = backend_config['resources.requests.nvidia.com/gpu']
            if 'kube-namespace' in backend_config:
                body['namespace'] = backend_config['kube-namespace']
            else:
                body['namespace'] = 'default'
        kube_context = backend_config.get('kube-context')
        if kube_context:
            body['kube_context'] = kube_context
        if ('parent_run_id' in backend_config):
            body['parent_run_id'] = backend_config['parent_run_id']
        if ('last_in_chain_of_xforms' in backend_config):
            body['last_in_chain_of_xforms'] = backend_config['last_in_chain_of_xforms']
        body['docker_repo_name'] = self.create_docker_repo_name(work_dir)
        commit = _get_git_commit(work_dir)
        if commit:
            _logger.info('Using git commit ' + commit)
            body['git_commit'] = commit

        cog = CognitoAuthenticatedRestStore()
        headers = {
                'Content-Type': 'application/x-amz-json-1.1',
                'Authorization' : 'Bearer ' + cog.get_token_string()
                }
        url = 'https://' + cog.get_service() + '/api/2.0/mlflow/projects/run-project'

        try:
            response = requests.post(url, data=json.dumps(body), headers=headers)
            response.raise_for_status()
        except HTTPError as http_err:
            _logger.info(f'HTTP error occurred: {http_err}')
            raise
        except Exception as err:
            _logger.info(f'Other error occurred: {err}')
            raise
        else:
            return InfinStorSubmittedRun(active_run.info.run_id)

    def fail_run(self, run_id):
        cog = CognitoAuthenticatedRestStore()
        headers = {
                'Content-Type': 'application/x-amz-json-1.1',
                'Authorization' : 'Bearer ' + cog.get_token_string()
                }
        url = 'https://' + cog.get_service() + '/api/2.0/mlflow/runs/update'

        body = {'run_id': run_id, 'status': 'FAILED'}
        try:
            response = requests.post(url, data=json.dumps(body), headers=headers)
            response.raise_for_status()
        except HTTPError as http_err:
            _logger.info(f'HTTP error occurred: {http_err}')
            raise
        except Exception as err:
            _logger.info(f'Other error occurred: {err}')
            raise
        else:
            return

    def create_docker_repo_name(self, work_dir):
        from mlflow.projects.utils import _get_git_repo_url
        wd = _get_git_repo_url(work_dir)
        if not wd:
            _logger.info('Unable to determine git repo. Using working dir ' + os.getcwd() + ' as docker repository name')
            return os.getcwd()
        else:
            _logger.info('Using git repo ' + wd + ' as docker repository name')
            return wd

    def run_eks_on_local(self, backend_type, project_uri, entry_point, params,
            version, backend_config, tracking_store_uri, experiment_id, project, active_run, work_dir):
        kube_context = backend_config.get('kube-context')
        repository_uri = backend_config.get('repository-uri')
        git_commit = backend_config.get('git-commit')
        kube_job_template_path = backend_config.get('kube-job-template-path')
        if (verbose):
            _logger.info("PluginInfinStorProjectBackend: run_eks. kube-context=" + str(kube_context)\
                + ", repository-uri=" + str(repository_uri)\
                + ", git-commit=" + str(git_commit)\
                + ", kube-job-template-path=" + str(kube_job_template_path))

        from mlflow.projects.docker import (
            validate_docker_env,
            validate_docker_installation
        )
        from mlflow.projects import kubernetes as kb

        tracking.MlflowClient().set_tag(active_run.info.run_id, MLFLOW_PROJECT_ENV, "docker")
        validate_docker_env(project)
        validate_docker_installation()

        kube_config = mlflow.projects._parse_kubernetes_config(backend_config)
        # First, try pulling the specific tagged version of the image from the repo
        do_build = True
        if git_commit:
            docker_client = docker.from_env()
            try:
                image = docker_client.images.pull(repository_uri, tag=git_commit[:7])
            except docker.errors.ImageNotFound as inf:
                _logger.info("PluginInfinStorProjectBackend.run_eks_on_local: Docker img "
                        + repository_uri + ", tag=" + git_commit[:7] + " not found. Building...")
            except docker.errors.APIError as apie:
                _logger.info("PluginInfinStorProjectBackend.run_eks_on_local: Error " + str(apie)
                        + " while pulling " + repository_uri + ", tag=" + git_commit[:7])
            else:
                _logger.info("PluginInfinStorProjectBackend.run_eks_on_local: image=" + str(image))
                _logger.info("PluginInfinStorProjectBackend.run_eks_on_local: Docker img found "
                        + repository_uri + ", tag=" + git_commit[:7] + ". Reusing...")
                image_digest = docker_client.images.get_registry_data(image.tags[0]).id
                _logger.info("PluginInfinStorProjectBackend.run_eks_on_local: image_digest=" + image_digest)
                do_build = False
        if do_build:
            _logger.info("PluginInfinStorProjectBackend.run_eks_on_local: Building "
                    + repository_uri)
            image = self.build_docker_image(
                work_dir=work_dir,
                repository_uri=kube_config["repository-uri"],
                base_image=project.docker_env.get("image"),
                run_id=active_run.info.run_id,
                git_commit=git_commit
            )
            image_digest = kb.push_image_to_registry(image.tags[0])

        submitted_run = self.run_eks_job(
            project.name,
            active_run,
            image.tags[0],
            image_digest,
            get_entry_point_command(project, entry_point, params, backend_config['STORAGE_DIR']),
            get_run_env_vars(
                run_id=active_run.info.run_uuid, experiment_id=active_run.info.experiment_id
            ),
            kube_config.get("kube-context", None),
            kube_config["kube-job-template"],
        )
        return submitted_run

    def build_docker_image(self, work_dir, repository_uri, base_image, run_id, git_commit):
        """
        Build a docker image containing the project in `work_dir`, using the base image.
        """
        from mlflow.projects.docker import (
            _create_docker_build_ctx,
            _PROJECT_TAR_ARCHIVE_NAME,
            _GENERATED_DOCKERFILE_NAME
        )
        version_string = ":" + git_commit[:7] if git_commit else ""
        image_uri = repository_uri + version_string
        dockerfile = (
            "FROM {imagename}\n COPY {build_context_path}/ {workdir}\n WORKDIR {workdir}\n"
        ).format(
            imagename=base_image,
            build_context_path=_PROJECT_TAR_ARCHIVE_NAME,
            workdir=MLFLOW_DOCKER_WORKDIR_PATH,
        )
        build_ctx_path = _create_docker_build_ctx(work_dir, dockerfile)
        with open(build_ctx_path, "rb") as docker_build_ctx:
            _logger.info("=== Building docker image %s ===", image_uri)
            client = docker.from_env()
            image, _ = client.images.build(
                tag=image_uri,
                forcerm=True,
                dockerfile=posixpath.join(_PROJECT_TAR_ARCHIVE_NAME, _GENERATED_DOCKERFILE_NAME),
                fileobj=docker_build_ctx,
                custom_context=True,
                encoding="gzip",
            )
        try:
            os.remove(build_ctx_path)
        except Exception:
            _logger.info("Temporary docker context file %s was not deleted.", build_ctx_path)
        tracking.MlflowClient().set_tag(run_id, MLFLOW_DOCKER_IMAGE_URI, image_uri)
        tracking.MlflowClient().set_tag(run_id, MLFLOW_DOCKER_IMAGE_ID, image.id)
        return image


    def run_eks_job(
        self,
        project_name,
        active_run,
        image_tag,
        image_digest,
        command,
        env_vars,
        kube_context=None,
        job_template=None,
    ):
        job_template = mlflow.projects.kubernetes._get_kubernetes_job_definition(
            project_name, image_tag, image_digest, _get_run_command(command), env_vars, job_template
        )
        job_name = job_template["metadata"]["name"]
        job_namespace = job_template["metadata"]["namespace"]
        _load_kube_context(context=kube_context)

        core_api_instance = kubernetes.client.CoreV1Api()
        tok = base64.b64encode(open(tokenfile.get_token_file_name(), "r").read().encode('utf-8')).decode('utf-8')
        token_secret_name = 'infintokenfile-' + str(uuid.uuid4())
        with tokenfile.get_token_file_obj('r') as tok_file_obj:
            tok = base64.b64encode(tok_file_obj.read().encode('utf-8')).decode('utf-8')
        token_secret_name = 'infintokenfile-' + str(uuid.uuid4())
        try:
            core_api_instance.delete_namespaced_secret(namespace=job_namespace, name=token_secret_name)
        except:
            pass
        sec = kubernetes.client.V1Secret()
        sec.metadata = kubernetes.client.V1ObjectMeta(name=token_secret_name)
        sec.type = 'Opaque'
        sec.data = {'token': tok}
        core_api_instance.create_namespaced_secret(namespace=job_namespace, body=sec)
        aws_creds = base64.b64encode(open(os.path.join(expanduser('~'), '.aws', 'credentials'), "r").read().encode('utf-8')).decode('utf-8')
        try:
            core_api_instance.delete_namespaced_secret(namespace=job_namespace, name='awscredsfile')
        except:
            pass
        sec1 = kubernetes.client.V1Secret()
        sec1.metadata = kubernetes.client.V1ObjectMeta(name='awscredsfile')
        sec1.type = 'Opaque'
        sec1.data = {'credentials': aws_creds}
        core_api_instance.create_namespaced_secret(namespace=job_namespace, body=sec1)

        volume_mounts = [
                    kubernetes.client.V1VolumeMount(mount_path='/root/.infinstor', name='infin-token-file'),
                    kubernetes.client.V1VolumeMount(mount_path='/root/.aws', name='aws-creds-file')
                ]
        job_template["spec"]["template"]["spec"]["containers"][0]["volumeMounts"] = volume_mounts

        job_template["spec"]["template"]["spec"]["volumes"] = [
                    kubernetes.client.V1Volume(name="infin-token-file", secret=kubernetes.client.V1SecretVolumeSource(secret_name=token_secret_name)),
                    kubernetes.client.V1Volume(name="aws-creds-file", secret=kubernetes.client.V1SecretVolumeSource(secret_name='awscredsfile'))
                ]

        api_instance = kubernetes.client.BatchV1Api()
        resp = api_instance.create_namespaced_job(namespace=job_namespace, body=job_template, pretty=True)
        _logger.info( resp.kind + " " + resp.metadata.name +" created." )
        tracking.MlflowClient().log_param(active_run.info.run_id, 'kubernetes.job_name', job_name)
        return KubernetesSubmittedRun(active_run.info.run_id, job_name, job_namespace)
