#!/bin/bash
ansible-test sanity --docker -v plugins/modules/ && \
ansible-test integration -v --docker
# ansible-lint tests/integration/targets/git_acp/tasks/main.yml
