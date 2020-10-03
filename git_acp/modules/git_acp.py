#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2020, Federico Olivieri (lvrfrc87@gmail.com)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = '''
---
module: git_acp
author:
    - "Federico Olivieri (@Federico87)"
short_description: Perform git add, commit and push operations.
description:
    - Manage C(git add), C(git commit) and C(git push) on a local
      or remote git repositroy.
options:
    path:
        description:
            - Folder path where C(.git/) is located.
        required: true
        type: path
    comment:
        description:
            - Git commit comment. Same as C(git commit -m).
        type: str
        required: true
    add:
        description:
            - List of files under C(path) to be staged. Same as C(git add .).
              File globs not accepted, such as C(./*) or C(*).
        type: list
        elements: str
        required: true
        default: ["."]
    user:
        description:
            - Git username for https operations.
        type: str
    token:
        description:
            - Git API token for https operations.
        type: str
    branch:
        description:
            - Git branch where perform git push.
        required: True
        type: str
    push_option:
        description:
            - Git push options. Same as C(git --push-option=option).
        type: str
    mode:
        description:
            - Git operations are performend eithr over ssh, https or local.
              Same as C(git@git...) or C(https://user:token@git...).
        choices: ['ssh', 'https', 'local']
        default: ssh
        type: str
    url:
        description:
            - Git repo URL.
        required: True
        type: str
    remote:
        description:
            - Local system alias for git remote PUSH and PULL repository operations.
        type: str
        default: origin
requirements:
    - git>=2.10.0 (the command line tool)
'''

EXAMPLES = '''
- name: HTTPS | add file1.
  git_acp:
    user: Federico87
    token: mytoken
    path: /Users/git/git_acp
    branch: master
    comment: Add file1.
    remote: origin
    add: [ "." ]
    mode: https
    url: "https://gitlab.com/networkAutomation/git_test_module.git"

- name: SSH | add file1.
  git_acp:
    path: /Users/git/git_acp
    branch: master
    comment: Add file1.
    add: [ file1  ]
    mode: ssh
    url: "git@gitlab.com:networkAutomation/git_test_module.git"

- name: LOCAL | push on local repo.
  git_acp:
    path: "~/test_directory/repo"
    branch: master
    comment: Add file1.
    add: [ file1 ]
    mode: local
    url: /Users/federicoolivieri/test_directory/repo.git
'''

RETURN = '''
output:
    description: list of git cli command stdout
    type: list
    returned: always
    sample: [
        "[master 99830f4] Remove [ test.txt, tax.txt ]\n 4 files changed, 26 insertions(+)..."
    ]
'''

from ansible.module_utils.basic import AnsibleModule


def git_add(module):
    """
    Run git add and stage changed files.

    args:
        * module:
            type: dict()
            descrition: Ansible basic module utilities and module arguments.
    return:
        * return: 
            type: null
    """
    add = module.params.get('add')
    path = module.params.get('path')

    add_cmds = [
        'git',
        'add',
        '--',
    ]
    add_cmds.extend(add)

    rc, _output, error = module.run_command(add_cmds, cwd=path)

    if rc != 0:
        module.fail_json(rc=rc, msg=error, command=' '.join(add_cmds))
    if rc == 0:
        return


def git_status(module):
    """
    Run git status and check if repo has changes.

    args:
        * module:
            type: dict()
            descrition: Ansible basic module utilities and module arguments.
    return:
        * data: 
            type: set()
            description: list of files changed in repo.
    """
    data = set()
    path = module.params.get('path')
    status_cmds = [
        'git',
        'status',
        '--porcelain',
    ]

    rc, output, error = module.run_command(status_cmds, cwd=path)

    if rc != 0:
        module.fail_json(rc=rc, msg=error, command=' '.join(status_cmds))
    if rc == 0:
        for line in output.split('\n'):
            file_name = line.split(' ')[-1].strip()
            if file_name:
                data.add(file_name)
    return data


def git_commit(module):
    """
    Run git commit and commit files in repo.

    args:
        * module:
            type: dict()
            descrition: Ansible basic module utilities and module arguments.
    return:
        * result: 
            type: dict()
            desription: returned output from git commit command and changed status
    """
    result = dict()
    comment = module.params.get('comment')
    path = module.params.get('path')

    if comment:
        git_add(module)

        commit_cmds = [
            'git',
            'commit',
            '-m',
            comment,
        ]

    rc, output, error = module.run_command(commit_cmds, cwd=path)

    if rc != 0:
        module.fail_json(rc=rc, msg=error, command=' '.join(commit_cmds))
    if rc == 0:
        if output:
            result.update(
                git_commit=output,
                changed=True
            )
            return result


def git_push(module):

    def git_set_url(module):

        url = module.params.get('url')
        mode = module.params.get('mode')
        user = module.params.get('user')
        token = module.params.get('token')
        origin = module.params.get('remote')

        git_get_url = [
            'git',
            'remote',
            'get-url',
            '--all',
            origin,
        ]
        
        path = module.params.get('path')

        rc, _output, _error = module.run_command(git_get_url, cwd=path)

        if rc == 0:
            return
        
        if rc == 128:
            if mode == 'https':
                if url.startswith('https://'):
                    remote_add = [
                        'git',
                        'remote',
                        'add',
                        origin,
                        'https://{user}:{token}@{url}'.format(
                            url=url[8:],
                            user=user,
                            token=token,
                        ),
                    ]
                else:
                    module.fail_json(msg='HTTPS mode selected but not HTTPS URL provided')
            else:
                remote_add = [
                    'git',
                    'remote',
                    'add',
                    origin,
                    url,
                ]

            rc, _output, error = module.run_command(remote_add, cwd=path)

            if rc != 0:
                module.fail_json(msg=error, command=' '.join(remote_add), rc=rc)
            if rc == 0:
                return


    def git_push_cmd(path, cmd_push):
        result = dict(changed=False)

        rc, output, error = module.run_command(cmd_push, cwd=path)

        if rc != 0:
            module.fail_json(msg=str(error) + str(output))
        if rc == 0:
            result.update(
                git_push=str(error) + str(output),
                changed=True
            )
            return result

    branch = module.params.get('branch')
    push_option = module.params.get('push_option')
    path = module.params.get('path')
    origin = module.params.get('remote')

    cmd_push = [
        'git',
        'push',
        origin,
        branch,
    ]

    if not push_option:
        git_set_url(module)
        return git_push_cmd(path, cmd_push)

    if push_option:
        cmd_push.insert(3, '--push-option={0} '.format(push_option))
        git_set_url(module)
        return git_push_cmd(path, cmd_push)


def main():

    argument_spec = dict(
        path=dict(required=True, type="path"),
        comment=dict(required=True),
        add=dict(type='list', elements='str', default=["."]),
        user=dict(),
        token=dict(no_log=True),
        branch=dict(required=True),
        push_option=dict(),
        mode=dict(choices=["ssh", "https", "local"], default='ssh'),
        url=dict(required=True),
        remote=dict(default="origin"),
    )

    required_if = [
        ("mode", "https", ["user", "token"]),
    ]

    module = AnsibleModule(
        argument_spec=argument_spec,
        required_if=required_if,
    )

    url = module.params.get('url')
    push_option = module.params.get('push_option')
    mode = module.params.get('mode')

    if mode == 'local':
        if url.startswith(('https://', 'git@', 'ssh://git@')):
            module.fail_json(msg='SSH or HTTPS mode selected but repo is LOCAL')

        if push_option:
            module.fail_json(msg='"--push-option" not supported with mode "local"')

    if mode == 'https':
        if not url.startswith('https://'):
            module.fail_json(msg='HTTPS mode selected but url ('+url+') is not HTTPS')

    if mode == 'ssh':
        if not url.startswith(('git@', 'ssh://git@')):
            module.fail_json(msg='SSH mode selected but url ('+url+') not starting with git@ or ssh://git@')

        if url.startswith('ssh://git@github.com'):
            module.fail_json(msg='GitHub does not support "ssh://" URL. Please remove it from url: '+url+'')

    result = dict(changed=False)

    changed_files = git_status(module)
    if changed_files:
        result.update(git_commit(module))
        result.update(git_push(module))

    if result:
        module.exit_json(**result)


if __name__ == "__main__":
    main()
