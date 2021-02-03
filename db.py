import mysql.connector
from mysql.connector import Error
from mysql.connector import errorcode
from datetime import datetime

class DBConection:
    
    def insertar_servidor(self, json_servidor):
        
        try:        
            cnx = mysql.connector.connect(option_files='mydb.conf')
            mycursor = cnx.cursor()

            date = datetime.now()
            sql_insert_query= ("insert into servidores (servidor_nombre, servidor_procesador, servidor_sistema_operativo,"
                            "servidor_version, servidor_cpu_utilizacion, servidor_fecha)"
                            "values (%s,%s, %s, %s, %s, %s)")
            values = ('test', 'test', 'test', 'test', 30.1, date)
            mycursor.execute(sql_insert_query, values)
            cnx.commit()
            print("New Student Added")
       
        except mysql.connector.Error as error:
            print("Failed to insert query into tbStudent table {}".format(error))
        finally:
            mycursor.close()
            cnx.close()

