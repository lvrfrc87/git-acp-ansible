# git-acp-ansible

`git_acp` is an Ansible module for `git add`, `git commit`, `git push` and `git pull` operations on local or remote (https/ssh) git repo. The module will interact with the local shell execution environment, so certain commands such as setting a new git URL will edit the local `.git/config`.

### PyPi Install:

PyPi package is not longer supported (last version available is `1.1.2`). Using collection is strongly advised.
For older Ansible versions that do not support collection, you can copy `ansible_collections/lvrfrc87/git_acp/plugins/modules/git_acp.py` into `library` directory in the root of your Ansible project:

```
myproject/
├── ansible.cfg
├── inv/
├── library/
│   ├── git_acp.py
├── playbooks/
├── roles/
```


### Ansible Galaxy Install (for Ansible version > 2.9)

All info related to Ansible Galaxy install are available [here](ansible_collections/lvrfrc87/git_acp/README.md)

### Module Documentation:

```
module: git_acp
    path:
        description:
            - Folder path where C(.git/) is located.
        type: path
        required: true
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
        version_added: "1.5.0"
    pull_options:
        description:
            - Options added to the pull command. See C(git pull --help) for available
              options.
        type: list
        elements: str
        default: ['--no-edit']
        version_added: "1.5.0"
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
```

### Examples:

```
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
```
