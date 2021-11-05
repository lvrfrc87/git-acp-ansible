class GitConfiguration:

    def __init__(self, module):
        self.module = module

    def user_conifg(self):
        """
        Config git local user.name and user.email.

        args:
            * module:
                type: dict()
                descrition: Ansible basic module utilities and module arguments.
        return:
            * result:
                type: dict()
                desription: updated changed status.
        """
        PARAMETERS = ['name','email']
        result = dict()
        path = self.module.params.get('path')

        for parameter in PARAMETERS:
            config_parameter = self.module.params.get(f'user_{parameter}')

            if config_parameter:
                command = ['git', 'config', '--local', f'user.{parameter}']
                _rc, output, _error = self.module.run_command(command, cwd=path)

                if output != config_parameter:
                    command.append(config_parameter)
                    _rc, output, _error = self.module.run_command(command, cwd=path)

                    result.update({f"{parameter}": output, "changed": True})

        return result