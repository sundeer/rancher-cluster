from invoke import ctask as task
from invoke import run, exceptions
from tasks import rancher, terraform
import os



@task
def create_infra(ctx):
    '''Creates only the infrastructure, no serves/hosts will be created'''
    terraform.apply(ctx)


@task(help={'servers'      : "Number of Rancher servers to create",
            'hosts'        : "Number of Rancher hosts to create",
            'instance_type': "AWS EC2 instance type"})
def build(ctx, hosts=None, servers=None, instance_type=None):
    '''Build cluster infrastructure and optionally add servers/hosts'''

    resource_count = terraform.count_resource(ctx, res_type='any')
    if resource_count is not 0:
        print('')
        print('Cluster already created!')
        list(ctx)
        return 1

    if servers is not None:
        add_servers(ctx, servers, instance_type=instance_type)

    if hosts is not None:
        for host in range(int(hosts)):
            add_host(ctx, instance_type=instance_type)


@task
def destroy(ctx):
    '''Completely destroy all previously created cluster resources'''
    terraform.destroy(ctx)


@task(help={'number': "Number of Rancher servers to add to cluster",
            'instance_type': "AWS EC2 instance type, default=t2.micro"})
def add_servers(ctx, number, instance_type=None):
    '''Add Rancher servers to cluster'''
    current_servers = terraform.count_resource(ctx, 'server')
    servers_to_add = int(number)
    servers = current_servers + servers_to_add
    terraform.apply(ctx, servers=servers, instance_type=instance_type)
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
            'instance_type': "AWS EC2 instance type",
            'env'   : "Name of Rancher Environment host(s) will be added to"})
def add_host(ctx, env='Default', instance_type=None):
    '''Add Rancher host to cluster'''
    current_servers = terraform.count_resource(ctx, 'server')
    if current_servers == 0:
        print('')
        print('No Rancher server found. Server must')
        print('be created prior to adding hosts')
        return 1

    current_hosts = terraform.count_resource(ctx, 'host')
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
        instance_type=instance_type,
        agent_registration_url=url,
        rancher_agent_image=image,
        env=env,
        target=target
    )


@task
def remove_host(ctx, env='Default'):
    '''Remove a single host from the selected Rancher environment'''
    current_total_hosts = terraform.count_resource(ctx, 'host')
    new_total_hosts = current_total_hosts - 1
    hosts_in_env = terraform.get_hosts_by_environment(ctx, env)
    number_of_hosts_in_env = len(hosts_in_env)

    if number_of_hosts_in_env == 0:
        print()
        print('There are no hosts in environment: {0}'.format(env))
        print()
        return 1

    if new_total_hosts == 0:
        # This is a special case since terraform removes the host index when
        # there is only a single host instance
        target = ['aws_instance.host']
        terraform.destroy(ctx, target)
    else:
        # Grab the name of the last host in the list
        target_host = hosts_in_env.pop()
        # The part after the . is the host index
        target_host_index = target_host.rsplit('.', 1)[-1]
        # Target only that host
        target = ['aws_instance.host[{0}]'.format(target_host_index)]
        terraform.destroy(ctx, target)


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
    servers = terraform.count_resource(ctx, res_type='server')
    hosts = terraform.count_resource(ctx, res_type='host')
    resources = terraform.count_resource(ctx, res_type='any')

    print('')
    print('Current Resources')
    print('-----------------')
    print('Servers:   {0}'.format(servers))
    print('Hosts:     {0}'.format(hosts))
    print('Resources: {0}'.format(resources))
    print('')
