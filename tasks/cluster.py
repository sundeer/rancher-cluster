from invoke import ctask as task
from invoke import run, exceptions
from jinja2 import Environment, FileSystemLoader
from tasks import rancher
import requests
import json
import os
import re



@task
def create_vpc(ctx):
    action = 'apply'
    _terraform(ctx, action)


@task
def create(ctx, hosts=None, servers=None):
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
    action = 'destroy'
    _terraform(ctx, action)


@task
def add_servers(ctx, number):
    current_servers = _count_tf_resource(ctx, 'aws_instance.server')
    servers_to_add = int(number)
    servers = current_servers + servers_to_add
    action = 'apply'
    _terraform(ctx, action, servers=servers)


@task
def remove_servers(ctx, number):
    current_servers = _count_tf_resource(ctx, 'aws_instance.server')
    servers_to_remove = int(number)
    servers = current_servers - servers_to_remove
    if servers < 0:
        servers = 0
    action = 'apply'
    _terraform(ctx, action, servers=servers)


@task
def add_hosts(ctx, number, environment='Default', token=False):
    current_hosts = _count_tf_resource(ctx, 'aws_instance.host')
    hosts_to_add = int(number)
    hosts = current_hosts + hosts_to_add

    rancher.wait_for_server(ctx)

    url, image = rancher.get_agent_registration_data(ctx)

    action = 'apply'
    _terraform(ctx, action, hosts=hosts, agent_registration_url=url, rancher_agent_image=image)

# Broke after adding host user_data template
# @task
# def remove_hosts(ctx, number):
#     current_hosts = _count_tf_resource(ctx, 'aws_instance.host')
#     hosts_to_remove = int(number)
#     hosts = current_hosts - hosts_to_remove
#     if hosts < 0:
#         hosts = 0
#     action = 'apply'
#     _terraform(ctx, action, hosts=hosts)


@task
def plan(ctx):
    action = 'plan'
    _terraform(ctx, action)


@task
def recreate(ctx, hosts=None, servers=None):
    if hosts is None:
        current_hosts = _count_tf_resource(ctx, 'aws_instance.host')
        hosts = current_hosts

    if servers is None:
        current_servers = _count_tf_resource(ctx, 'aws_instance.server')
        servers = current_servers

    destroy(ctx)
    create(ctx, hosts=hosts, servers=servers)


# @task
# def refresh(ctx):
#     current_servers = _count_tf_resource(ctx, 'aws_instance.server')
#     current_hosts = _count_tf_resource(ctx, 'aws_instance.host')
#
#     rancher.wait_for_server(ctx)
#     url, image = rancher.get_agent_registration_data(ctx)
#     _create_hosts_cloud_config_user_data(ctx, url)
#
#     action = 'apply'
#     _terraform(ctx, action, hosts=current_hosts, servers=current_servers)


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
        count = _count_tf_resource(ctx, '.*')
    elif res_type == 'host':
        count = _count_tf_resource(ctx, 'aws_instance.host')
    elif res_type == 'server':
        count = _count_tf_resource(ctx, 'aws_instance.server')
    return count


def _count_tf_resource(ctx, resource_pattern):
    tf_state = _get_tf_state(ctx)
    resources = tf_state['modules'][0]['resources']
    matches = [key for key in resources if re.search(resource_pattern, key)]
    count = len(matches)
    return count


def _terraform(ctx,
    action,
    hosts=None, agent_registration_url=None, rancher_agent_image=None,
    servers=None
    ):

    if action == 'destroy':
        force = '-force'
    else:
        force = ''

    if hosts is None:
        current_hosts = _count_tf_resource(ctx, 'aws_instance.host')
        hosts = '-var host_count={0}'.format(current_hosts)
    else:
        hosts = '-var host_count={0}'.format(hosts)

    if agent_registration_url is None:
        url = ''
    else:
        url = '-var agent_registration_url={0}'.format(agent_registration_url)

    if rancher_agent_image is None:
        image = ''
    else:
        image = '-var rancher_agent_image={0}'.format(rancher_agent_image)

    if servers is None:
        current_servers = _count_tf_resource(ctx, 'aws_instance.server')
        servers = '-var server_count={0}'.format(current_servers)
    else:
        servers = '-var server_count={0}'.format(servers)

    tf_state_file = '-state={0}/{1}'.format(ctx.terraform.dir, ctx.terraform.state)
    tf_dir = '{0}'.format(ctx.terraform.dir)

    tf_string = 'terraform {0} {1} {2} {3} {4} {5} {6} {7}'
    tf_cmd = tf_string.format(
        action,
        hosts,
        url,
        image,
        servers,
        force,
        tf_state_file,
        tf_dir)
    result = run(tf_cmd, hide=False, warn=True)
    if result.ok:
        list(ctx)
    else:
        print("\n" + "-> " + result.command + "\n")
        print(result)
        raise exceptions.Failure(result)


def _get_server_name(ctx):
    tf_state = _get_tf_state(ctx)
    tf_cluster = tf_state['modules'][0]
    tf_server = tf_cluster['resources']['aws_route53_record.rancher']
    server_name = tf_server['primary']['attributes']['fqdn']
    return server_name


def _get_tf_state(ctx):
    tf_state_file = '{0}/{1}'.format(ctx.terraform.dir, ctx.terraform.state)
    tf_state = json.loads(open(tf_state_file).read())
    return tf_state


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
