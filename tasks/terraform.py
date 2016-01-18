from invoke import ctask as task
from invoke import run, exceptions
import json


def destroy(ctx, targets=None):
    opts_list = []

    option = '-force'
    opts_list.append(option)

    if targets is not None:
        for target in targets:
            option = '-target={0}'.format(target)
            opts_list.append(option)

    run_terraform(ctx, 'destroy', opts_list)


def apply(ctx,
    hosts=None, agent_registration_url=None, rancher_agent_image=None, env=None,
    servers=None,
    instance_type=None,
    target=None
    ):

    opts_list = []

    if hosts is not None:
        option = '-var host_count={0}'.format(hosts)
        opts_list.append(option)
    else:
        current_hosts = count_resource(ctx, 'host')
        option = '-var host_count={0}'.format(current_hosts)
        opts_list.append(option)

    if agent_registration_url is not None:
        option = '-var agent_registration_url={0}'.format(agent_registration_url)
        opts_list.append(option)

    if rancher_agent_image is not None:
        option = '-var rancher_agent_image={0}'.format(rancher_agent_image)
        opts_list.append(option)

    if env is not None:
        option = '-var rancher_environment={0}'.format(env)
        opts_list.append(option)

    if servers is not None:
        option = '-var server_count={0}'.format(servers)
        opts_list.append(option)
    else:
        current_servers = count_resource(ctx, 'server')
        option = '-var server_count={0}'.format(current_servers)
        opts_list.append(option)

    if instance_type is not None:
        option = '-var aws_instance_type={0}'.format(instance_type)
        opts_list.append(option)

    if target is not None:
        option = '-target={0}'.format(target)
        opts_list.append(option)

    run_terraform(ctx, 'apply', opts_list)


def run_terraform(ctx, command, opts_list):
    # Add state file location option
    tf_state_file = '{0}/{1}'.format(ctx.terraform.dir, ctx.terraform.state)
    option = '-state={0}'.format(tf_state_file)
    opts_list.append(option)

    # Build terraform command
    opts = ' '.join(opts_list)
    tf_dir = ctx.terraform.dir
    terraform = 'terraform {0} {1} {2}'.format(command, opts, tf_dir)

    result = run(terraform, hide=False, warn=True)
    if result.ok:
        list(ctx)
    else:
        print("\n" + "-> " + result.command + "\n")
        print(result)
        raise exceptions.Failure(result)


def get_resources(ctx, pattern):
    '''Finds all current terraform resources whose name matches pattern'''
    tf_state = get_state(ctx)
    resources = tf_state['modules'][0]['resources']
    matches = {k:v for k, v in resources.items() if pattern in k}
    return matches


def get_state(ctx):
    tf_state_file = '{0}/{1}'.format(ctx.terraform.dir, ctx.terraform.state)
    tf_state = json.loads(open(tf_state_file).read())
    return tf_state


def count_resource(ctx, res_type='any'):
    if res_type == 'any':
        resources = get_resources(ctx, '')
    elif res_type == 'host':
        resources = get_resources(ctx, 'aws_instance.host')
    elif res_type == 'server':
        resources = get_resources(ctx, 'aws_instance.server')
    return len(resources)


@task
def get_hosts_by_environment(ctx, env):
    hosts = get_resources(ctx, 'aws_instance.host')

    matches = [k for k in hosts if hosts[k]['primary']['attributes']['tags.environment'] == env]
    return matches
