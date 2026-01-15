Google Cloud Set up:
    - Sign-In Google Cloud: https://console.cloud.google.com/
    - Install Google Cloud CLI: https://docs.cloud.google.com/sdk/docs/install-sdk
        * After installation completed restart vs-code
        * Check the version: `gcloud --version`

        1. Search `buckets`
            * Create bucket:
                - Upload the file 'Hotel_Reservation.csv' without contain space in file name

        2. Navigate Menu `IAM & Admin --> Service Accounts`
            * Create service account:
                `mlop-project-1` --> Create and continue
            * Permissions:
                Select Role - `Storage Admin` and `Storage Object Viewer` --> Continue

            * `mlop-project-1@burnished-flare-484006-e2.iam.gserviceaccount.com` and select three dot
                `Manage permissions` --> Keys tab --> `Add key` --> `Create new key` and download the json file
        
        3. Search `buckets` and select three dot
            * `Edit access` --> `Add principal`
            * Search `mlops-project-1` and select
            * Assign roles --> `Storage Admin` and `Storage Object Viewer` --> Save

        4. vs-code in powershell: `set GOOGLE_APPLICATION_CREDENTIALS=C:\Users\Aaron\Downloads\burnished-flare-484006-e2-08628c6da325.json`

Project Setup:
    - Create MLOPS-Project-1 Folder and open with vs-code

    - Create venv using powershell:
        `python -m venv venv`

    - Create Folder and Files Structures:
        artifacts
        config
            __init__.py
            config.yaml
        src
            __init__.py
            custom_exception.py
            data_ingestion.py
            logger.py
        static
        pipeline
            __init__.py
        templates
        utils
            __init__.py
        requirements.txt
        setup.py
            from setuptools import setup, find_packages

            with open('requirements.txt') as f:
                requirements = f.read().splitlines()
                
            setup(
                name = 'MLOPS-Project-1',
                version = '0.1',
                author = 'Aaron P',
                packages = find_packages(),
                install_requires = requirements
            )

        ** Execute setup.py
            `pip install -e .` - This refer to setup.py file and look all the packages whereever contain `__init__.py` file

    - Create Logger file inside the src folder

    - Create Custom Exception file inside the src folder

1. Project Folder Setup

2. Loggers
    `src/logger.py`

3. Custom Exception
    `src/custom_exception.py` - For test `Custom_Exception_Test.py`

4. Data Ingestion - installation `google-cloud-storage, scikit-learn, pyyaml`
   i.  `config/config.yaml` - Bucket Name, File Name, Train Data
   ii. `config/paths_config.py` - Only storing path. Raw data --> splitting into Train and Test file .csv
   iii. `utils/common_functions.py` - Reading YAML file
   iv. `src/data_ingestion.py` - Download the file from google cloud bucket for Raw, Train and Testing csv files

5. Data Processing - installation `imbalanced-learn`
    i. `utils/common_functions.py` - Reading csv file
    ii. `config/paths_config.py` - Only storing path. Train and Test file .csv
    iii. `config/config.yaml` - Categorical and Numerical column names
    iv. `src/data_preprocessing.py` - Data Cleaning, Balance Data, Feature Selection, Save Data

6. Model Training and Experiment Tracking - installation `scipy, joblib, lightgbm, mlflow`
    i. `config/paths_config.py` - Only storing path. Model training pickle file .pkl
    ii. `config/model_params.py` - Model parameter or hyperparameter
    iii. `src/model_training.py` - Train and Test, Model train, Model evaluation, Save model and Export .pkl file
    iv. In powershell - `mlflow ui`

7. Pipeline
    i. `pipeline/training_pipeline.py` - To execute all the process (Data Ingestion, Data Processing, Model Training and Model saved)

8. Flask - installation `flask`
    i. `templates/index.html` and `static\style.css` - Create a web page
    ii. `application.py` - Prediction method using POST method

