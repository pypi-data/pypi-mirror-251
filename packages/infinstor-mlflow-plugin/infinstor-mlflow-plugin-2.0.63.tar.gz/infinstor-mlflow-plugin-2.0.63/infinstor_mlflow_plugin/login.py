#!/usr/bin/env python
import argparse
from dataclasses import dataclass
import sys
import getpass
import json
import builtins
from typing import Any, Dict, List, Tuple

import jsons
from . import servicedefs   # do not remove 'servicedefs', although it is unreferenced; needed to setup some 'builtins' attributes
from .utils import set_builtins_with_serverside_config
from infinstor_mlflow_plugin.tokenfile import write_token_file, read_token_file, get_token_file_obj
from requests.exceptions import HTTPError
import requests
from os.path import expanduser
from os.path import sep as separator
import time
import configparser
from urllib.parse import unquote, urlparse
import os
import traceback
import logging
import urllib.parse
import jwt

from .utils import _get_logger, _validate_infin_mlflow_tracking_uri_exit

logger:logging.Logger = _get_logger(__name__)

def print_version(token):
    """print the output of /api/2.0/mlflow/infinstor/get_version

    Args:
        token ([type]): [description]
    """
    headers = { 'Authorization': token }
    url = 'https://' + builtins.mlflowserver + '/api/2.0/mlflow/infinstor/get_version'
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
    except HTTPError as http_err:
        print(f'HTTP error occurred while getting version: {http_err}')
        raise
    except Exception as err:
        print(f'Other error occurred while getting version: {err}')
        raise

def get_creds():
    if sys.stdin.isatty():
        username = input("Username: ")
        password = getpass.getpass("Password: ")
    else:
        username = sys.stdin.readline().rstrip()
        password = sys.stdin.readline().rstrip()
    return username, password

def get_customer_info_rest(idToken:str) -> dict:
    """Invokes api.<infinstor.com>/customerinfo API and returns the dict

    Args:
        idToken (str): idToken to use for authentication

    Returns:
        dict: the response from /customerinfo call
        {'awsAccountId': 'xxx', 'enableProjects': 'true', 'InfinSnapBuckets': [], 'InfinStorAccessKeyId': 'xxxx', 'userName': 'xxxxx@infinstor.com', 'serviceVersion': '2.0.18', 'productCode': ['xxxx'], 'iamExternalId': 'xxx', 'customerId': 'xxxxx', 'customerArtifactUri': 'xxxxx', 'customerRoleArn': 'xxxxx', 'mlflowTrackingDdbTableName': 'xxxxxx', 'isSecondaryUser': 'true'}
    """
    payload = ("ProductCode=" + builtins.prodcode)
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Authorization': idToken
        }

    for attempt in range(2):
        url = 'https://' + builtins.apiserver + '/customerinfo'
        try:
            response = requests.post(url, data=payload, headers=headers)
            response.raise_for_status()
            break
        except HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')
            if attempt == 0 and http_err.response.status_code == 504:
                print(f'504 Gateway Timeout. Could be lambda cold start. Retrying once..')
                continue
            else:
                raise
        except Exception as err:
            print(f'Other error occurred: {err}')
            raise

    # print('customerinfo success')
    logger.debug(f"url={url}; response.content={response.content}")
    try:
        response_json:dict = response.json()
    except Exception as e:
        # if authentication fails, see this as the response instead of valid json: response.content=b'<html><head><meta http-equiv="refresh" content="0; URL=\'https://service.isstage13.isstage2.com/login.html\'"/></head><body>Login expired. Please login again</body></html>'
        raise Exception(f"Authentication failed for {url}.  Please check your token and try again.." ) from e
    
    return response_json
    
