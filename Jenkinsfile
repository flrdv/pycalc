pipeline {
    agent any

    environment {
        PATH = "${PATH}:${HOME}/.local/bin"
    }

    stages {
        stage('Cloning the repo') {
            steps {
                git branch: 'i190544', url: 'https://github.com/SyedMustafa145/researchgpt.git'
                bat 'pip install poetry'

            }
        }

        stage('Lint with flake8') {
            steps {
                bat 'pip install flake8'
                bat 'flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics'
            }
        }

        stage('Format with black') {
            steps {
                bat 'pip install black'
                bat 'black .'
            }
        }

    }
}
