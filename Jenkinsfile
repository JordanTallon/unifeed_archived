pipeline {
    // Run on the next available agent
    agent any

    options {
        gitLabConnection('gitlab-unifeed')
    }

    // triggers from GitLab
    triggers {
        gitlab(triggerOnPush: true, triggerOnMergeRequest: true, branchFilterType: 'All')
    }

    stages {
        stage('Build') {
            steps {
                echo ${BRANCH_NAME}
                script {
                    updateGitlabCommitStatus name: 'build', state: 'running'
                    echo 'Building the Unifeed application..'
                    // Start container
                    sh "docker-compose build"
                    updateGitlabCommitStatus name: 'build', state: 'success'
                }
            }
        }

        stage('Test') {
            steps {
                script {
                    updateGitlabCommitStatus name: 'test', state: 'running'
                    echo 'Testing the application..'

                    // Start container
                    sh "docker-compose up -d"
                    def testOutput = sh(script: 'docker-compose exec -T app python manage.py test -v 3', returnStdout: true).trim()

                    // Print the test output                    
                    echo testOutput

                    // Check for test failures in the output
                    if (testOutput.contains("FAILED") || testOutput.contains("ERRORS")) {
                        updateGitlabCommitStatus name: 'test', state: 'failed'
                        error "Tests failed, see output above"
                    } else {
                        updateGitlabCommitStatus name: 'test', state: 'success'
                    }
                }
                echo 'Cleaning up...'
                sh "docker-compose down"
            }
        }

        stage('Deploy') {
            when {
                branch 'main'
            }
            steps {
                script {
                    updateGitlabCommitStatus name: 'deploy', state: 'running'
                    echo 'Deploying the application..'
                                    sh '''
                    ssh root@206.189.22.163 <<EOF
                    
                        echo "Entering project directory"
                        cd /opt/projects/2024-ca326-unifeed
                        
                        echo "Stopping the old server and freeing up port 80..."

                        docker-compose -f docker-compose-deploy.yml down
                        # Sometimes the nginx proxy held port 80 (this is probably dangerous, if there's any issues; i'll find another way)
                        lsof -ti:80 | xargs --no-run-if-empty kill
                        
                        echo "Pulling the Unifeed repo..."
                        git pull
                        
                        echo "Starting the Docker containers..."
                        docker-compose -f docker-compose-deploy.yml build
                        docker-compose -f docker-compose-deploy.yml up -d
                        << EOF
                        '''
                    updateGitlabCommitStatus name: 'deploy', state: 'success'
                }
            }
        }
    }

    post {
        failure {
            updateGitlabCommitStatus name: 'build', state: 'failed'
        }
        success {
            updateGitlabCommitStatus name: 'build', state: 'success'
        }
        aborted {
            updateGitlabCommitStatus name: 'build', state: 'canceled'
        }
    }
}
