import mysql.connector
from mysql.connector import errorcode
from keras.models import load_model
class AIDAO():
    
    def uploadTARS(self):
        connection = mysql.connector.connect(host='localhost',
                                                port=8891,
                                                database='tensorflow_models',    #CONNECT
                                                user='root',
                                                password='root')
        try:
            if connection.is_connected():
                db_Info = connection.get_server_info()
                cursor = connection.cursor()
                cursor.execute("select database();")
                record = cursor.fetchone()
                print("Connected to MySQL Server version ", db_Info +", database: ", record)
                
                mycursor = connection.cursor()
                # Read the h5 file into a binary string
                with open("tars.h5", "rb") as f:
                    model_file_data = f.read()
                sql = "INSERT INTO model_storage (model) VALUES (%s) ON DUPLICATE KEY UPDATE model = VALUES(model);"
                
                affected = mycursor.execute(sql, (model_file_data,))
                connection.commit()
                
                return affected

        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(err)
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
                print("MySQL connection is closed")
                
    def downloadTARS(self):
        connection = mysql.connector.connect(host='localhost',
                                                port=8891,
                                                database='tensorflow_models',    #CONNECT
                                                user='root',
                                                password='root')
        try:
            if connection.is_connected():
                db_Info = connection.get_server_info()
                cursor = connection.cursor()
                cursor.execute("select database();")
                record = cursor.fetchone()
                print("Connected to MySQL Server version ", db_Info +", database: ", record)
                
                mycursor = connection.cursor()
                
                sql = "SELECT model FROM model_storage WHERE id = 1;"
                
                cursor.execute(sql)
                row = cursor.fetchone()
                if row is None:
                    raise ValueError("No model found in database")
                # Write model to local h5 file
                with open("tars.h5", "wb") as f:
                    f.write(row[0])
                model = load_model("tars.h5")
                return model
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(err)
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
                print("MySQL connection is closed")
    
        