def _refresh_token(refresh_token:str, region:str) -> Tuple[str, str, str]:
    """
    refreshes the tokens

    _extended_summary_

    Args:
        refresh_token (str): the refresh token needed to perform a token refresh
        region (str): AWS region

    Returns:
        Tuple[str, str, str]: returns the tuple authentication_result, id_token, access_token
    """
    ##Refresh token once############################
    postdata = dict()
    auth_parameters = dict()
    auth_parameters['REFRESH_TOKEN'] = refresh_token
    postdata['AuthParameters'] = auth_parameters
    postdata['AuthFlow'] = "REFRESH_TOKEN_AUTH"
    postdata['ClientId'] = builtins.clientid

    payload = json.dumps(postdata)

    url = 'https://cognito-idp.' +region +'.amazonaws.com:443/'
    headers = {
            'Content-Type': 'application/x-amz-json-1.1',
            'X-Amz-Target' : 'AWSCognitoIdentityProviderService.InitiateAuth'
            }

    try:
        response = requests.post(url, data=payload, headers=headers)
        logger.debug(f"login_and_update_token_file(): response headers for cognito AuthFlow = REFRESH_TOKEN_AUTH for url={url} = {response.headers}")
        logger.debug(f"login_and_update_token_file(): response for cognito AuthFlow = REFRESH_TOKEN_AUTH url={url} = {response.content}")
        response.raise_for_status()
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
        raise
    except Exception as err:
        print(f'Other error occurred: {err}')
        raise

    authres = response.json()['AuthenticationResult']
    idToken = authres['IdToken']
    accessToken = authres['AccessToken']
    
    return authres, idToken, accessToken
    #########

