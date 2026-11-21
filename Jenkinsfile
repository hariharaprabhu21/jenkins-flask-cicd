@Library('hari-lib@k8s-deploy') _

pythonDockerPipeline(
    image:        'hariharaprabhu21/flask-cicd',
    appName:      'flask-app',
    deployTarget: 'k8s',
    namespace:    'flask',
    nodePort:     30080
)