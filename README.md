# TARS
OFFICIAL TARS REPOSITORY

TARS is an AI Chatbot Entity planted on a Raspberry Pi. TARS can be communicated with by connecting to the Raspberri Pi via SSH, after which TARS automatically wakes up and connects to the user. 
# Initialize TARS
Follow the below steps to initialize TARS.
 - Navigate to the root of the TARS Directory.
 - run 'python training.py'
 - after successful training, the tars.h5 file should be populated. Uploading and downloading TARS's memory can be done with 'python upload.py' and 'python download.py' respectively.
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