def login_and_update_token_file(region, username, password) -> dict:
    """ does AuthFlow = "USER_PASSWORD_AUTH" or grant_type = 'authorization_code' (oauth)
    
    does AuthFlow = "REFRESH_TOKEN_AUTH"
    
    then updates token file at ~/.infinstor/token or at location specified by environment var INFINSTOR_TOKEN_FILE_DIR

    Args:
        region (str): AWS region where cognito is deployed
        username (str): see above description
        password (str): see above description
        srvdict (dict): dictionary that describes the service; returned by api/2.0/mflow/infinstor/get_version; 
    Returns:
        [dict]: returns /customerinfo REST call results
    """
    
    #############
    #  Note: The use of this function is to write a persistent token file when a CLI login step is performed.  But with PARALLELS_REFRESH_TOKEN or INFINSTOR_REFRESH_TOKEN, an in-memory tokenfile is created, which will be lost when the CLI login process terminates.  As a result, PARALLELS_REFRESH_TOKEN or INFINSTOR_REFRESH_TOKEN are not honored/processed here.  when PARALLELS_REFRESH_TOKEN or INFINSTOR_REFRESH_TOKEN is in use, the in memory tokenfile is created in tokenfile.read_token_file()
    
    # validate that either username or isExternalAuth is specified
    if not builtins.isexternalauth and not username: raise Exception("Internal error: neither external auth or username is specified.  Need to specify at least one. ")
        
    # if not external authentication or username is specified, then use username/password authentication
    if ( not builtins.isexternalauth or username ):
        logger.debug(f"login_and_update_token_file(): login using AuthFlow=USER_PASSWORD_AUTH flow (cognito API)")
        postdata = dict()
        auth_parameters = dict()
        auth_parameters['USERNAME'] = username
        auth_parameters['PASSWORD'] = password
        postdata['AuthParameters'] = auth_parameters
        postdata['AuthFlow'] = "USER_PASSWORD_AUTH"
        postdata['ClientId'] = builtins.clientid

        payload = json.dumps(postdata)

        url = 'https://cognito-idp.' +region +'.amazonaws.com:443/'
        headers = {
                'Content-Type': 'application/x-amz-json-1.1',
                'X-Amz-Target' : 'AWSCognitoIdentityProviderService.InitiateAuth'
                }

        try:
            response:requests.Response = requests.post(url, data=payload, headers=headers)
            logger.debug(f"login_and_update_token_file(): response headers for cognito AuthFlow = USER_PASSWORD_AUTH for url={url} = {response.headers}")
            logger.debug(f"login_and_update_token_file(): response for cognito AuthFlow = USER_PASSWORD_AUTH url={url} = {response.content}")
            response.raise_for_status()
        except HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')
            raise
        except Exception as err:
            print(f'Other error occurred: {err}')
            raise
        
        authres = response.json()['AuthenticationResult']
        idToken = authres['IdToken']
        accessToken = authres['AccessToken']
        refresh_token = authres['RefreshToken']

        ##Refresh token once############################        
        authres, idToken, accessToken = _refresh_token(refresh_token, region)
    else:  # this is the external auth flow..
        logger.debug(f"login_and_update_token_file(): login using grant_type=authorization_code flow (cognito API)")
        serviceserver:str = builtins.serviceserver
        # "https%3A%2F%2Fservice11.ai.isstage1.com%2Fologin.html"
        # https://api13.isstage13.isstage2.com/customerinfo
        redirect_uri:str = f"https://{builtins.mlflowserver}/api/2.0/mlflow/infinstor/cliclient_authorize"
        
        # create the cognito oauth2 URL based on the service dashboard url
        # example url for auth code=https://service11-ai-isstage1-com.auth.us-east-1.amazoncognito.com/oauth2/authorize?redirect_uri=https%3A%2F%2Fservice11.ai.isstage1.com%2Fologin.html&response_type=code&scope=openid&state=uxZCvnJk33cDTIoFhT2yxo846Rdj7Q&access_type=offline&prompt=select_account&client_id=6g8uhmgagq42ii3j6klfcmpru9
        # scope=openid%20email%20profile%20phone&
        oauth2_authorize_url:str = f"https://{serviceserver.replace('.','-')}.auth.{builtins.region}.amazoncognito.com/oauth2/authorize?redirect_uri={urllib.parse.quote_plus( redirect_uri)}&response_type=code&state=uxZCvnJk33cDTIoFhT2yxo846Rdj7Q&access_type=offline&prompt=select_account&client_id={builtins.clientid}"
        
        auth_code:str = input(f"Enter this URL in a browser and obtain a code: {oauth2_authorize_url}\n  Enter the obtained code here: ")
        
        # get the auth2 access token url based on the service dasshboard url
        oauth2_token_url = f"https://{serviceserver.replace('.','-')}.auth.{builtins.region}.amazoncognito.com/oauth2/token"
        # do not urlencode the redirect_uri using urllib.parse.quote_plus():  the post call automatically does this..
        response:requests.Response = requests.post(oauth2_token_url, data={"grant_type":"authorization_code", "client_id":builtins.clientid, "code":auth_code, 'redirect_uri': redirect_uri})
        logger.debug(f"login_and_update_token_file(): response headers for grant_type:authorization_code for url={oauth2_token_url} = {response.headers}")
        logger.debug(f"login_and_update_token_file(): response for grant_type:authorization_code for url={oauth2_token_url} = {response.content}")
        
        authres = response.json()
        idToken = authres['id_token']
        accessToken = authres['access_token']
        refresh_token = authres['refresh_token']
        
        # refresh the token.
        response:requests.Response = requests.post(oauth2_token_url, data={"grant_type":"refresh_token", "client_id":builtins.clientid, "refresh_token":refresh_token})
        logger.debug(f"login_and_update_token_file(): response headers for oauth2 grant_type:refresh_token for url={oauth2_token_url} = {response.headers}")
        logger.debug(f"login_and_update_token_file(): response for oauth2 grant_type:refresh_token for url={oauth2_token_url} = {response.content}")
        accessToken = authres['access_token']
        refresh_token = authres['refresh_token']
        
    token_time = int(time.time())
    write_token_file(token_time, accessToken, refresh_token, builtins.clientid,\
                idToken)

    response_json:dict = get_customer_info_rest(idToken)
    
    # for infinstor s3 proxy for infinsnap.  Note that 'superadmin' will not have these keys populuated populated.
    # This check is needed to avoid this error further down the call stack, when login_infinstor is done for superadmin: Caught exception argument of type 'NoneType' is not iterable
    infinStorAccessKeyId = unquote(response_json.get('InfinStorAccessKeyId')) if response_json.get('InfinStorAccessKeyId') else None
    infinStorSecretAccessKey = unquote(response_json.get('InfinStorSecretAccessKey')) if response_json.get('InfinStorSecretAccessKey') else None
    setup_credentials(infinStorAccessKeyId, infinStorSecretAccessKey)

    logger.info(f'login_and_update_token_file(): Login to service {builtins.service} for username={username} complete')
    print_version(accessToken)
    return response_json, builtins.clientid, refresh_token

def setup_credentials(infinStorAccessKeyId, infinStorSecretAccessKey):
    # Note that 'superadmin' will not have these specified.  
    if infinStorAccessKeyId is None or infinStorSecretAccessKey is None:
        logger.warn(f"Not setting up credentials for s3 proxy for infinsnap")
        return
    
    home = expanduser("~")
    config = configparser.ConfigParser()
    newconfig = configparser.ConfigParser()
    credsfile = home + separator + ".aws" + separator + "credentials"
    if (os.path.exists(credsfile)):
        credsfile_save = home + separator + ".aws" + separator + "credentials.save"
        try:
            os.remove(credsfile_save)
        except Exception as err:
            print()
        try:
            os.rename(credsfile, credsfile_save)
        except Exception as err:
            print()
        config.read(credsfile_save)
        for section in config.sections():
            if (section != 'infinstor'):
                newconfig[section] = {}
                dct = dict(config[section])
                for key in dct:
                    newconfig[section][key] = dct[key]
    else:
        dotaws = home + "/.aws"
        if (os.path.exists(dotaws) == False):
            os.mkdir(dotaws, 0o755)
            open(credsfile, 'a').close()

    newconfig['infinstor'] = {}
    newconfig['infinstor']['aws_access_key_id'] = infinStorAccessKeyId
    newconfig['infinstor']['aws_secret_access_key'] = infinStorSecretAccessKey

    with open(credsfile, 'w') as configfile:
        newconfig.write(configfile)

