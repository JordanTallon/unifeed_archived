pipeline {
    // Run on the next available agent
    agent any
    
    stages {
        stage('Build') {
            steps {
                echo 'Building the Unifeed application..'
                sh "docker-compose build"
            }
        }

        stage('Test') {
            steps {
                echo 'Testing the application..'
                // Start the container
                sh "docker-compose up -d"
                script {
                    // Run Django unit tests and capture the output
                    def testOutput = sh(script: 'docker-compose exec -T app python manage.py test -v 3', returnStdout: true).trim()
        
                    // Print the test output
                    echo testOutput
        
                    // Check for any failures in the output
                    if(testOutput.contains("FAILED") || testOutput.contains("ERRORS")){
                        error "Tests failed, see output above"
                    }
                }
            }
        }


        stage('Deploy') {
            steps {
                //TODO: SSH onto deployment server, git pull the repo, compose the docker file, switch docker container to new one.
                echo 'Deploying the application..'
                
            }
        }
    }
    post {
        always {
            // Cleanup after pipeline execution
            echo 'Cleaning up...'
            sh "docker-compose down"
        }
    }
}



