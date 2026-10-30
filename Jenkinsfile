pipeline {
  agent any
  environment {
    IMAGE = 'yashvini2010/incident-monitor'
    TAG   = "${env.BUILD_NUMBER}"
  }
  stages {
    stage('Test') {
      steps {
        sh '''
          python3 -m venv venv
          . venv/bin/activate
          pip install -r requirements.txt
          python -m pytest
        '''
      }
    }
    stage('Build image') {
      steps {
        sh 'docker build -t $IMAGE:$TAG .'
      }
    }
    stage('Push image') {
      steps {
        withCredentials([usernamePassword(credentialsId: 'dockerhub', usernameVariable: 'U', passwordVariable: 'P')]) {
          sh '''
            echo $P | docker login -u $U --password-stdin
            docker push $IMAGE:$TAG
          '''
        }
      }
    }
    stage('Deploy') {
      steps {
        withCredentials([file(credentialsId: 'kubeconfig', variable: 'KUBECONFIG')]) {
          sh '''
            kubectl apply -f k8s/
            kubectl set image deployment/incident-monitor incident-monitor=$IMAGE:$TAG
            kubectl rollout status deployment/incident-monitor --timeout=120s
          '''
        }
      }
    }
  }
  post {
    failure { echo 'Pipeline failed. Check the stage logs.' }
  }
}