# returns dict of service details if successful, None if unsuccessful
def bootstrap_from_mlflow_rest(tracking_uri:str=None) -> Dict[str,str]:
    """ use the passed store_uri or MLFLOW_TRACKING_URI environment variable to bootstrap: call get_version() REST API and use it to return a dict with the configuration detected like 'clientid', 'appclientid', 'service', 'region' and others..  If neither is available to bootstrap, exits with an error.

    Args:
        tracking_uri: the URI for the tracking backend store.  if uri has the scheme infinstor (example infinstor://mlflow.infinstor.com), then tracking_uri is used to bootstrap.  Otherwise, MLFLOW_TRACKING_URI is used to detect the store.  
        
    Returns:
        [dict]: see description above.
    """

    muri:str; pmuri:urllib.parse.ParseResult
    muri, pmuri = _validate_infin_mlflow_tracking_uri_exit(tracking_uri=tracking_uri, do_exit=True)
        
    # extract 'infinstor.com' from 'mlflow.infinstor.com'
    cognito_domain = pmuri.hostname[pmuri.hostname.index('.')+1:]
    url = 'https://' + pmuri.hostname + '/api/2.0/mlflow/infinstor/get_version'
    headers = { 'Authorization': 'None' }
    try:
        response = requests.get(url, headers=headers)
        logger.debug(f"response headers from url={url}: {response.headers}")
        logger.debug(f"response from url={url}: {response.content}")
        response.raise_for_status()
        resp = response.json()
        serv_dict:Dict[str,str] = { 'clientid' : resp['cognitoCliClientId'],
                'appclientid' : resp['cognitoAppClientId'],
                'mlflowserver' : resp['mlflowDnsName'] + '.' + cognito_domain,
                'mlflowuiserver' : resp['mlflowuiDnsName'] + '.' + cognito_domain,
                'mlflowstaticserver' : resp['mlflowstaticDnsName'] + '.' + cognito_domain,
                'apiserver' : resp['apiDnsName'] + '.' + cognito_domain,
                'serviceserver' : resp['serviceDnsName'] + '.' + cognito_domain,
                'service' : cognito_domain,
                'region': resp['region'],
                # handle the case where server is a old version that doesn't set this.. server returns the string 'true' or 'false' and not boolean True or False
                'isexternalauth': resp.get('isExternalAuth', False) }
        logger.debug(f"Service details from url={url}: {serv_dict}")
        return serv_dict
    except HTTPError as http_err:
        logger.error(f"Caught Exception: {http_err}: {traceback.format_exc()}" )
        return None
    except Exception as err:
        logger.error(f"Caught Exception: {err}: {traceback.format_exc()}" )
        return None

