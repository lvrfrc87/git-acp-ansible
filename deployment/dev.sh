#!/bin/bash
cd ../ansible_collections/studyly/git_mactp/ && \
ansible-test sanity --docker -v plugins/ && \
ansible-test integration -v --docker && \
ansible-lint tests/integration/targets/git_mactp/tasks/main.yml
