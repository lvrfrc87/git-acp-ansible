from __future__ import absolute_import, division, print_function

__metaclass__ = type


class ModuleFailure:
    def __init__(self, module, rc, command, output, error):
        """
        Failing message function for rc codes != 0.

        args:
            * module:
                type: dict()
                description: Ansible basic module utilities and module arguments.
            * rc:
                type: int()
                description: rc code returned by shell command.
            * command:
                type: list()
                description: list of string that compose the shell command.
            * output:
                type: str()
                description: stdout returned by the shell.
            * error:
                type: str()
                description: stder returned by the shell.

        return: None
        """
        module.fail_json(
            rc=rc,
            msg="Error in running '{command}' command".format(
                command=" ".join(command)
            ),
            command=" ".join(command),
            stdout=output,
            stderr=error,
        )


class FailingMessage(ModuleFailure):
    """Module failure related errors."""
