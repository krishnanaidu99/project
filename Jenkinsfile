pipeline {
    agent any

    environment {
        GIT_REPO = 'https://github.com/krishnanaidu99/project.git' // Git repository URL
        BRANCH = 'main'                                           // Branch to checkout
        DOCKER_IMAGE_NAME = 'project_image'                       // Name of the Docker image
        DOCKER_CONTAINER_NAME = 'project_container'               // Name of the Docker container
        PORT_MAPPING = '9000:7000'                                // Port mapping
        WORKDIR = "${WORKSPACE}"                                  // Jenkins workspace
    }

    stages {
        stage('Install Docker') {
            steps {
                script {
                    echo "Installing Docker if not already installed..."
                    sh """
                        if ! [ -x \$(command -v docker) ]; then
                            echo "Docker not found, installing..."
                            apt-get update
                            apt-get install -y docker.io
                            systemctl start docker
                            systemctl enable docker
                        else
                            echo "Docker is already installed."
                        fi
                    """
                }
            }
        }

        stage('Checkout') {
            steps {
                script {
                    echo "Cloning the repository..."
                    checkout([$class: 'GitSCM', branches: [[name: "${BRANCH}"]],
                              userRemoteConfigs: [[url: "${GIT_REPO}"]]])
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    echo "Building Docker image: ${DOCKER_IMAGE_NAME}..."
                    sh "docker build -t ${DOCKER_IMAGE_NAME} ${WORKDIR}"
                }
            }
        }

        stage('Deploy Docker Container') {
            steps {
                script {
                    echo "Cleaning up any existing container named ${DOCKER_CONTAINER_NAME}..."
                    sh """
                        if [ \$(docker ps -aq -f name=${DOCKER_CONTAINER_NAME}) ]; then
                            docker rm -f ${DOCKER_CONTAINER_NAME}
                        fi
                    """
                    echo "Deploying new container ${DOCKER_CONTAINER_NAME}..."
                    sh "docker run -d --name ${DOCKER_CONTAINER_NAME} -p ${PORT_MAPPING} ${DOCKER_IMAGE_NAME}"
                }
            }
        }
    }

    post {
        always {
            echo 'Cleaning up dangling Docker images...'
            sh "docker image prune -f || true"
        }
        success {
            echo 'Pipeline completed successfully!'
        }
        failure {
            echo 'Pipeline failed. Please check the logs for more details.'
        }
    }
}
