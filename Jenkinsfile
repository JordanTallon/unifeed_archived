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
                // Todo: unit / regression tests, health tests?
                echo 'Testing the application..'
                // Start container
                sh "docker-compose up -d"
                // Run Django unit tests
                def testStatus = sh(script: 'docker-compose exec app python manage.py test -v 3', returnStatus: true)

                // Check result of tests (any number that isn't 0 indicates failure)
                if(testStatus != 0){
                    error "Tests failed with status: ${testStatus}"
                }
            }
        }

        stage('Deploy') {
            steps {
                // Todo: Replace the old container with the new container?
                echo 'Deploying the application..'
                sh "docker-compose up -d"
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
