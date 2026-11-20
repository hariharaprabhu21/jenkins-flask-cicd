@Library('hari-lib') _

pipeline {
    agent any

    environment {
        IMAGE = "hariharaprabhu21/flask-cicd"
        TAG   = "${env.BRANCH_NAME.replace('/', '-')}-${env.BUILD_NUMBER}"
    }

    options {
        timeout(time: 20, unit: 'MINUTES')
        buildDiscarder(logRotator(numToKeepStr: '10'))
        disableConcurrentBuilds()
    }

    stages {
        stage('Install & Test') {
            steps { runPythonTests() }
        }
        stage('Docker Build') {
            steps { dockerBuild(image: env.IMAGE, tag: env.TAG) }
        }
        stage('Docker Push') {
            when { branch 'main' }
            steps { dockerPush(image: env.IMAGE, tag: env.TAG) }
        }
        stage('Deploy') {
            when { branch 'main' }
            steps { deployContainer(name: 'flask-app', image: env.IMAGE, tag: env.TAG, port: 5000) }
        }
        stage('Smoke Test') {
            when { branch 'main' }
            steps { smokeTest('http://host.docker.internal:5000/health') }
        }
    }

    post {
        always {
            junit allowEmptyResults: true, testResults: 'report.xml'
            sh 'docker logout || true'
            deleteDir()
        }
        success { echo "Build OK: ${env.IMAGE}:${env.TAG}" }
        failure { echo 'Pipeline failed - check the stage in red' }
    }
}