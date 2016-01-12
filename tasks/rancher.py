from invoke import ctask as task
import gdapi
from tasks import utils
import time
import requests
import json

@task
def env(ctx,
    list=False,
    create=False,
    delete=False,
    name=None,
    description=None):
    '''Create and interact with environments/projects'''

    environments_url = resource_url(ctx, 'projects')

    if list:
        response = requests.get(environments_url, verify=False)
        response.raise_for_status()

        environments = response.json()['data']
        env_names = [ environment['name'] for environment in environments ]
        print('')
        print('Rancher Environments')
        print('--------------------')
        print(*env_names, sep='\n')
        print('')
    elif create:
        data = {"name": name,
                "description": description}
        response = requests.post(environments_url, data, verify=False)
        response.raise_for_status()

        print('')
        print("Environment '{}' created".format(name))
        # environments(ctx, list=True)
    elif delete:
        response = requests.get(environments_url, verify=False)
        response.raise_for_status()

        environments = response.json()['data']
        environment_url = None
        for e in environments:
            if e['name'] == name:
                environment_url = e['links']['self']
        if environment_url is not None:
            response = requests.delete(environment_url, verify=False)
            response.raise_for_status()
            print('')
            print("Environment '{0}' deleted".format(name))
        else:
            print('')
            print('No such environment: {0}'.format(name))


def resource(ctx, list=False):
    pass


def resource_url(ctx, resource_name='all'):
    url = get_root_api_url(ctx)

    response = wait_for_server(ctx)

    schemas_url = response.headers['X-Api-Schemas']
    response = requests.get(schemas_url, verify=False)

    schemas = response.json()['data']
    collections = [ s for s in schemas if 'collection' in s['links'] ]
    urls = { c['pluralName']:c['links']['collection'] for c in collections }
    if resource_name is 'all':
        return urls
    else:
        return urls[resource_name]


def wait_for_server(ctx):
    url = get_root_api_url(ctx)

    print('Rancher server: {0}'.format(url))
    print('Waiting for server to respond.')
    print('This may take a few minutes')

    responding = False
    while not responding:
        print('.', end="", flush=True)
        try:
            response = requests.get(url, verify=False, timeout=1)
            if response.status_code is 200:
                responding = True
        except requests.exceptions.ConnectionError:
            time.sleep(1)
        except requests.exceptions.Timeout:
            pass
    print('')
    return response


def get_agent_registration_data(ctx, env):
    environments_url = resource_url(ctx, 'projects')
    response = requests.get(environments_url, verify=False)
    response.raise_for_status()

    environments = response.json()['data']
    environment_url = None
    for e in environments:
        if e['name'] == env:
             environment_url = e['links']['self']
    if environment_url is None:
        return None, None
    else:
        response = requests.get(environment_url, verify=False)
        response.raise_for_status()

        tokens_url = response.json()['links']['registrationTokens']
        response = requests.post(tokens_url, verify=False)
        response.raise_for_status()
        token_url = response.json()['links']['self']

        response = requests.get(token_url, verify=False)
        token_data_state = response.json()['state']
        while token_data_state != 'active':
            response = requests.get(token_url, verify=False)
            token_data_state = response.json()['state']
            time.sleep(1)

        registration_url = response.json()['registrationUrl']
        image = response.json()['image']
        return registration_url, image


def get_root_api_url(ctx):
    scheme      = ctx.rancher.server.scheme
    port        = ctx.rancher.server.port
    hostname    = ctx.rancher.server.hostname
    domain_name = ctx.rancher.server.domain_name
    api         = ctx.rancher.server.api

    server = '{0}.{1}'.format(hostname, domain_name)
    url = '{0}://{1}:{2}/{3}'.format(scheme, server, port, api)

    return url
