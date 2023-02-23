# TARS
OFFICIAL TARS REPOSITORY

TARS is an Artificial Intelligence system. TARS has access to API's that it can use to communicate meteorological data, such as weather, to the user. TARS also has access to the GPT-3 API, so that it can respond to prompts that it was not explicitly trained on. 
# Initialize TARS
Follow the below steps to initialize TARS.
 - Navigate to the root of the TARS Directory.
 - run 'python training.py'
 - after successful training, the tars.h5 file should be populated. Uploading and downloading TARS's memory to and from the database can be done with 'python upload.py' and 'python download.py' respectively.
 - 'python tars.py' to run TARS.
# TECHNOLOGIES
- Python 3
- Tensorflow 2.10
- Rasperry Pi 4B 

# REQUIRED MODULES
Run the following commands to install the required modules

- pip install numpy
- pip install nltk
- pip install keras
- pip install mysql-connector-python
