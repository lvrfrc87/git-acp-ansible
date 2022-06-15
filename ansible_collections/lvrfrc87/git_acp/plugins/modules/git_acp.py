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
short_description: Perform git add, commit and push operations. Set git config user name and email.
description:
    - Manage C(git add), C(git commit) C(git push), C(git config) user name and email on a local
      or remote git repository.
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
        type: str
        default: main
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
    ssh_params:
        description:
            - Dictionary containing SSH parameters.
        type: dict
        suboptions:
            key_file:
                description:
                    - Specify an optional private key file path, on the target host, to use for the checkout.
            accept_hostkey:
                description:
                    - If C(yes), ensure that "-o StrictHostKeyChecking=no" is
                      present as an ssh option.
                type: bool
                default: 'no'
            ssh_opts:
                description:
                    - Creates a wrapper script and exports the path as GIT_SSH
                      which git then automatically uses to override ssh arguments.
                      An example value could be "-o StrictHostKeyChecking=no"
                      (although this particular option is better set via
                      C(accept_hostkey)).
                type: str
                default: None
        version_added: "1.4.0"
    executable:
        description:
            - Path to git executable to use. If not supplied,
              the normal mechanism for resolving binary paths will be used.
        type: path
        version_added: "1.4.0"
    remote:
        description:
            - Local system alias for git remote PUSH and PULL repository operations.
        type: str
        default: origin
    user_name:
        description:
            - Explicit git local user name. Nice to have for remote operations.
        type: str
    user_email:
        description:
            - Explicit git local email address. Nice to have for remote operations.
        type: str

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
    remote: dev_test
    mode: ssh
    url: "git@gitlab.com:networkAutomation/git_test_module.git"
    user_name: lvrfrc87
    user_email: lvrfrc87@gmail.com

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
from ansible_collections.lvrfrc87.git_acp.plugins.module_utils.git_actions import Git
from ansible_collections.lvrfrc87.git_acp.plugins.module_utils.git_configuration import GitConfiguration


def main():
    """
    Code entrypoint.

    args: none
    return:
        * result:
            type: dict()
            desription: returned output from git commands and updated changed status.
    """
    argument_spec = dict(
        path=dict(required=True, type='path'),
        executable=dict(default=None, type='path'),
        comment=dict(required=True),
        add=dict(type='list', elements='str', default=['.']),
        user=dict(),
        token=dict(no_log=True),
        ssh_params=dict(default=None, type='dict', required=False),
        branch=dict(default='main'),
        push_option=dict(default=None, type='str'),
        mode=dict(choices=['ssh', 'https', 'local'], default='ssh'),
        url=dict(required=True),
        remote=dict(default='origin'),
        user_name=dict(),
        user_email=dict()
    )

    required_if = [
        ('mode', 'https', ['user', 'token']),
    ]

    required_together = [
        ['user_name', 'user_email'],
    ]

    module = AnsibleModule(
        argument_spec=argument_spec,
        required_if=required_if,
        required_together=required_together,
    )

    url = module.params.get('url')
    push_option = module.params.get('push_option')
    mode = module.params.get('mode')
    user_name = module.params.get('user_name')
    user_email = module.params.get('user_email')
    ssh_params = module.params.get('ssh_params')

    # We screenscrape a huge amount of git commands so use C
    # locale anytime we call run_command()
    module.run_command_environ_update = dict(LANG='C', LC_ALL='C', LC_MESSAGES='C', LC_CTYPE='C')

    if mode == 'local':
        if url.startswith(('https://', 'git', 'ssh://git')):
            module.fail_json(msg='SSH or HTTPS mode selected but repo is "local')

        if push_option:
            module.fail_json(msg='"--push-option" not supported with mode "local"')

        if ssh_params:
            module.warn(msg='SSH Parameters will be ignored as mode "local"')

    elif mode == 'https':
        if not url.startswith('https://'):
            module.fail_json(msg='HTTPS mode selected but url (' + url + ') not starting with "https"')
        if ssh_params:
            module.warn(msg='SSH Parameters will be ignored as mode "https"')

    elif mode == 'ssh':
        if not url.startswith(('git', 'ssh://git')):
            module.fail_json(
                msg='SSH mode selected but url (' + url + ') not starting with "git" or "ssh://git"'
            )

        if url.startswith('ssh://git@github.com'):
            module.fail_json(msg='GitHub does not support "ssh://" URL. Please remove it from url')

    result = dict(changed=False)

    git = Git(module)

    if user_name and user_email:
        result.update(GitConfiguration(module).user_config())

    changed_files = git.status()

    if changed_files:
        git.add()
        result.update(git.commit())
        result.update(git.push())

    module.exit_json(**result)


if __name__ == "__main__":
    main()
