#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2020, Federico Olivieri (lvrfrc87@gmail.com)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


from __future__ import absolute_import, division, print_function

__metaclass__ = type


DOCUMENTATION = """
---
module: git_acp
author:
    - "Federico Olivieri (@Federico87)"
short_description: Perform git add, commit, pull and push operations. Set git config user name and email.
description:
    - Manage C(git add), C(git commit) C(git push), C(git pull), C(git config) user name and email on a local
      or remote git repository.
options:
    path:
        description:
            - Folder path where C(.git/) is located.
        type: path
        required: true
    comment:
        description:
            - Git commit comment. Same as C(git commit -m).
              Required when using add.
        type: str
    add:
        description:
            - List of files under C(path) to be staged. Same as C(git add .).
              File globs not accepted, such as C(./*) or C(*).
              Required when using comment.
        type: list
        elements: str
        default: None
    branch:
        description:
            - Git branch where perform git push.
        type: str
        default: main
    pull:
        description:
            - Perform a git pull before pushing.
        type: bool
        default: False
    pull_options:
        description:
            - Options added to the pull command. See C(git pull --help) for available
              options.
        type: list
        elements: str
        default: ['--no-edit']
    push:
        description:
            - Perform a git push.
        type: bool
        default: True
    push_option:
        description:
            - Git push options. Same as C(git --push-option=option).
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
                default: False
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
requirements:
    - git>=2.10.0 (the command line tool)
"""

EXAMPLES = """
- name: HTTPS | add file1.
  git_acp:
    path: "/Users/git/git_acp"
    comment: "Add file1."
    add: [ "." ]
    url: "https://Federico87:mytoken@gitlab.com/networkAutomation/git_test_module.git"

- name: SSH | add file2.
  git_acp:
    path: "/Users/git/git_acp"
    branch: development
    comment: Add file2.
    add: [ "file2" ]
    url: "git@gitlab.com:networkAutomation/git_test_module.git dev_test"

- name: LOCAL | push on local repo.
  git_acp:
    path: "~/test_directory/repo"
    comment: Add file3.
    add: [ "file3" ]
    url: /Users/federicoolivieri/test_directory/repo.git

- name: SSH | pull before to push.
  git_acp:
    add: [ "c.txt" ]
    comment: "commit 3"
    path: "~/test_directory/repo"
    pull: true
    url: "git@gitlab.com:networkAutomation/git_test_module.git automation"
    ssh_params:
        accept_hostkey: true
        key_file: "{{ github_ssh_private_key }}"
        ssh_opts: "-o UserKnownHostsFile={{ remote_tmp_dir }}/known_hosts"
"""

RETURN = """
output:
    description: list of git cli commands stdout
    type: list
    returned: always
    sample: [
        "[master 99830f4] Remove [ test.txt, tax.txt ]\n 4 files changed, 26 insertions(+)..."
    ]
"""

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.lvrfrc87.git_acp.plugins.module_utils.git_actions import Git


def main():
    """
    Code entrypoint.

    args: none
    return:
        * result:
            type: dict()
            description: returned output from git commands and updated changed status.
    """
    argument_spec = dict(
        path=dict(required=True, type="path"),
        executable=dict(default=None, type="path"),
        comment=dict(default=None, type="str"),
        add=dict(default=None, type="list", elements="str"),
        ssh_params=dict(default=None, type="dict", required=False),
        branch=dict(default="main"),
        pull=dict(default=False, type="bool"),
        pull_options=dict(default=["--no-edit"], type="list", elements="str"),
        push=dict(default=True, type="bool"),
        push_option=dict(default=None, type="str"),
        url=dict(required=True, no_log=True),
    )

    module = AnsibleModule(
        argument_spec=argument_spec,
        required_together=[("comment", "add")],
        required_one_of=[("add", "pull", "push")]
    )

    url = module.params.get("url")
    add = module.params.get("add")
    pull = module.params.get("pull")
    push = module.params.get("push")
    ssh_params = module.params.get("ssh_params")

    module.run_command_environ_update = dict(
        LANG="C.UTF-8", LC_ALL="C.UTF-8", LC_MESSAGES="C.UTF-8", LC_CTYPE="C.UTF-8"
    )
    result = dict(changed=False)

    if url.startswith("https://"):
        if ssh_params:
            module.warn('SSH Parameters will be ignored as "https" in url')

    if url.startswith(("git", "ssh://git")):
        if url.startswith("ssh://git@github.com"):
            module.fail_json(
                msg='GitHub does not support "ssh://" URL. Please remove it from url'
            )

    git = Git(module)
    changed_files = git.status()

    if changed_files:
        if pull:
            result.update(git.pull())
        if add:
            git.add()
            result.update(git.commit())
        if push:
            result.update(git.push())
        result["changed"] = True

    module.exit_json(**result)


if __name__ == "__main__":
    main()
