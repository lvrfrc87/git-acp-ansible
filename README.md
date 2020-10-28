# git-acp-ansible

`git_acp` is an Ansible module for `git add`, `git commit` and `git push` operations on local or remote (https/ssh) git repo.

### Install:

To install just run the command:

`pip install git-acp-ansible`

### Configure Ansible:

Edit your `ansible.cfg` file and add the path where `git_acp` module is installed.

i.e.

```
[defaults]
library = ./lib/python3.7/site-packages/git-acp-ansible/modules
```

If you run a `virtualenv` most probably the path would be something similar to the example above. 
Otherwise you can use for example `mlocate` to find where the module is.

For more info, have a look to [Ansible Docs](https://docs.ansible.com/ansible/latest/installation_guide/intro_configuration.html#library)

### Module Documentation:

```
module: git_acp
options:
    path:
        description:
            - Folder path where ".git/" is located.
        required: true
        type: path
    comment:
        description:
            - Git commit comment. Same as "git commit -m".
        type: str
        required: true
    add:
        description:
            - List of files under `path` to be staged. Same as "git add .".
              File globs not accepted, such as "./*" or "*".
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
            - Git push options. Same as "git --push-option=option".
        type: str
    mode:
        description:
            - Git operations are performend eithr over ssh, https or local.
              Same as "git@git..." or "https://user:token@git...".
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
    user_name:
        decription:
            - Explicit git local user name. Nice to have for remote operations.
        type: str
    user_email:
        decription:
            - Explicit git local email address. Nice to have for remote operations.
        type: str
```

### Examples:

```
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
```
