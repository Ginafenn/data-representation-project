
# Import Packages
import mysql.connector
import dbconfig as cfg


# Using the variables from dbconfig.py

class PhoneDAO:
    connection = None
    cursor = None
    
    def __init__(self):
        self.host = cfg.host
        self.user = cfg.user
        self.password = cfg.password
        self.database = cfg.database

    def getcursor(self): 
        self.connection = mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database,
        )
        self.cursor = self.connection.cursor()
        return self.cursor

    def closeAll(self):
        if self.connection is not None:
            self.connection.close()
        if self.cursor is not None:
            self.cursor.close()

    def create(self, values):
        try:
            cursor = self.getcursor()
            sql = "INSERT INTO phone (Make, Model, Price) values (%s, %s, %s)"
            print(f"Executing SQL: {sql} with values: {values}")
            cursor.execute(sql, values)

            self.connection.commit()
            new_id = cursor.lastrowid
            print(f"New phone record inserted with id: {new_id}")
            return new_id
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return None
        finally:
            self.closeAll()

    def getAll(self):
        cursor = self.getcursor()
        sql="select * from phone"
        cursor.execute(sql)
        results = cursor.fetchall()
        returnArray = []
        print(results)
        for result in results:
            print(result)
            returnArray.append(self.convertToDictionary(result))
        
        self.closeAll()
        return returnArray

    def findByID(self, id):
        cursor = self.getcursor()
        sql="select * from phone where id = %s"
        values = (id,)

        cursor.execute(sql, values)
        result = cursor.fetchone()
        returnvalue = self.convertToDictionary(result)
        self.closeAll()
        return returnvalue

    def update(self, values):
        cursor = self.getcursor()
        sql="update phone set Make= %s,Model=%s, Price=%s  where id = %s"
        cursor.execute(sql, values)
        self.connection.commit()
        self.closeAll()
        
    def delete(self, id):
        cursor = self.getcursor()
        sql="delete from phone where id = %s"
        values = (id,)
        print(f"Executing SQL: {sql} with values: {values}")  # Debugging print statement
        cursor.execute(sql, values)
        self.connection.commit()
        self.closeAll()
        print("delete done")

    def convertToDictionary(self, result):
        colnames=['id','Make','Model', "Price"]
        item = {}
        
        if result:
            for i, colName in enumerate(colnames):
                value = result[i]
                item[colName] = value
        
        return item
        
phoneDAO = PhoneDAO()





















