Module documentation can be found [here](../../../README.md)

### HOW INSTALL COLLECTION

- Locally using `tar` file: `ansible-galaxy collection install studyly-git_mactp-2.1.0.tar.gz`

- From GitHub: `ansible-galaxy collection install git@github.com:Studyly-GmbH/git-mactp-ansible.git#ansible_collections/studyly/git_mactp,master`

- From [Ansible Galaxy](https://galaxy.ansible.com/): `ansible-galaxy collection install studyly.git_mactp`

[Here](https://docs.ansible.com/ansible/latest/galaxy/user_guide.html#installing-a-collection-from-galaxy) more info regarding collection installation.

### HOW TO USE COLLECTION

```
---
- hosts: localhost
  gather_facts: false
  collections:
    - studyly.git_mactp

  tasks:
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
```
