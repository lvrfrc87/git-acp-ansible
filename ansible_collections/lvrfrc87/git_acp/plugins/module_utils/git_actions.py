from __future__ import absolute_import, division, print_function
__metaclass__ = type

import os
import stat
import tempfile

from ansible_collections.lvrfrc87.git_acp.plugins.module_utils.messages import FailingMessage
from ansible.module_utils.six import b


class Git:

    def __init__(self, module, git_path='git', key_file=None, ssh_opts=None):
        self.module = module
        self.git_path = git_path

        ssh_wrapper = self.write_ssh_wrapper(module.tmpdir)
        self.set_git_ssh(ssh_wrapper, key_file, ssh_opts)
        module.add_cleanup_file(path=ssh_wrapper)

    ## ref: https://github.com/ansible/ansible/blob/05b90ab69a3b023aa44b812c636bb2c48e30108e/lib/ansible/modules/git.py#L368
    def write_ssh_wrapper(self, module_tmpdir):
        try:
            # make sure we have full permission to the module_dir, which
            # may not be the case if we're sudo'ing to a non-root user
            if os.access(module_tmpdir, os.W_OK | os.R_OK | os.X_OK):
                fd, wrapper_path = tempfile.mkstemp(prefix=module_tmpdir + '/')
            else:
                raise OSError
        except (IOError, OSError):
            fd, wrapper_path = tempfile.mkstemp()

        fh = os.fdopen(fd, 'w+b')
        template = b("""#!/bin/sh
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
""")
        fh.write(template)
        fh.close()
        st = os.stat(wrapper_path)
        os.chmod(wrapper_path, st.st_mode | stat.S_IEXEC)
        return wrapper_path

    ## ref: https://github.com/ansible/ansible/blob/05b90ab69a3b023aa44b812c636bb2c48e30108e/lib/ansible/modules/git.py#L402
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

        add = self.module.params['add']
        path = self.module.params['path']
        command = [self.git_path, 'add', '--']

        command.extend(add)

        rc, output, error = self.module.run_command(command, cwd=path)

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
        path = self.module.params['path']
        command = [self.git_path, 'status', '--porcelain']

        rc, output, error = self.module.run_command(command, cwd=path)

        if rc == 0:
            for line in output.split('\n'):
                file_name = line.split(' ')[-1].strip()
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
        result = dict()
        comment = self.module.params['comment']
        path = self.module.params['path']
        command = [self.git_path, 'commit', '-m', comment]

        rc, output, error = self.module.run_command(command, cwd=path)

        if rc == 0:
            if output:
                result.update({"git_commit": output, "changed": True})
                return result
        else:
            FailingMessage(self.module, rc, command, output, error)

    def push(self):
        """
        Set URL and remote if required. Push changes to remote repo.

        args:
            * module:
                type: dict()
                descrition: Ansible basic module utilities and module arguments.
        return:
            * result:
                type: dict()
                desription: returned output from git push command and updated changed status.
        """
        url = self.module.params['url']
        mode = self.module.params['mode']
        origin = self.module.params['remote']
        branch = self.module.params['branch']
        path = self.module.params['path']
        origin = self.module.params['remote']
        push_option = self.module.params.get('push_option')
        user = self.module.params.get('user')
        token = self.module.params.get('token')

        command = [self.git_path, 'push', origin, branch]

        def set_url():
            """
            Set URL and remote if required.

            args:
                * module:
                    type: dict()
                    descrition: Ansible basic module utilities and module arguments.
            return: null
            """
            command = [self.git_path, 'remote', 'get-url', '--all', origin]
            path = self.module.params['path']

            rc, _output, _error = self.module.run_command(command, cwd=path)

            if rc == 0:
                return

            if rc == 128:
                if mode == 'https':
                    if url.startswith('https://'):
                        command = [
                            self.git_path,
                            'remote',
                            'add',
                            origin,
                            'https://{0}:{1}@{2}'.format(user, token, url[8:])
                        ]
                    else:
                        self.module.fail_json(msg='HTTPS mode selected but not HTTPS URL provided')
                else:
                    command = [self.git_path, 'remote', 'add', origin, url]

                rc, output, error = self.module.run_command(command, cwd=path)

                if rc == 0:
                    return
                else:
                    FailingMessage(self.module, rc, command, output, error)

        def push_cmd():
            """
            Set URL and remote if required. Push changes to remote repo.

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
            result = dict()

            rc, output, error = self.module.run_command(command, cwd=path)

            if rc == 0:
                result.update({"git_push": str(error) + str(output), "changed": True})
                return result
            else:
                FailingMessage(self.module, rc, command, output, error)

        if push_option:
            command.insert(3, '--push-option={0} '.format(push_option))

        set_url()

        return push_cmd()
