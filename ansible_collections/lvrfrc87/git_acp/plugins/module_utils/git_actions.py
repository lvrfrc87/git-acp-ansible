from __future__ import absolute_import, division, print_function
__metaclass__ = type

from ansible_collections.lvrfrc87.git_acp.plugins.module_utils.messages import FailingMessage


class Git:

    def __init__(self, module):
        self.module = module

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
        command = ['git', 'add', '--']

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
        command = ['git', 'status', '--porcelain']

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
        command = ['git', 'commit', '-m', comment]

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

        command = ['git', 'push', origin, branch]

        def set_url():
            """
            Set URL and remote if required.

            args:
                * module:
                    type: dict()
                    descrition: Ansible basic module utilities and module arguments.
            return: null
            """
            command = ['git', 'remote', 'get-url', '--all', origin]
            path = self.module.params['path']

            rc, _output, _error = self.module.run_command(command, cwd=path)

            if rc == 0:
                return

            if rc == 128:
                if mode == 'https':
                    if url.startswith('https://'):
                        command = [
                            'git',
                            'remote',
                            'add',
                            origin,
                            'https://{0}:{1}@{2}'.format(user, token, url[8:])
                        ]
                    else:
                        self.module.fail_json(msg='HTTPS mode selected but not HTTPS URL provided')
                else:
                    command = ['git', 'remote', 'add', origin, url]

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
