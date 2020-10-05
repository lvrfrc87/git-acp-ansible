# Ver. 1.1.0

- Add idempotency for `git remote add`  command
- Add support for custom `remote` repo alias (i.e. origin)
- Improved returned module messages
- Add support for `git config user.name` and `user.email`
- Add doc strings to each function
- Improve variable name

# Ver. 1.0.9

- Add fail if 'ssh://' in GitHub URL when ssh mode

# Ver. 1.0.8

- Add no_log to HTTPS token argument

# Ver. 1.0.7

- Module not failing even if git repo has nothing to commit

# Ver. 1.0.6

- Improve conditional logic for ssh://git@
- Improve error message in URL

# Ver. 1.0.5

- Update conditional for ssh://git@

# Ver. 1.0.4

- Fix comment variable
- Implement RC validation
- Update return values
- Add `--` in git_add
- Move URLs conditional under main

# Ver. 1.0.2

- Remove unused `allow_empty`
- Fix return for `push_options`

# Ver. 1.0.1

- Change version only

# Ver. 1.0.0

- Build pypi package for git_acp ansible install
