# git-acp-ansible`

`git_acp` is an Ansible module for `git add`, `git commit` and `git push` operations on local or remote (https/ssh) git repo.

## Install:



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
```

