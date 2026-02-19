pipeline {

    agent any

    environment {

        DOCKER_IMAGE = "kwamasco/server-info-app"
        DOCKER_TAG = "v${BUILD_NUMBER}"

    }

    stages {

        stage('Checkout Code') {

            steps {

                git branch: 'main',
                url: 'https://github.com/kwamasco/server-info-app.git'

            }

        }


        stage('Build Docker Image') {

            steps {

                sh "docker build -t $DOCKER_IMAGE:$DOCKER_TAG ."

            }

        }


        stage('Push to Docker Hub') {

            steps {

                withCredentials([usernamePassword(
                    credentialsId: 'dockerhub-credentials',
                    usernameVariable: 'DOCKER_USER',
                    passwordVariable: 'DOCKER_PASS'
                )]) {

                    sh "docker login -u $DOCKER_USER -p $DOCKER_PASS"

                    sh "docker push $DOCKER_IMAGE:$DOCKER_TAG"

                }

            }

        }


        stage('Deploy Container') {

            steps {

                sh """
                docker stop server-info-container || true
                docker rm server-info-container || true

                docker run -d -p 5002:5002 \
                --name server-info-container \
                -e VERSION=$DOCKER_TAG \
                -e ENVIRONMENT=JENKINS \
                $DOCKER_IMAGE:$DOCKER_TAG
                """

            }

        }

    }

}