def _login(srvdct, username:str=None, password:str=None) -> Tuple[str, str]:
    """ 
    performs a login into the service.  Reads and writes the token file (in memory or filesystem).  Also sets the builtins based on values of 'srvdct'
    
    Note that the underlying token store is determined by: {INFINSTOR_COGNITO_CLIENTID , INFINSTOR_REFRESH_TOKEN}, then INFINSTOR_TOKEN_FILE_DIR, and ~/.infinstor/token.  tokenfile.read_token_file() and tokenfile.write_token_file() rely on the above to read and write tokens. 
    
    When logging in and operational mode is {INFINSTOR_COGNITO_CLIENTID , INFINSTOR_REFRESH_TOKEN}, then set the env variables to empty strings: this will force a login and then internally set these environment variables to the right values.
    
    if login is invoked without an username (and password), then the refresh_token from the existing token file is returned.
    if login is invoked with an username (and password), and if the username specified doesn't match the token file username, then a re-login is forced.
    if the token file service name doesn't match the current service name, a relogin is forced.
    if the token file doesn't exist, a login is forced.
    Args:
        srvdct [dict]: service dictionary which describes the service
        
    Returns:
        Tuple[str,str]: retunrs the tuple (cognito_client_id, refresh_token)
    """
    set_builtins_with_serverside_config(srvdct)
    
    decoded:Dict[str, Any] = {}; service:str = None
    try:
        # read the token file if it exists and return the refresh_token, instead of performing a cognito login.
        # 
        # the very first time a login is performed from the CLI, the 'token' file will not exist.  So use 'exit_on_error=False' below; in this casethe return value will be a tuple of Nones
        # 
        # if {INFINSTOR_REFRESH_TOKEN, INFINSTOR_COGNITO_CLIENTID} is set and empty (when logging in using this method, these are usually set to empty), the return value is a tuple of Nones. See read_token_file() for details.
        access_token, refresh_token, token_time, client_id, service, token_type, id_token = read_token_file(exit_on_error=False)
        # if we were able to read the token file, then use its values instead of performing a login
        if refresh_token:
            decoded:Dict = jwt.decode(access_token, options={"verify_signature":False})

            # since we use 'exit_on_error=False' in the call above, there is a chance that service can be None (if MLFLOW_TRACKING_URI or its variants are not set)
            # 
            # if username is not specified or if specified and matches token file user and the service matches, then expectation is to return the refresh_token from the token file
            if ( (not username or username == decoded.get('username') ) and service and service == builtins.service):
                print(f"Login to service {service} completed for user {decoded.get('username')}")
                # return the client_id and refresh_token from the existing token file
                return client_id, refresh_token
    except Exception as err:
        logger.error('caught exception in _login() and ignored: ' + str(err), exc_info=err)
        pass

    # at this point, we weren't able to fetch the refresh_token (for reasons listed above: token file doesn't exist or username mismatch or service mismatch), and so need to perform a login.
    if not username or not password:
        if not builtins.isexternalauth:
            username, password = get_creds() 
    
    # if token file was found but token file username doesn't match the specified username, force a login
    if username and decoded and decoded.get('username') != username:
        print(f"current token file user {decoded['username']} does not match the specified login username {username}:. Forcing login")
    
    if service and service != builtins.service:
        print(f'mismatch in value for service between MLFLOW_TRACKING_URI (service={builtins.service}) and token file (service={service}). Forcing login')
    
    customerinfo:dict;cognito_client_id:str; refresh_token:str; 
    customerinfo, cognito_client_id, refresh_token = login_and_update_token_file(srvdct['region'], username, password)

    # set enableProjects / isProjectEnabled ; /customer_info REST response has 'enableProjects': 'true'        
    builtins.enableProjects = True if customerinfo.get('enableProjects', False) == 'true' else False
    srvdct['enableProjects'] = builtins.enableProjects
    logger.debug(f"enableProjects={builtins.enableProjects}")
    
    return cognito_client_id, refresh_token

def login_cli():
    # if --username is specified, force a password login, even if the system is configured for external oauth authentication
    argparser:argparse.ArgumentParser = argparse.ArgumentParser()
    argparser.add_argument("--username", required=False, default=None)
    argparser.add_argument("--password", required=False, default=None)
    parsed_args:argparse.Namespace = argparser.parse_args()
    
    # if username is specified, then password must be specified; and vice versa
    if (parsed_args.username and not parsed_args.password) or (not parsed_args.username and parsed_args.password):
        logger.error(f"Error: only one of username or password was specified.  Both must be specifeid")
        return 255
    
    logger.debug(f"parsed_args.username={parsed_args.username}; parsed_args.password={parsed_args.password}")
    retval:int = 0
    try:
        cognito_client_id:str; refresh_token:str
        cognito_client_id, refresh_token = _login(bootstrap_from_mlflow_rest(), parsed_args.username, parsed_args.password)
    except Exception as e:
        logger.error(f"login_cli(): Caught exception {e}", exc_info=e)
        retval = 255
        
    return retval

