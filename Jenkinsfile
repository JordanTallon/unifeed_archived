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
            }
        }

        stage('Deploy') {
            steps {
                // Todo: Replace the old container with the new container?
                echo 'Deploying the application..'
            }
        }
    }
}
