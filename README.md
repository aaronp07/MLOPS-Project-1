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

