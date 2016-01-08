from invoke import ctask as task
from invoke import run, exceptions
from jinja2 import Environment, FileSystemLoader
from tasks import rancher, terraform
import requests
import json
import os



@task
def create_vpc(ctx):
    terraform.apply(ctx)


@task
def build(ctx, hosts=None, servers=None):
    resource_count = _count_current_resource(ctx, res_type='any')
    if resource_count is not 0:
        print('')
        print('Cluster already created!')
        list(ctx)
        return 1

    if servers is not None:
        add_servers(ctx, servers)

    if hosts is not None:
        add_hosts(ctx, number=hosts)


@task
def destroy(ctx):
    terraform.destroy(ctx)


@task
def add_servers(ctx, number):
    current_servers = terraform.count_resource(ctx, 'aws_instance.server')
    servers_to_add = int(number)
    servers = current_servers + servers_to_add
    terraform.apply(ctx, servers=servers)


@task
def remove_servers(ctx, number):
    current_servers = terraform.count_resource(ctx, 'aws_instance.server')
    servers_to_remove = int(number)
    servers = current_servers - servers_to_remove
    if servers < 0:
        servers = 0
    terraform.apply(ctx, servers=servers)


@task
def add_hosts(ctx, number, environment='Default', token=False):
    current_hosts = terraform.count_resource(ctx, 'aws_instance.host')
    hosts_to_add = int(number)
    hosts = current_hosts + hosts_to_add

    rancher.wait_for_server(ctx)

    url, image = rancher.get_agent_registration_data(ctx)

    terraform.apply(ctx, hosts=hosts, agent_registration_url=url, rancher_agent_image=image)

# Broke after adding host user_data template
# @task
# def remove_hosts(ctx, number):
#     current_hosts = terraform.count_resource(ctx, 'aws_instance.host')
#     hosts_to_remove = int(number)
#     hosts = current_hosts - hosts_to_remove
#     if hosts < 0:
#         hosts = 0
#     terraform.apply(ctx, hosts=hosts)


@task
def plan(ctx):
    terraform.apply(ctx, action)


@task
def recreate(ctx, hosts=None, servers=None):
    if hosts is None:
        current_hosts = terraform.count_resource(ctx, 'aws_instance.host')
        hosts = current_hosts

    if servers is None:
        current_servers = terraform.count_resource(ctx, 'aws_instance.server')
        servers = current_servers

    destroy(ctx)
    create(ctx, hosts=hosts, servers=servers)


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
    servers = _count_current_resource(ctx, res_type='server')
    hosts = _count_current_resource(ctx, res_type='host')
    resources = _count_current_resource(ctx, res_type='any')

    print('')
    print('Current Resources')
    print('-----------------')
    print('Servers:   {0}'.format(servers))
    print('Hosts:     {0}'.format(hosts))
    print('Resources: {0}'.format(resources))
    print('')


def _count_current_resource(ctx, res_type='any'):
    if res_type == 'any':
        count = terraform.count_resource(ctx, '.*')
    elif res_type == 'host':
        count = terraform.count_resource(ctx, 'aws_instance.host')
    elif res_type == 'server':
        count = terraform.count_resource(ctx, 'aws_instance.server')
    return count


def _create_hosts_cloud_config_user_data(ctx, registration_url):
    path = os.path.dirname(os.path.abspath(__file__))
    template_environment = Environment(
        autoescape=False,
        loader=FileSystemLoader(os.path.join(path, 'templates')),
        trim_blocks=False)
    context = {'registration_url': registration_url}
    target = template_environment.get_template('agent.yml.j2').render(context)
    f = open(os.path.join(path, '../terraform/cloud-config/agent.yml'), 'w')
    f.write(target)
