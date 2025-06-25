pipeline {
    agent any

    environment {
        IMAGE_NAME = "gcr.io/YOUR_PROJECT_ID/test-aerospike-app"
    }

    stages {
        stage('Docker Build') {
            steps {
                sh 'docker build -t $IMAGE_NAME .'
            }
        }

        stage('Push to GCR') {
            steps {
                sh 'gcloud auth configure-docker'
                sh 'docker push $IMAGE_NAME'
            }
        }

        stage('Deploy to GKE') {
            steps {
                sh 'helm upgrade --install test-aerospike-app helm-charts/ --values helm-charts/dev-values/aerospike.yaml --set image.tag=latest'
            }
        }
    }
}
