from __future__ import absolute_import, division, print_function

__metaclass__ = type

import os
import stat
import tempfile

from ansible_collections.lvrfrc87.git_acp.plugins.module_utils.messages import (
    FailingMessage,
)
from ansible.module_utils.six import b


class Git:
    def __init__(self, module):
        self.module = module
        self.url = module.params["url"]
        self.path = module.params["path"]
        self.git_path = module.params["executable"] or module.get_bin_path(
            "git", True
        )

        ssh_args = {
            "ssh_key_file": None,
            "ssh_opts": None,
            "ssh_accept_hostkey": False,
            "ssh_params": module.params["ssh_params"] or None
        }

        if ssh_args["ssh_params"]:

            ssh_args["ssh_key_file"] = (
                ssh_args["ssh_params"]["key_file"] if "key_file" in ssh_args["ssh_params"] else None
            )
            self.ssh_opts = ssh_args["ssh_params"]["ssh_opts"] if "ssh_opts" in ssh_args["ssh_params"] else None
            self.ssh_accept_hostkey = (
                ssh_args["ssh_params"]["accept_hostkey"]
                if "accept_hostkey" in ssh_args["ssh_params"]
                else False
            )

            if ssh_args["ssh_accept_hostkey"]:
                if ssh_args["ssh_opts"] is not None:
                    if "-o StrictHostKeyChecking=no" not in ssh_args["ssh_opts"]:
                        ssh_args["ssh_opts"] += " -o StrictHostKeyChecking=no"
                else:
                    ssh_args["ssh_opts"] = "-o StrictHostKeyChecking=no"

        self.ssh_wrapper = self.write_ssh_wrapper(module.tmpdir)
        self.set_git_ssh(self.ssh_wrapper, ssh_args["ssh_key_file"], ssh_args["ssh_opts"])
        module.add_cleanup_file(path=self.ssh_wrapper)

    # ref: https://github.com/ansible/ansible/blob/05b90ab69a3b023aa44b812c636bb2c48e30108e/lib/ansible/modules/git.py#L368
    def write_ssh_wrapper(self, module_tmpdir):
        try:
            # make sure we have full permission to the module_dir, which
            # may not be the case if we're sudo'ing to a non-root user
            if os.access(module_tmpdir, os.W_OK | os.R_OK | os.X_OK):
                fd, wrapper_path = tempfile.mkstemp(prefix=module_tmpdir + "/")
            else:
                raise OSError
        except (IOError, OSError):
            fd, wrapper_path = tempfile.mkstemp()

        fh = os.fdopen(fd, "w+b")
        template = b(
            """#!/bin/sh
if [ -z "$GIT_SSH_OPTS" ]; then
    BASEOPTS=""
else
    BASEOPTS=$GIT_SSH_OPTS
fi

# Let ssh fail rather than prompt
BASEOPTS="$BASEOPTS -o BatchMode=yes"

if [ -z "$GIT_KEY" ]; then
    ssh $BASEOPTS "$@"
else
    ssh -i "$GIT_KEY" -o IdentitiesOnly=yes $BASEOPTS "$@"
fi
"""
        )
        fh.write(template)
        fh.close()
        st = os.stat(wrapper_path)
        os.chmod(wrapper_path, st.st_mode | stat.S_IEXEC)
        return wrapper_path

    # ref: https://github.com/ansible/ansible/blob/05b90ab69a3b023aa44b812c636bb2c48e30108e/lib/ansible/modules/git.py#L402
    def set_git_ssh(self, ssh_wrapper, key_file, ssh_opts):

        if os.environ.get("GIT_SSH"):
            del os.environ["GIT_SSH"]
        os.environ["GIT_SSH"] = ssh_wrapper

        if os.environ.get("GIT_KEY"):
            del os.environ["GIT_KEY"]

        if key_file:
            os.environ["GIT_KEY"] = key_file

        if os.environ.get("GIT_SSH_OPTS"):
            del os.environ["GIT_SSH_OPTS"]

        if ssh_opts:
            os.environ["GIT_SSH_OPTS"] = ssh_opts

    def add(self):
        """
        Run git add and stage changed files.

        args:
            * module:
                type: dict()
                descrition: Ansible basic module utilities and module arguments.

        return: null
        """

        add = self.module.params["add"]
        command = [self.git_path, "add", "--"]

        command.extend(add)

        rc, output, error = self.module.run_command(command, cwd=self.path)

        if rc == 0:
            return

        FailingMessage(self.module, rc, command, output, error)

    def status(self):
        """
        Run git status and check if repo has changes.

        args:
            * module:
                type: dict()
                descrition: Ansible basic module utilities and module arguments.
        return:
            * data:
                type: set()
                description: list of files changed in repo.
        """
        data = set()
        command = [self.git_path, "status", "--porcelain"]

        rc, output, error = self.module.run_command(command, cwd=self.path)

        if rc == 0:
            for line in output.split("\n"):
                file_name = line.split(" ")[-1].strip()
                if file_name:
                    data.add(file_name)
            return data

        else:
            FailingMessage(self.module, rc, command, output, error)

    def commit(self):
        """
        Run git commit and commit files in repo.

        args:
            * module:
                type: dict()
                descrition: Ansible basic module utilities and module arguments.
        return:
            * result:
                type: dict()
                desription: returned output from git commit command and changed status
        """
        comment = self.module.params["comment"]
        command = [self.git_path, "commit", "-m", comment]

        rc, output, error = self.module.run_command(command, cwd=self.path)

        if rc == 0:
            return {
                "git_commit": {"output": output, "error": error, "changed": True}
            }
        FailingMessage(self.module, rc, command, output, error)

    def pull(self):
        """
        Get git changes from upstream before pushing.

        args:
            * url:
                type: str()
                descrition: git url of the git repo.
            * branch:
                type: str()
                descrition: git branch of the git repo.
            * pull_options:
                type: list()
                desription: pull options added to the pull command.
        return:
            * result:
                type: dict()
                descrition: returned output from git pull command.
        """
        url = self.module.params["url"]
        branch = self.module.params["branch"]
        command = [
            self.git_path,
            "-C",
            self.path,
            "pull",
            url,
            branch,
        ] + self.module.params["pull_options"]
        rc, output, error = self.module.run_command(command)
        if rc == 0:
            return {
                "git_pull": {"output": output, "error": error, "changed": True}
            }
        FailingMessage(self.module, rc, command, output, error)

    def push(self):
        """
        Push changes to remote repo.

        args:
            * path:
                type: path
                descrition: git repo local path.
            * cmd_push:
                type: list()
                descrition: list of commands to perform git push operation.
        return:
            * result:
                type: dict()
                desription: returned output from git push command and updated changed status.
        """
        url = self.module.params["url"]
        branch = self.module.params["branch"]
        push_option = self.module.params.get("push_option")
        command = [self.git_path, "push", url, branch]

        if push_option:
            command.insert(3, "--push-option={0} ".format(push_option))

        rc, output, error = self.module.run_command(command, cwd=self.path)

        if rc == 0:
            return {
                "git_push": {"output": str(output), "error": str(error), "changed": True}
            }
        FailingMessage(self.module, rc, command, output, error)
