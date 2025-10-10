pipeline {
  agent any
  options { timestamps(); skipDefaultCheckout(true) }
  triggers { githubPush() }              // remove if you don’t want auto-builds

  environment {
    APP_REPO = 'sci-cal'                 // image name only (no namespace)
  }

  stages {
    stage('Checkout') {
      steps { checkout scm }
    }

    stage('Set up Python') {
      steps {
        sh '''
          set -e
          python3 --version || true
          pip3 --version || true
          python3 -m venv .venv
          . .venv/bin/activate
          python -m pip install --upgrade pip
          if [ -f requirements.txt ]; then pip install -r requirements.txt; fi
          # Install pytest only if tests exist
          if ls -1 tests 2>/dev/null | grep -q .; then pip install pytest; fi
        '''
      }
    }

    stage('Unit Tests') {
      steps {
        sh '''
          . .venv/bin/activate
          # Prove pytest is installed and show what it will collect
          python -c "import pytest, sys; print('pytest', pytest.__version__)"
          # Run tests explicitly from the root file
          pytest -q test_calculator.py --junitxml=pytest.xml
        '''
      }
      post {
        always {
          junit testResults: 'pytest.xml', allowEmptyResults: true
        }
      }
    }


    stage('Build & Push Docker Image') {
      steps {
        withCredentials([usernamePassword(credentialsId: 'dockerhub-creds', usernameVariable: 'DH_USER', passwordVariable: 'DH_PASS')]) {
          sh '''
            set -e
            docker version
            IMAGE="${DH_USER}/${APP_REPO}"
            echo "Building ${IMAGE}:${BUILD_NUMBER} and :latest"
            docker build -t "${IMAGE}:latest" -t "${IMAGE}:${BUILD_NUMBER}" .

            echo "$DH_PASS" | docker login -u "$DH_USER" --password-stdin
            docker push "${IMAGE}:latest"
            docker push "${IMAGE}:${BUILD_NUMBER}"
            docker logout

            # persist the full image ref for deploy stage
            echo "${IMAGE}" > .image_name
          '''
        }
      }
      post {
        failure { sh 'docker logout || true' }
      }
    }

    stage('Deploy (Ansible → localhost)') {
      steps {
        sh '''
          set -e
          IMAGE="$(cat .image_name)"
          echo "Deploying ${IMAGE}:latest via Ansible"
          ansible --version || true
          ansible-playbook -i "localhost," -c local deploy.yml \
            --extra-vars "docker_image=${IMAGE}:latest"
        '''
      }
    }
  }

  post {
    always { cleanWs() }
  }
}