def login(username:str, password:str) -> Tuple[str, str]:
    """
    login api.  
    
    Note that login() can store the token in one of 3 locations:
    -- INFINSTOR_TOKEN_FILE_DIR environment variable: perform login and store the token file (named token) in this directory
    -- INFINSTOR_REFRESH_TOKEN and INFINSTOR_COGNITO_CLIENT_ID environment variables are set to empty: perform login and store the token in an in-memory file.
    -- None of the above environment variables are set: perform login and store the token in ~/.infinstor/token file

    Args:
        username (str): _description_
        password (str): _description_

    Returns:
        Tuple[str, str]: return the tuple (cognito_client_id, refresh_token).  On failure, {None, None} is returned
    """
    try:
        return _login(bootstrap_from_mlflow_rest(), username, password)
    except Exception as e:
        logger.error(f"login(): Caught exception {e}", exc_info=e)
        return None, None

def get_python_creds():
    username = input("Username: ")
    password = getpass.getpass("Password: ")
    return username, password

def new_login():
    uname, passwd = get_python_creds()
    _login(bootstrap_from_mlflow_rest(), uname, passwd)

@dataclass
class _InfinstorServiceVersion(jsons.JsonSerializable):
    #service_name:str                            # service_name like isstage2

    client_python_package_versions:Dict[str,str]         # version for python packages: infinstor (clientlib), jupyterlab-infinstor (server-extension) and infinstor-mlflow-plugin (infinstor-mlflow/plugin)
    client_npm_package_versions:Dict[str,str]            # version for npm package: jupyterlab-infinstor (browser_component)
    
    service_version:str = None                         # service version
    
    infinstor_web_version:str = None                   # infinstor-web version
    infinstor_lambda_version:str = None                # infinstor/lambda version
    infinstor_mlflow_lambda_version:str = None         # infinstor-mlflow/server/lambda version
    
    pip_index_url:str = 'https://www.pypi.org/simple'                           # pip index url for pypi repository
    pip_extra_index_urls:List[str] = ('https://pip.infinstor.com')              # pip extra index urls for additional pypi compliant repositories
    
    # "optimized" == rely on hash of infinstor_service_version.json to determine if auto update must be done or not.  faster than "normal" but will only work for '==' version specifiers (no ranges)
    #      Do not use this when version ranges for python packages are specifed in the json
    #      because the hash may not have changed (and no auto update will be attempted) but in reality an auto-update may be needed (say a version range is used in the version specifier in json and a newer version
    #      of a python package is uploaded to pypi that matches this version range)
    # "disabled"  == disable auto update..
    # "normal"  == the above hash based check is disabled.  And pip is used to determine if an update is needed..  slower than "optimized" but will work for all scenarios.
    auto_update_strategy:str = "optimized"

def _downloadJsonUrlAndDeser(url:str, cls) -> Tuple[bytes,Any]:
    """
    downloads the json from specified 'url' and deserializes it to an instance of the specified 'cls'

    [extended_summary]

    Args:
        url (str): URL for the json to be downloaded

    Returns:
        Tuple[bytes,Any]: on Success, returns the Tuple ( json_response_as_string_from_url , deserialized json as an instance of specified 'cls' ); None on failure
    """
    try:
        with urllib.request.urlopen(url, timeout=10, ) as f:
            urlcontents:str = f.read()   #read the contents of the url
            logger.debug(f"Response for url={url}={urlcontents}")
            return (urlcontents, jsons.loads(urlcontents, cls))
    except Exception as e:
        logger.error(f"Caught exception for url={url}: ", exc_info=e)

    return (None,None)

def get_infinstor_client_versions():
    """
    Fetches the python client library versions from the server, based on the server specified in MLFLOW_TRACKING_URI.  These python client versions, that match the server, can then be installed by the user, for successfully working with this server.
    Maps to the command 'infinstor_get_client_versions' specified in setup.py

    _extended_summary_
    """
    get_version_resp:Dict[str,str] = bootstrap_from_mlflow_rest()
    
    # download https://<service_name>/assets/infinstor_service_version.json
    infin_service_ver_json_url = f"https://{get_version_resp['serviceserver']}/infinstor_service_version.json"
    jsonbytes:bytes; infin_service_ver:_InfinstorServiceVersion; (jsonbytes, infin_service_ver) = _downloadJsonUrlAndDeser(infin_service_ver_json_url, _InfinstorServiceVersion)
    
    logger.debug(f"client_python_package_versions={infin_service_ver.client_python_package_versions}")
    logger.info(list(map(
        # some old infinstor_service_version.json's still may have infinstor-py-bootstrap in them.  Filter this out
        lambda x: f"pip install {x[1]}" if x[1].lower().find("bootstrap") == -1 else "", 
        infin_service_ver.client_python_package_versions.items())))
    
if __name__ == "__main__":
    exit(login_cli())
