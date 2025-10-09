pipeline {
  agent any

  environment {
    DOCKERHUB_REPO = 'iamruthless/sci-cal'
  }

  stages {
    stage('Checkout') {
      steps { checkout scm }   // uses your GitHub repo configured for the job
    }

    stage('Set up Python') {
      steps {
        sh '''
          python3 --version || true
          pip3 --version || true
          python3 -m venv .venv
          . .venv/bin/activate
          python -m pip install --upgrade pip
          if [ -f requirements.txt ]; then pip install -r requirements.txt; fi
        '''
      }
    }

    stage('Unit Tests') {
      steps {
        sh '''
          . .venv/bin/activate
          pytest -q --junitxml=pytest.xml
        '''
      }
      post {
        always {
          junit allowEmptyResults: true, testResults: 'pytest.xml'
        }
      }
    }

    stage('Build Docker Image') {
      steps {
        sh '''
          docker version
          docker build -t "${DOCKERHUB_REPO}:latest" -t "${DOCKERHUB_REPO}:${BUILD_NUMBER}" .
        '''
      }
    }

    stage('Push Docker Image') {
      steps {
        withCredentials([usernamePassword(credentialsId: 'dockerhub-creds', usernameVariable: 'DH_USER', passwordVariable: 'DH_PASS')]) {
          sh '''
            echo "$DH_PASS" | docker login -u "$DH_USER" --password-stdin
            docker push "${DOCKERHUB_REPO}:latest"
            docker push "${DOCKERHUB_REPO}:${BUILD_NUMBER}"
          '''
        }
      }
    }

    stage('Deploy (Ansible)') {
      steps {
        sh '''
          ansible --version || true
          ansible-playbook -i "localhost," -c local deploy.yml \
            --extra-vars "docker_image=${DOCKERHUB_REPO}:latest"
        '''
      }
    }
  }

  post {
    always { cleanWs() }
  }
}
