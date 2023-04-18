# TARS
OFFICIAL TARS REPOSITORY

TARS is an Artificial Intelligence system. TARS has access to API's that it can use to communicate meteorological data, such as weather, to the user. TARS also has access to the ChatGPT API, so that it can respond to prompts that it was not explicitly trained on.

- TARS utilizes it's LSTM (Long Short-Term Memory) Embedded Recurrent Neural Network to process and classify language. 

- This neural network works hand in hand with Keras' tokenizer and NLTK to map words to it's vector matrix, and compares an input to (n) output neurons, making probability predictions. 

# UNIQUE FEATURES

 - Context Awareness
  TARS has it's own context awareness trained as supporting intents. It can now keep track of the context of conversation. You can see this in action down below in the 'Example Conversation' section.
  
 - Threshold meets Chat-GPT
  TARS, as most chatbots do, has a confidence threshold in it's predictions. What I decided to do though, is rather than simply coding a response like "I'm sorry, I didnt understand", it will send the message to Chat-GPT for a response.
  
 - Smooth UI Interface
  A smooth user interface has been built to allow for easy communication with TARS, and ease of authentication with the IP address and API key.
  
 - Advanced Neural Network
  TARS started off as a simple network with a couple dense layers and an output layer, using bag-of-words preprocessing. In other words, a basic tutorial copied from geeks-for-geeks. Now, tars features an advanced LSTM recurrent neural network, with almost 50 thousand trainable parameters. Training architecture is now taking advantage of a technique called K-fold cross validation to ensure that TARS both trains on and validates on every piece of data that it's given. Data is preprocessed using methods such as token embedding and one-hot encoding. This allows for a fairly advanced understanding of the data that it was trained on.
  
 - Persisted memory
 Finally, the memory of TARS is persisted by the ability for me to upload and download his weights and nerual network to and from a MySQL database. This both secures the model, and adds for future ability to regularly update TARS's weights. 



# Initialize TARS
Follow the below steps to initialize TARS.
 - Pull down the docker image.
 - Run the docker image and map the ports to the host machine.
 - HTTP 'Post' requests can now be sent to the IP address of the host machine, from machines on the same wifi network. Use the '/chat' endpoint. (I.E. 172.168.0.1:8000/chat)
 - You can also use the UI client to send requests. Make sure you've typed your API key and machine's IP address into the side navigation bar's respective slots. The UI can be found in my TARS_UI repository.
# TECHNOLOGIES
- Python 3.9.12
- Tensorflow 2.10.0, Keras 2.10.0
- Rasperry Pi 4B
- NLTK, PyEnchant, and more.

# REQUIRED MODULES
 All you need is docker, and the docker image :)

# DOCUMENTATION
Documentation can be found in the 'Documents' directory located in the root of the project.

# Example Conversations

Let's walk through some example conversations with TARS using the UI client. 


- Context Awareness

![context](https://user-images.githubusercontent.com/23193263/232133654-d82b3b2b-2f15-4cb0-8b4a-d4afb2ba4cfa.jpg)


- Current Weather Data

![current](https://user-images.githubusercontent.com/23193263/232134358-e0b8eb4c-64d1-4f1b-bff8-1c37914dc404.jpg)


- Weekly Weather Data
![weekly](https://user-images.githubusercontent.com/23193263/232137924-318a4e91-715c-413a-a719-c4e2305a079e.jpg)


- Daily Weather Data

![daily](https://user-images.githubusercontent.com/23193263/232141485-8c311723-bb19-40ab-a333-8fb78470b2f4.jpg)

