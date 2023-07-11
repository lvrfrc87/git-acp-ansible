#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2020, Federico Olivieri (lvrfrc87@gmail.com)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


from __future__ import absolute_import, division, print_function

__metaclass__ = type


DOCUMENTATION = """
---
module: git_mactp
author:
    - "Federico Olivieri (@Federico87)"
short_description: Perform git add, commit, pull and push operations.
description:
    - Manage C(git add), C(git commit) C(git push) and C(git pull) on a git repository.
module: git_mactp
options:
    path:
        description:
            - Folder path where C(.git/) is located.
        type: path
        required: true
    message:
        description:
            - Git commit message. Same as C(git commit -m).
              Required when using C(add).
        type: str
    add:
        description:
            - List of files under C(path) to be staged. Same as C(git add .).
              File globs not accepted, such as C(./*) or C(*).
              Required when using C(message).
        type: list
        elements: str
        default: ["."]
    branch:
        description:
            - Git branch where perform git push.
        type: str
        default: main
    merge:
        description:
            - Name of the branch that should be merged into the current branch. Perform merge from given branch into current branch. 
        type: str
        version_added: "3.0.0"
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
    tag:
        description:
            - Name of the git tag. Tag the current state of the branch.
        type: str
        version_added: "3.0.0"
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
- name: ADD FILE-1 VIA HTTPS.
  environment:
    GIT_AUTHOR_NAME: "me"
    GIT_AUTHOR_EMAIL: "me@me.me"
    GIT_COMMITTER_NAME: "me"
    GIT_COMMITTER_EMAIL: "me@me.me"
  git_mactp:
    path: "{{ working_dir }}"
    branch: "master"
    message: "Add {{ file1 }}."
    add: [ "." ]
    url: "{{ https_repo }}"

- name: PUSH REMOVE FILE-1 VIA HTTPS + FORCE.
  environment:
    GIT_AUTHOR_NAME: "me"
    GIT_AUTHOR_EMAIL: "me@me.me"
    GIT_COMMITTER_NAME: "me"
    GIT_COMMITTER_EMAIL: "me@me.me"
  git_mactp:
    path: "{{ working_dir }}"
    branch: "master"
    message: "Remove {{ file1 }}."
    add: [ "." ]
    url: "{{ https_repo }}"
    push_force: true

- name: PULL BEFORE TO PUSH.
  environment:
    GIT_AUTHOR_NAME: "me"
    GIT_AUTHOR_EMAIL: "me@me.me"
    GIT_COMMITTER_NAME: "me"
    GIT_COMMITTER_EMAIL: "me@me.me"
  git_mactp:
    message: "Pull before to push."
    path: "{{ _pull_dest.path }}"
    url: "{{ _pull_src.path }}"
    pull: true

- name: ADD FILES ONLY. - NO PUSH
  environment:
    GIT_AUTHOR_NAME: "me"
    GIT_AUTHOR_EMAIL: "me@me.me"
    GIT_COMMITTER_NAME: "me"
    GIT_COMMITTER_EMAIL: "me@me.me"
  git_mactp:
    add:
      - "{{ item }}"
    branch: "master"
    message: "Add {{ item }}"
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
  git_mactp:
    branch: "master"
    path: "{{ working_dir }}"
    url: "{{ https_repo }}"
    message: "Add {{ file4 }}"

- name: PUSH VIA SSH AND CCEPT_HOSTKEY WHEN SSH DOES NOT SUPPORT THE OPTION
  environment:
    GIT_AUTHOR_NAME: me
    GIT_AUTHOR_EMAIL: me@me.me
    GIT_COMMITTER_NAME: me
    GIT_COMMITTER_EMAIL: me@me.me
  git_mactp:
    url: "{{ ssh_repo }}"
    path: "{{ working_dir }}"
    branch: "master"
    message: "Remove {{ file2 }}"
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
from ansible_collections.studyly.git.plugins.module_utils.git_actions import Git

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
        # Path to local repo
        path=dict(required=True, type="path"),
        executable=dict(default=None, type="path"),
        message=dict(default=None, type="str"),
        add=dict(default=None, type="list", elements="str"),
        ssh_params=dict(default=None, type="dict", required=False),
        # Name of working branch
        branch=dict(default=None),
        merge=dict(default=None, type="str"),
        merge_options=dict(default=None, type="list", elements="str"),
        pull=dict(default=False, type="bool"),
        pull_options=dict(default=["--no-edit"], type="list", elements="str"),
        push=dict(default=True, type="bool"),
        push_option=dict(default=None, type="str"),
        push_force=dict(default=False, type="bool"),
        # Name of tag
        tag=dict(default=None, type="str"),
        url=dict(required=True, no_log=True),
    )

    module = AnsibleModule(
        argument_spec=argument_spec,
        required_together=[("tag", "branch")],
        required_one_of=[("add", "pull", "push", "tag", "branch", "merge")],
        mutually_exclusive=["add", "tag", "merge"]
    )

    add = module.params.get("add")
    url = module.params.get("url")
    merge = module.params.get("merge")
    pull = module.params.get("pull")
    push = module.params.get("push")
    branch = module.params.get("branch")
    ssh_params = module.params.get("ssh_params")
    tag = module.params.get("tag")

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
    # checkout branch if parameter was given
    if branch:
        git.checkout()

    if pull:
        result.update(git.pull())
    
    changed_files = git.status()

    if merge:
        result.update(git.merge())
    elif changed_files and add:
        git.add()
        result.update(git.commit())
    elif tag:
        result.update(git.tag())
    else:
        push = False

    if push:
        result.update(git.push())

    result["changed"] = False

    for d in result:
        if type(d) == dict:
            if "changed" in d:
                if d["changed"]:
                    result["changed"] = True
                    break
         

    module.exit_json(**result)


if __name__ == "__main__":
    main()
