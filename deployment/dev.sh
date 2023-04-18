#!/bin/bash
cd ../ansible_collections/lvrfrc87/git_acp/ && \
ansible-test sanity --docker -v plugins/ && \
ansible-test integration -v --docker && \
ansible-lint tests/integration/targets/git_acp/tasks/main.yml
