#!/bin/bash
ansible-galaxy collection build && \
ansible-galaxy collection install lvrfrc87-git_acp-1.1.3.tar.gz -p ./tests/install/ && \
ansible-galaxy collection publish ./lvrfrc87-git_acp-1.1.3.tar.gz --token=$GALAXY_TOKEN