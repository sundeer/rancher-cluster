from invoke import ctask as task
from invoke import run, exceptions
import json
import re


def destroy(ctx):
    command = 'destroy'
    opts_list = ['-force']
    run_terraform(ctx, command, opts_list)


def apply(ctx,
    hosts=None, agent_registration_url=None, rancher_agent_image=None, env=None,
    servers=None,
    target=None
    ):

    opts_list = []

    if hosts is not None:
        option = '-var host_count={0}'.format(hosts)
        opts_list.append(option)
    else:
        current_hosts = count_resource(ctx, 'aws_instance.host')
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
        current_servers = count_resource(ctx, 'aws_instance.server')
        option = '-var server_count={0}'.format(current_servers)
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


def count_resource(ctx, resource_pattern):
    tf_state = get_state(ctx)
    resources = tf_state['modules'][0]['resources']
    matches = [key for key in resources if re.search(resource_pattern, key)]
    count = len(matches)
    return count


def get_state(ctx):
    tf_state_file = '{0}/{1}'.format(ctx.terraform.dir, ctx.terraform.state)
    tf_state = json.loads(open(tf_state_file).read())
    return tf_state


def count_current_resource(ctx, res_type='any'):
    if res_type == 'any':
        count = count_resource(ctx, '.*')
    elif res_type == 'host':
        count = count_resource(ctx, 'aws_instance.host')
    elif res_type == 'server':
        count = count_resource(ctx, 'aws_instance.server')
    return count
