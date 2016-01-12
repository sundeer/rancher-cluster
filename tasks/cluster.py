from invoke import ctask as task
from invoke import run, exceptions
from tasks import rancher, terraform
import os



@task
def create_infra(ctx):
    '''Creates only the infrastructure, no serves/hosts will be created'''
    terraform.apply(ctx)


@task(help={'servers': "Number of Rancher servers to create",
            'hosts'  : "Number of Rancher hosts to create"})
def build(ctx, hosts=None, servers=None):
    '''Build cluster infrastructure and optionally add servers/hosts'''

    resource_count = terraform.count_current_resource(ctx, res_type='any')
    if resource_count is not 0:
        print('')
        print('Cluster already created!')
        list(ctx)
        return 1

    if servers is not None:
        add_servers(ctx, servers)

    if hosts is not None:
        for host in range(int(hosts)):
            add_host(ctx)


@task
def destroy(ctx):
    '''Completely destroy all previously created cluster resources'''
    terraform.destroy(ctx)


@task(help={'number': "Number of Rancher servers to add to cluster"})
def add_servers(ctx, number):
    '''Add Rancher servers to cluster'''
    current_servers = terraform.count_resource(ctx, 'aws_instance.server')
    servers_to_add = int(number)
    servers = current_servers + servers_to_add
    terraform.apply(ctx, servers=servers)
    rancher.wait_for_server(ctx)


# @task
# def remove_servers(ctx, number):
#     current_servers = terraform.count_resource(ctx, 'aws_instance.server')
#     servers_to_remove = int(number)
#     servers = current_servers - servers_to_remove
#     if servers < 0:
#         servers = 0
#     terraform.apply(ctx, servers=servers)


@task(help={'number': "Number of Rancher hosts to add to cluster",
            'env'   : "Name of Rancher Environment host(s) will be added to"})
def add_host(ctx, env='Default', token=False):
    '''Add Rancher host to cluster'''
    current_servers = terraform.count_resource(ctx, 'aws_instance.server')
    if current_servers == 0:
        print('')
        print('No Rancher server found. Server must')
        print('be created prior to adding hosts')
        return 1

    current_hosts = terraform.count_resource(ctx, 'aws_instance.host')
    hosts = current_hosts + 1

    url, image = rancher.get_agent_registration_data(ctx, env)
    if url is None:
        print('')
        print('No such environment: {0}'.format(env))
        return 1

    # target only this host (host count starts with 0)
    target = 'aws_instance.host[{0}]'.format(hosts - 1)

    terraform.apply(
        ctx,
        hosts=hosts,
        agent_registration_url=url,
        rancher_agent_image=image,
        target=target
    )


@task
def remove_host(ctx):
    current_hosts = terraform.count_resource(ctx, 'aws_instance.host')
    if current_hosts == 0:
        print('')
        print('There are no hosts to remove')

    hosts = current_hosts - 1
    if hosts == 0:
        # This is a special case since terraform removes the host index when
        # there is only a single instance
        terraform.apply(ctx, hosts=0)
    else:
        # target only the last host added host (host count starts with 0)
        target = 'aws_instance.host[{0}]'.format(current_hosts - 1)
        terraform.apply(ctx, hosts=hosts, target=target)


# @task
# def recreate(ctx, hosts=None, servers=None):
#     if hosts is None:
#         current_hosts = terraform.count_resource(ctx, 'aws_instance.host')
#         hosts = current_hosts
#
#     if servers is None:
#         current_servers = terraform.count_resource(ctx, 'aws_instance.server')
#         servers = current_servers
#
#     destroy(ctx)
#     create(ctx, hosts=hosts, servers=servers)


# @task
# def refresh(ctx):
#     current_servers = terraform.count_resource(ctx, 'aws_instance.server')
#     current_hosts = terraform.count_resource(ctx, 'aws_instance.host')
#
#     rancher.wait_for_server(ctx)
#     url, image = rancher.get_agent_registration_data(ctx)
#     _create_hosts_cloud_config_user_data(ctx, url)
#
#     terraform.apply(ctx, hosts=current_hosts, servers=current_servers)


@task
def list(ctx):
    '''Lists all server, host, and other active cluster resources'''
    servers = terraform.count_current_resource(ctx, res_type='server')
    hosts = terraform.count_current_resource(ctx, res_type='host')
    resources = terraform.count_current_resource(ctx, res_type='any')

    print('')
    print('Current Resources')
    print('-----------------')
    print('Servers:   {0}'.format(servers))
    print('Hosts:     {0}'.format(hosts))
    print('Resources: {0}'.format(resources))
    print('')
