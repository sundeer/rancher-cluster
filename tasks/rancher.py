from invoke import ctask as task
import time
import requests
import gdapi


@task
def env(ctx,
        list=False,
        create=False,
        delete=False,
        name=None,
        description=None,
        type='cattle'):
    '''Create and interact with environments/projects'''

    rancher = gdapi.Client(url=get_root_api_url(ctx),
                           access_key=ctx.rancher.access_key,
                           secret_key=ctx.rancher.secret_key)

    if list:
        environments = rancher.list_project().data
        env_names = [environment.name for environment in environments]

        print('')
        print('Rancher Environments')
        print('--------------------')
        print(*env_names, sep='\n')
        print('')
    elif create:
        types = {'swarm', 'kubernetes', 'mesos', 'cattle'}

        if name is None:
            print()
            print('Must specify environment name with -n or -name')
            print()
            return 1
        elif type not in types:
            print()
            print('Option "-t/--type_of_env" must be one of {0}'.format(types))
            print()
            return 1

        environment = {
            "name": name,
            "description": description,
            "swarm": type == 'swarm',
            "kubernetes": type == 'kubernetes',
            "mesos": type == 'mesos'
        }
        rancher.create_project(**environment)

        print('')
        print("Environment '{}' created".format(name))
    elif delete:
        environments = rancher.list_project().data

        for environment in environments:
            if environment.name is name:
                environment = rancher.by_id_project(environment.id)
                rancher.delete(environment)

                print('')
                print("Environment '{0}' deleted".format(name))
                return

        print('')
        print('No such environment: {0}'.format(name))


def resource(ctx, list=False):
    pass


def resource_url(ctx, session, resource_name='all'):
    response = wait_for_server(ctx, session)

    schemas_url = response.headers['X-Api-Schemas']
    response = session.get(schemas_url)

    schemas = response.json()['data']
    collections = [ s for s in schemas if 'collection' in s['links'] ]
    urls = { c['pluralName']:c['links']['collection'] for c in collections }
    if resource_name is 'all':
        return urls
    else:
        return urls[resource_name]


def wait_for_server(ctx, session):
    url = get_root_api_url(ctx)

    print('Rancher server: {0}'.format(url))
    print('Waiting for server to respond.')
    print('This may take a few minutes')
    print('')

    responding = False
    while not responding:
        print('.', end="", flush=True)
        try:
            response = session.get(url, timeout=1)
            response.raise_for_status()
            if response.status_code is 200:
                responding = True
        except requests.exceptions.ConnectionError:
            time.sleep(1)
        except requests.exceptions.Timeout:
            pass
    print('')
    return response


def get_agent_registration_data(ctx, env):
    session = create_rancher_http_session(ctx)

    environments_url = resource_url(ctx, session, 'projects')
    response = session.get(environments_url)
    response.raise_for_status()

    environments = response.json()['data']
    environment_url = None
    for e in environments:
        if e['name'] == env:
            environment_url = e['links']['self']
    if environment_url is None:
        return None, None
    else:
        response = session.get(environment_url)
        response.raise_for_status()

        tokens_url = response.json()['links']['registrationTokens']
        response = session.post(tokens_url)
        response.raise_for_status()
        token_url = response.json()['links']['self']

        response = session.get(token_url)
        token_data_state = response.json()['state']
        while token_data_state != 'active':
            response = session.get(token_url)
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


def create_rancher_http_session(ctx):
    access_key = ctx.rancher.access_key
    secret_key = ctx.rancher.secret_key

    session = requests.Session()
    session.auth = (access_key, secret_key)
    session.verify = False
    return session
