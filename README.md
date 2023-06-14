# git-mactp-ansible

`git_mactp` is an Ansible module for `git add`, `git commit`, `git push`, `git merge`, `git tag` and `git pull` operations on local or remote (https/ssh) git repo. The module will interact with the local shell execution environment, so certain commands such as setting a new git URL will edit the local `.git/config`. This repo was forked from [lvrfrc87](https://github.com/lvrfrc87/git-acp-ansible).

### PyPi Install:

PyPi package is not longer supported (last version available is `1.1.2`). Using collection is strongly advised.
For older Ansible versions that do not support collection, you can copy `ansible_collections/studyly/git_mactp/plugins/modules/git_mactp.py` into `library` directory in the root of your Ansible project:

```
myproject/
├── ansible.cfg
├── inv/
├── library/
│   ├── git_mactp.py
├── playbooks/
├── roles/
```


### Ansible Galaxy Install (for Ansible version > 2.9)

All info related to Ansible Galaxy install are available [here](ansible_collections/studyly/git_mactp/README.md)

### Module Documentation:

```
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
```

### Examples:

```
- name: ADD FILE-1 VIA HTTPS.
  environment:
    GIT_AUTHOR_NAME: "me"
    GIT_AUTHOR_EMAIL: "me@me.me"
    GIT_COMMITTER_NAME: "me"
    GIT_COMMITTER_EMAIL: "me@me.me"
  git_mactp:
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
  git_mactp:
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
  git_mactp:
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
  git_mactp:
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
  git_mactp:
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
  git_mactp:
    url: "{{ ssh_repo }}"
    path: "{{ working_dir }}"
    branch: "master"
    comment: "Remove {{ file2 }}"
    add: [ "{{ file2 }}" ]
    ssh_params:
        accept_hostkey: true
        key_file: '{{ github_ssh_private_key }}'
        ssh_opts: '-o UserKnownHostsFile={{ remote_tmp_dir }}/known_hosts'
```

### Return Example:

```
 {
    "result": {
        "changed": true,
        "failed": false,
        "git_commit": {
            "changed": true,
            "error": "",
            "output": "[master 4596d9d] Add 1682063905033586650.txt.\n 1 file changed, 0 insertions(+), 0 deletions(-)\n create mode 100644 1682063905033586650.txt\n"
        },
        "git_push": {
            "changed": true,
            "error": "",
            "output": "remote: Resolving deltas:   0% (0/1)        \rremote: Resolving deltas: 100% (1/1)        \rremote: Resolving deltas: 100% (1/1), completed with 1 local object.        \nTo https://github.com/lvrfrc87/git-acp-test.git\n   3ba9041..4596d9d  master -> master\n"
        }
    }
}
```