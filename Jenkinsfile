pipeline {
    agent any

    environment {
        IMAGE = "hariharaprabhu21/flask-cicd"
        TAG   = "${BUILD_NUMBER}"
    }

    options {
        timeout(time: 20, unit: 'MINUTES')
        buildDiscarder(logRotator(numToKeepStr: '10'))
    }

    triggers {
        pollSCM('H/2 * * * *')
    }

    stages {
        stage('Checkout') {
            steps { checkout scm }
        }

        stage('Install & Test') {
            steps {
                sh '''
                  python3 -m venv venv
                  venv/bin/pip install -r requirements.txt
                  venv/bin/pytest --junitxml=report.xml
                '''
            }
        }

        stage('Docker Build') {
            steps { sh 'docker build -t $IMAGE:$TAG .' }
        }

        stage('Docker Push') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'dockerhub',
                        usernameVariable: 'USER', passwordVariable: 'PASS')]) {
                    sh '''
                      echo $PASS | docker login -u $USER --password-stdin
                      docker push $IMAGE:$TAG
                    '''
                }
            }
        }

        stage('Deploy') {
            steps {
                sh '''
                  docker rm -f flask-app || true
                  docker run -d --name flask-app -p 5000:5000 $IMAGE:$TAG
                '''
            }
        }

        stage('Smoke Test') {
            steps {
                sh 'sleep 5 && curl -f http://host.docker.internal:5000/health'
            }
        }
    }

    post {
        always {
            junit allowEmptyResults: true, testResults: 'report.xml'
            sh 'docker logout || true'
            deleteDir()
        }
        success { echo "Deployed $IMAGE:$TAG" }
        failure { echo "Pipeline failed - check the stage in red" }
    }
}