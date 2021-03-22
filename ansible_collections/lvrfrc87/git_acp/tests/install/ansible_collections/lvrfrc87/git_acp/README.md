Module documentation can be found [here](../../../README.md)

### HOW INSTALL COLLECTION

- Locally using `tar` file: `ansible-galaxy collection install lvrfrc87-git_acp-1.1.tar.gz`

- From GitHub: `ansible-galaxy collection install git+https://github.com/lvrfrc87/git-acp-ansible.git#ansible_collections/lvrfrc87/git_acp,master`

- From [Ansible Galaxy](https://galaxy.ansible.com/): `ansible-galaxy collection install lvrfrc87.git_acp`

[Here](https://docs.ansible.com/ansible/latest/galaxy/user_guide.html#installing-a-collection-from-galaxy) more info regarding collection installation.

### HOW TO USE COLLECTION

```
---
- hosts: localhost
  gather_facts: false
  collections:
    - lvrfrc87.git_acp

  tasks:
    - name: 10005 - SETUP | https loca repo ahead.
      register: result
      git_acp:
        user: "{{ user }}"
        token: "{{ token }}"
        path: "{{ working_dir }}"
        branch: master
        add: ["."]
        comment: Local repo ahead
        mode: https
        url: "https://gitlab.com/networkAutomation/git_test_module.git"
```
