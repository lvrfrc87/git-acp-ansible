from __future__ import absolute_import, division, print_function

__metaclass__ = type


class GitConfiguration:
    def __init__(self, module):
        self.module = module

    def config(self):
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
        PARAMETERS = ["name", "email"]
        result = dict()
        path = self.module.params["path"]
        mode = self.module.params["git_config"]["mode"]

        for parameter in PARAMETERS:
            config_parameter = self.module.params["git_config"].get(f"user_{parameter}")
            command = ["git", "config", f"--{mode}", f"user.{parameter}"]
            _rc, output, _error = self.module.run_command(command, cwd=path)

            if output != config_parameter:
                command.append(config_parameter)
                _rc, output, _error = self.module.run_command(command, cwd=path)

                result.update({"git_config": {parameter: output, "changed": True}})

        return result
