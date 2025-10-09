pipeline {
  agent any

  environment {
    // Set this to your Docker Hub repo, e.g. "yourname/sci-calc"
    DOCKER_IMAGE = credentials('docker-image-name') // or set a simple string like "yourname/sci-calc"
    // Credentials in Jenkins (Username/Password) ID: 'dockerhub-creds'
    // If you prefer not to use credentials() for DOCKER_IMAGE, replace with a literal.
  }

  stages {
    stage('Checkout') {
      steps { checkout scm }
    }

    stage('Set up Python') {
      steps {
        sh '''
          python3 --version || true
          pip3 --version || true
          python3 -m venv .venv
          . .venv/bin/activate
          pip install --upgrade pip
          pip install -r requirements.txt
        '''
      }
    }

    stage('Unit Tests') {
      steps {
        sh '''
          . .venv/bin/activate
          pytest -q
        '''
      }
      post {
        always {
          junit allowEmptyResults: true, testResults: '**/pytest*.xml'
        }
      }
    }

    stage('Build Docker Image') {
      steps {
        script {
          // If DOCKER_IMAGE is a string like "yourname/sci-calc", this will work.
          sh '''
            IMAGE_NAME="${DOCKER_IMAGE:-yourname/sci-calc}"
            docker build -t "$IMAGE_NAME:latest" .
          '''
        }
      }
    }

    stage('Push Docker Image') {
      steps {
        withCredentials([usernamePassword(credentialsId: 'dockerhub-creds', usernameVariable: 'DH_USER', passwordVariable: 'DH_PASS')]) {
          sh '''
            IMAGE_NAME="${DOCKER_IMAGE:-yourname/sci-calc}"
            echo "$DH_PASS" | docker login -u "$DH_USER" --password-stdin
            docker push "$IMAGE_NAME:latest"
          '''
        }
      }
    }

    stage('Deploy (Ansible)') {
      steps {
        sh '''
          # Assumes ansible is installed on the Jenkins agent and inventory present (or using localhost).
          ansible --version || true
          ansible-playbook -i "localhost," -c local deploy.yml \
            --extra-vars "docker_image=${DOCKER_IMAGE:-yourname/sci-calc}:latest"
        '''
      }
    }
  }

  post {
    always { cleanWs() }
  }
}

