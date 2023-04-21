#!/bin/bash
cd ../ansible_collections/lvrfrc87/git_acp/ && \
ansible-galaxy collection build && \
ansible-galaxy collection install lvrfrc87-git_acp-2.1.0.tar.gz -p ./tests/install/ && \
ansible-galaxy collection publish ./lvrfrc87-git_acp-2.1.0.tar.gz --token=e7460647d7746d0a0c95e2859181714a23c4eb49
