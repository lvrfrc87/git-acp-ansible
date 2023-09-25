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
short_description: Perform git add, commit, pull and push operations.
description:
    - Manage C(git add), C(git commit) C(git push) and C(git pull) on a git repository.
options:
    path:
        description:
            - Folder path where C(.git/) is located.
        type: path
        required: true
    comment:
        description:
            - Git commit comment. Same as C(git commit -m).
              Required when using C(add).
        type: str
    add:
        description:
            - List of files under C(path) to be staged. Same as C(git add .).
              File globs not accepted, such as C(./*) or C(*).
              Required when using C(comment).
        type: list
        elements: str
        default: ["."]
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
        version_added: "2.0.0"
    pull_options:
        description:
            - Options added to the pull command. See C(git pull --help) for available
              options.
        type: list
        elements: str
        default: ['--no-edit']
        version_added: "2.0.0"
    push:
        description:
            - Perform a git push.
        type: bool
        default: True
    push_option:
        description:
            - Git push options. Same as C(git --push-option=option).
        type: str
    push_force:
        description:
            - Git push force options. Same as C(git push --force).
        type: bool
        default: False
        version_added: "2.1.0"
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
                type: path
            accept_hostkey:
                description:
                    - If C(yes), ensure that "-o StrictHostKeyChecking=no" is
                      present as an ssh option.
                type: bool
            ssh_opts:
                description:
                    - Creates a wrapper script and exports the path as GIT_SSH
                      which git then automatically uses to override ssh arguments.
                      An example value could be "-o StrictHostKeyChecking=no"
                      (although this particular option is better set via
                      C(accept_hostkey)).
                type: str
        version_added: "1.4.0"
    executable:
        description:
            - Path to git executable to use. If not supplied,
              the normal mechanism for resolving binary paths will be used.
        type: path
        version_added: "1.4.0"
    clean:
        description:
            - If C(ignored), clean ignored files and directories in the repository.
            - If C(untracked), clean untracked files and directories in the repository.
            - If C(all), clean both ignored and untracked.
        type: str
        required: false
        choices: [ "ignored", "untracked", "all" ]
        version_added: "2.2.0"

requirements:
    - git>=2.10.0 (the command line tool)
"""

EXAMPLES = """
- name: ADD FILE-1 VIA HTTPS.
  environment:
    GIT_AUTHOR_NAME: "me"
    GIT_AUTHOR_EMAIL: "me@me.me"
    GIT_COMMITTER_NAME: "me"
    GIT_COMMITTER_EMAIL: "me@me.me"
  git_acp:
    path: "{{ working_dir }}"
    branch: "master"
    comment: "Add {{ file1 }}."
    add: [ "." ]
    url: "{{ https_repo }}"

- name: PUSH REMOVE FILE-1 VIA HTTPS + FORCE.
  environment:
    GIT_AUTHOR_NAME: "me"
    GIT_AUTHOR_EMAIL: "me@me.me"
    GIT_COMMITTER_NAME: "me"
    GIT_COMMITTER_EMAIL: "me@me.me"
  git_acp:
    path: "{{ working_dir }}"
    branch: "master"
    comment: "Remove {{ file1 }}."
    add: [ "." ]
    url: "{{ https_repo }}"
    push_force: true

- name: PULL BEFORE TO PUSH.
  environment:
    GIT_AUTHOR_NAME: "me"
    GIT_AUTHOR_EMAIL: "me@me.me"
    GIT_COMMITTER_NAME: "me"
    GIT_COMMITTER_EMAIL: "me@me.me"
  git_acp:
    comment: "Pull before to push."
    path: "{{ _pull_dest.path }}"
    url: "{{ _pull_src.path }}"
    pull: true

- name: ADD FILES ONLY. - NO PUSH
  environment:
    GIT_AUTHOR_NAME: "me"
    GIT_AUTHOR_EMAIL: "me@me.me"
    GIT_COMMITTER_NAME: "me"
    GIT_COMMITTER_EMAIL: "me@me.me"
  git_acp:
    add:
      - "{{ item }}"
    branch: "master"
    comment: "Add {{ item }}"
    path: "{{ working_dir }}"
    push: false
    url: "{{ https_repo }}"
  loop:
      - "{{ file2 }}"
      - "{{ file3 }}"

- name: 10220 - PUSH FILE-2, FILE-3 ALONG WITH FILE-4.
  environment:
    GIT_AUTHOR_NAME: "me"
    GIT_AUTHOR_EMAIL: "me@me.me"
    GIT_COMMITTER_NAME: "me"
    GIT_COMMITTER_EMAIL: "me@me.me"
  git_acp:
    branch: "master"
    path: "{{ working_dir }}"
    url: "{{ https_repo }}"
    comment: "Add {{ file4 }}"

- name: PUSH VIA SSH AND CCEPT_HOSTKEY WHEN SSH DOES NOT SUPPORT THE OPTION
  environment:
    GIT_AUTHOR_NAME: me
    GIT_AUTHOR_EMAIL: me@me.me
    GIT_COMMITTER_NAME: me
    GIT_COMMITTER_EMAIL: me@me.me
  git_acp:
    url: "{{ ssh_repo }}"
    path: "{{ working_dir }}"
    branch: "master"
    comment: "Remove {{ file2 }}"
    add: [ "{{ file2 }}" ]
    ssh_params:
        accept_hostkey: true
        key_file: '{{ github_ssh_private_key }}'
        ssh_opts: '-o UserKnownHostsFile={{ remote_tmp_dir }}/known_hosts'
"""

RETURN = """
output:
    description: dic of git cli commands stdout
    type: dict
    returned: always
    sample: {
    "result": {
        "changed": true,
        "failed": false,
        "git_commit": {
            "changed": true,
            "error": "",
            "output": "[master 4596d9d] Add 1682063905033586650.txt.\n 1 file changed, ..."
        },
        "git_push": {
            "changed": true,
            "error": "",
            "output": "remote: Resolving deltas:   0% (0/1)        \rremote: Resolving ..."
        }
    }
}
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
        add=dict(default=".", type="list", elements="str"),
        ssh_params=dict(default=None, type="dict", required=False),
        branch=dict(default="main"),
        pull=dict(default=False, type="bool"),
        pull_options=dict(default=["--no-edit"], type="list", elements="str"),
        push=dict(default=True, type="bool"),
        push_option=dict(default=None, type="str"),
        push_force=dict(default=False, type="bool"),
        url=dict(required=True, no_log=True),
        clean=dict(default=None, type='str', required=False, choices=['ignored', 'untracked', 'all']),
    )

    module = AnsibleModule(
        argument_spec=argument_spec,
        required_together=[("comment", "add")],
        required_one_of=[("add", "pull", "push")]
    )

    url = module.params.get("url")
    pull = module.params.get("pull")
    push = module.params.get("push")
    ssh_params = module.params.get("ssh_params")
    clean = module.params['clean']

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
    changed_files, untracked = git.status()

    if all([changed_files, untracked, clean]):
        result.update(git.clean())
    else:
        if pull:
            result.update(git.pull())

        git.add()

        commit_result = git.commit()
        result.update(commit_result)

        # Exit if nothing to commit
        if not commit_result["git_commit"]["changed"]:
            result.update(warnings=commit_result["git_commit"]["output"])
            module.exit_json(**result)

        if push:
            result.update(git.push())
        result["changed"] = True

    module.exit_json(**result)


if __name__ == "__main__":
    main()
