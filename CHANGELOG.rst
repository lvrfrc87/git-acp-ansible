# Ver. 2.1.0

- Add support for `push` option.
- Add `force_push` argument.
- Improve README.md
- Minor fixes and improvements

# Ver. 2.0.0

- Remove git config argument (the practice of setting parameters in the environmental variables is encouraged)
- Remove remote argument (the practice of setting parameters in the URL is encouraged).
- Remove user argument (the practice of setting parameters in the URL is encouraged).
- Remove token argument (the practice of setting parameters in the URL is encouraged).
- Remove remote argument (the practice of setting parameters in the URL is encouraged)

# Ver. 1.5.0

- Add `pull` function.
- Bump cryptography.
- Fix typo in README.md.
- Fix Compatibility with pre-commit ansible-lint.

# Ver. 1.4.1

- Remove duplicated variable.
- Rename "origin" variable into "remote".
- Improve conditional logic for URL set.
- Update README.md

# Ver. 1.4.0

- Add SSH parameters support.
- Add poetry.

# Ver. 1.3.0

- Class based code refactoring.

# Ver. 1.2.0

- Minor code refactoring.

# Ver. 1.1.3

- Add default "origin" in remote.
- End of support for PyPi.
- Remove args from closure function.

# Ver. 1.1.2

- New release for PyPi package fix only.

# Ver. 1.1.1

- Add support for Gitolite ssh URL.

# Ver. 1.1.0

- Add idempotency for `git remote add`  command.
- Add support for custom `remote` repo alias (i.e. origin).
- Improved returned module messages.
- Add support for `git config user.name` and `user.email`.
- Add doc strings to each function.
- Improve variable name.

# Ver. 1.0.9

- Add fail if 'ssh://' in GitHub URL when ssh mode.

# Ver. 1.0.8

- Add no_log to HTTPS token argument.

# Ver. 1.0.7

- Module not failing even if git repo has nothing to commit.

# Ver. 1.0.6

- Improve conditional logic for ssh://git@.
- Improve error message in URL.

# Ver. 1.0.5

- Update conditional for ssh://git@.

# Ver. 1.0.4

- Fix comment variable.
- Implement RC validation.
- Update return values.
- Add `--` in git_add.
- Move URLs conditional under main.

# Ver. 1.0.2

- Remove unused `allow_empty`.
- Fix return for `push_options`.

# Ver. 1.0.1

- Change version only.

# Ver. 1.0.0

- Build pypi package for git_acp ansible install.
