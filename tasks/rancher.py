from invoke import ctask as task
from tasks import utils
import time
import requests
import json

@task
def environments(ctx,
    list=False,
    create=False,
    name=None,
    description="",
    servicePortRange=None,
    members=[]):

    environments_url = resource_url(ctx, 'projects')

    if list:
        response = requests.get(environments_url, verify=False)
        if response.status_code != 200:
            raise ApiError('GET /v1/projects/ {}'.format(response.status_code))
        environments = response.json()['data']
        env_names = [ environment['name'] for environment in environments ]
        print('')
        print('Rancher Environments')
        print('--------------------')
        print(*env_names, sep='\n')
        print('')
    elif create:
        data = {"name": name,
                "description": description,
                "servicePortRange": servicePortRange,
                "members": members}
        response = requests.post(environments_url, data, verify=False)
        response.raise_for_status()
        print('')
        print("Environment '{}' created".format(name))
        # environments(ctx, list=True)
    elif delete:
        response = requests.get(environments_url)
        environments = response.json()['data']

        response = requests.post(environments_url, data, verify=False)
        response.raise_for_status()
        print('')
        print("Environment '{}' created".format(name))
        # environments(ctx, list=True)


@task
def resource(ctx, list=False):
    pass






def resource_url(ctx, resource_name='all'):
    # see invoke.yml in project root
    hostname = ctx.rancher.server.hostname
    domain_name = ctx.rancher.server.domain_name
    api = ctx.rancher.server.api

    server = '{0}.{1}'.format(hostname, domain_name)
    url = 'https://{0}/{1}'.format(server, api)

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
    # see invoke.yml in project root
    hostname = ctx.rancher.server.hostname
    domain_name = ctx.rancher.server.domain_name
    api = ctx.rancher.server.api

    server = '{0}.{1}'.format(hostname, domain_name)
    url = 'https://{0}/{1}'.format(server, api)

    print('Waiting for Rancher server to respond.')
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


def get_agent_registration_data(ctx):
    # see invoke.yml in project root
    hostname = ctx.rancher.server.hostname
    domain_name = ctx.rancher.server.domain_name
    api = ctx.rancher.server.api

    server = '{0}.{1}'.format(hostname, domain_name)
    url = 'https://{0}/{1}/projects'.format(server, api)
    # url = 'http://{0}:8080/{1}/projects'.format(server, api)

    response = requests.get(url, verify=False)
    if response.status_code != 200:
        raise ApiError('GET /v1/projects/ {}'.format(response.status_code))
    url = response.json()['data'][0]['links']['registrationTokens']
    response = requests.post(url, verify=False)
    response = requests.get(url, verify=False)

    registration_url = response.json()['data'][0]['registrationUrl']
    image = response.json()['data'][0]['image']
    return registration_url, image