9. CI-CD Deployment using Jenkins and Google Cloud
    i. Setup Jenkins Container (DinD - Docker in Docker)
    ii. Github Integration
    iii. Dockerization of project (Docker file)
    iv. Create a venv in Jenkins
    v. Build Docker Image of project - Push to Google Cloud Registry (GCR)
    vi. Extract image from GCR - Push to Google Cloud Run (App is deployed)

    i. Setup Jenkins Container (DinD - Docker in Docker)
        1. Create `custom_jenkins` folder:
            `Dockerfile` create file and paste code

            # Use official Jenkins with Docker-in-Docker support
            FROM jenkins/jenkins:lts-jdk17

            USER root

            # Install Docker CLI + DinD dependencies
            RUN apt-get update && \
                apt-get install -y \
                ca-certificates \
                curl \
                gnupg \
                lsb-release && \
                curl -fsSL https://download.docker.com/linux/debian/gpg | gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg && \
                echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/debian \
                $(lsb_release -cs) stable" | tee /etc/apt/sources.list.d/docker.list > /dev/null && \
                apt-get update && \
                apt-get install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin && \
                apt-get clean && rm -rf /var/lib/apt/lists/*

            # Allow Jenkins user to use Docker without sudo
            RUN usermod -aG docker jenkins

            # Switch back to Jenkins user
            USER jenkins

        2. Create Docker Image:
            i. Check docker login - `docker login`
            ii. Create Image - `docker build -t jenkins-dind .`
            iii. Finally Check the repository image created - `docker images`

        3. Run the Docker Image:
            docker run -d --name jenkins-dind `
                --privileged ` # Run privileged mode
                -p 8080:8080 -p 50000:50000 ` # Port number
                -v /var/run/docker.sock:/var/run/docker.sock ` # Setup connection between docker and jenkins
                -v jenkins_home:/var/jenkins_home ` # Create a volume directory for jenkins
                jenkins-dind # Container name

        4. Install suggested plugin and Create user
            `docker ps`
            `docker logs jenkins-dind` # Password will generate

            **** Open Web Browser - `http://localhost:8080/` ****
            i. Paste the password
            ii. Customize Jenkins - Install suggested plugins
            iii. Create the user
        
        5. Setup Jenkins Container - Terminal custom_jenkins
            `docker exec -u root -it jenkins-dind bash` # Open the bash
            `apt update -y` # Packages
            `apt install -y python3` # Install python
            `python3 --version` # Check the python version
            `ln -s /usr/bin/python3 /usr/bin/python` # Nick name python3 to python
            `python --version` # Version check the python3 or python both will work
            `apt install -y python3-pip` # Installing pre-requisiting
            `apt install -y python3-venv` # Create virual environment
            `exit` # End the bash

    ii. Github Integration
        1. Github Generate Token
            * Profile -> Setting -> Developer Setting -> Personal Access Token -> Tokens (classic)
            * Note `jenkins-github-token`
                - Permission
                    repo, admin:repo_hook
            * Generate token
        
        2. Jenkins Dashboard
            * Manage Jenkins -> Credentials -> click (global) -> Add Credential
            * Username: github account name (aaronp07)
            * Password: Github token
            * Id: github-token
            * Description: github-token
            * Create

        3. Jenkins Dashboard
            * New Item
                Item Name: MLOPS-1
                Select -> `Pipeline`
                Ok
            * Pipeline session
                Select -> `Pipeline script from SCM` (Source Code Management)
                SCM Select -> Git
                Repository URL -> `https://github.com/aaronp07/MLOPS-Project-1.git`
                Credential -> github-token
                Branch to build: */main
                Save

        4. Pipeline Syntax
            * Sample Step
                Select -> `checkout: Check out from version control`
                Repository URL -> `https://github.com/aaronp07/MLOPS-Project-1.git`
                Credential -> github-token
                Branch to build: */main
                Generate Pipeline Script

        5. VS-Code Create File `Jenkinsfile`
            pipeline{
                agent any

                stages{
                    stage("Cloning Github repo to Jenkins"){
                        steps{
                            script{
                                echo 'Cloning Github repo to Jenkins...........'
                                checkout scmGit(branches: [[name: '*/main']], extensions: [], userRemoteConfigs: [[credentialsId: 'github-token', url: 'https://github.com/aaronp07/MLOPS-Project-1.git']])
                            }
                        }
                    }
                }
            }

        6. Git bash
            `git add .`
            `git commit -m 'commit'`
            `git push origin main`

        7. Jenkins Dashboard
            * Click -> `MLOPS-1`
            * Build Now
            * Workspaces (Clone all codes in Jenkins workspace)

    iii. Dockerization of project (Docker file)
        * Create `Dockerfile` in root folder
            FROM python:slim

            ENV PYTHONDONTWRITEBYTECODE = 1\
                PYTHONUNBUFFERED = 1

            WORKDIR /app

            RUN apt-get update && apt-get-install -y --no-install-recommends \
                libgomp1 \
                && apt-get-clean \
                && rm -rf /var/lib/apt/lists/*

            COPY . .

            RUN pip install --no-cache-dir -e .

            RUN python pipeline/training_pipeline.py

            EXPOSE 5000

            CMD ["python", "application.py"]

    iv. Create a venv in Jenkins
        * Jenkinsfile
            pipeline{
                agent any

                environment {
                    VENV_DIR = 'venv'
                }

                stages{
                    stage("Cloning Github repo to Jenkins"){
                        steps{
                            script{
                                echo 'Cloning Github repo to Jenkins...........'
                                checkout scmGit(branches: [[name: '*/main']], extensions: [], userRemoteConfigs: [[credentialsId: 'github-token', url: 'https://github.com/aaronp07/MLOPS-Project-1.git']])
                            }
                        }
                    }

                    stage("Setting up virtual environment and installing dependencies"){
                        steps{
                            script{ 
                                echo 'Setting up virtual environment and installing dependencies.......'
                                sh '''
                                python -m venv ${VENV_DIR}
                                . ${VENV_DIR}/bin/activate
                                pip install --upgrade pip
                                pip install -e .
                                '''
                            }
                        }
                    }
                }
            }

    v. Build Docker Image of project - Push to Google Cloud Registry (GCR)
        1. Install Google Cloud CLI on Jenkins container
            `docker exec -u root -it jenkins-dind bash`
                `apt-get update`
                `apt-get install -y curl apt-transport-https ca-certificates gnupg`
                `curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key add -`
                `echo "deb https://packages.cloud.google.com/apt cloud-sdk main" | tee -a /etc/apt/sources.list.d/google-cloud-sdk.list`
                `apt-get update && apt-get install -y google-cloud-sdk`

    vi. Extract image from GCR - Push to Google Cloud Run (App is deployed)