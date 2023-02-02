import mysql.connector
from mysql.connector import errorcode
from keras.models import load_model
class AIDAO():
    # Method to upload TARS's memory
    def uploadTARS(self):
        # Initialize connection to local database
        print("Opening connection to database...")
        connection = mysql.connector.connect(host='localhost',
                                                port=8891,
                                                database='tensorflow_models',    #CONNECT
                                                user='root',
                                                password='root')
        try:
            if connection.is_connected():
                db_Info = connection.get_server_info()
                cursor = connection.cursor()
                # Select database
                cursor.execute("select database();")
                record = cursor.fetchone()
                print("Connected to Database: ", record)
                
                mycursor = connection.cursor()
                # Read the h5 file into a binary string
                print("Opening TARS memory file...")
                with open("tars.h5", "rb") as f:
                    model_file_data = f.read()
                # SQL query to insert model into database
                sql = "UPDATE model_storage SET model = %s WHERE id = 1;"
                # Execute query with the h5 file as the parameter
                print("Executing upload...")
                mycursor.execute(sql, (model_file_data,))
                connection.commit()
                # Return true if succesfull
                print("Upload succesfull.")
                return True
        # Errors
        except mysql.connector.Error as err:
            # If access denied error, print something wrong with username or password
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something went wrong.")
                # If database does not exist
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
                # Internal server error
            else:
                print(err)
            return False
        finally: # Close the connection
            if connection.is_connected():
                print("Closing connection...")
                cursor.close()
                connection.close()
                print("Connection closed.")
    # Method to download TARS's memory
    def downloadTARS(self):
        # Initialize connection to local database
        print("Opening connection to database...")
        connection = mysql.connector.connect(host='localhost',
                                                port=8891,
                                                database='tensorflow_models',    #CONNECT
                                                user='root',
                                                password='root')
        try:
            if connection.is_connected():
                db_Info = connection.get_server_info()
                cursor = connection.cursor()
                # Select database
                cursor.execute("select database();")
                record = cursor.fetchone()
                print("Connected to Database: ", record)
                
                cursor = connection.cursor()
                # SQL Query to select model from database
                sql = "SELECT model FROM model_storage WHERE id = 1;"
                # Execute SQL Query
                print("Executing download...")
                cursor.execute(sql)
                row = cursor.fetchone() # raise error if no model found
                if row is None:
                    raise ValueError("No model found in database")
                # Write model to local h5 file
                print("Opening TARS memory file...")
                with open("tars.h5", "wb") as f:
                    f.write(row[0])
                # Return true if succesful
                print("Download succesfull...")
                return True
        # Errors
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(err)
            return False
        finally: # Close connection
            if connection.is_connected():
                cursor.close()
                connection.close()
                print("Database connection closed.")
    # Method to authenticate a user with login
    def login(self, username, password):
        # Initialize connection to local database
        connection = mysql.connector.connect(host='localhost',
                                                port=8891,
                                                database='tensorflow_models',    #CONNECT
                                                user='root',
                                                password='root')
        try:
            if connection.is_connected():
                db_Info = connection.get_server_info()
                cursor = connection.cursor()
                # Select database
                cursor.execute("select database();")
                record = cursor.fetchone()
                print("Connected to database: ", record)
                
                cursor = connection.cursor()
                # SQL Query to select username from users where username and password equals input parameters
                sql = "SELECT username FROM users WHERE username = %s AND password = %s;"
                # Bind parameters
                values = (username, password)
                # Execute query with values binded
                cursor.execute(sql, values)
                row = cursor.fetchone()
                if row is None: # Return false if username or password is incorrect.
                    print("Incorrect Username or Password. Please try again.")
                    return False
                # Else return true
                return True
        # Errors
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(err)
            return False
        finally: # Close connection
            if connection.is_connected():
                print("Closing connection...")
                cursor.close()
                connection.close()
                print("Database connection closed.")
        