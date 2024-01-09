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
                // Start container
                sh "docker-compose up -d"
                script {
                    // Run Django unit tests and capture the output
                    def testOutput = sh(script: 'docker-compose exec -T app python manage.py test -v 3', returnStdout: true).trim()
        
                    // Print the test output
                    echo testOutput
        
                    // Check for test failures in the output
                    if(testOutput.contains("FAILED") || testOutput.contains("ERRORS")){
                        error "Tests failed, see output above"
                    }
                }

                echo 'Cleaning up...'
                sh "docker-compose down"
            }
        }


        stage('Deploy') {
            steps {
                echo 'Deploying the application..'
                sh '''
                    ssh root@206.189.22.163 <<EOF
                        echo "Stopping the old server and freeing up port 80..."

                        docker-compose -f docker-compose-deploy.yml down
                        # Sometimes the nginx proxy held port 80 (this is probably dangerous, if there's any issues; i'll find another way)
                        lsof -ti:80 | xargs --no-run-if-empty kill
                        
                        echo "Pulling the Unifeed repo..."
                        cd /opt/projects/2024-ca326-unifeed
                        git pull
                        
                        echo "Starting the Docker containers..."
                        docker-compose -f docker-compose-deploy.yml build
                        docker-compose -f docker-compose-deploy.yml up -d
                    EOF
                '''
                }
            }
    }
}



