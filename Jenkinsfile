pipeline {
    agent { docker { image 'python:3.8.2' } }
    stages {
        stage('build') {
            steps {
                sh 'pip install ansible==2.9.5'
                sh 'pip install ansible-lint'
            }
        }
        stage('lint') {
            steps {
                sh 'ansible-lint -x 502,305,301,303,401,208 tests/integration/targets/source_control/git_acp.yaml'
            }
        }
        stage('integration') {
            steps {
                sh 'pwd'
                sh 'ansible-playbook tests/integration/targets/source_control/git_acp.yaml -vvv'
            }
        }
    }
}