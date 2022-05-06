import sqlite3





class DataPlayer():

    DataBaseName = "Player.db"


    def __init__(self, **kwargs):
        super().__init__(**kwargs)



    def CreateAccount(self, name, lastname, password):


        connect = sqlite3.connect(self.DataBaseName)

        cursor = connect.cursor()

        cursor.execute("INSERT INTO Player VALUES (:name, :lastname, :password)",
                       {
                           'name': name,
                           'lastname': lastname,
                           'password': password
                       }
                       )

        connect.commit()

        connect.close()


    def UpdatePassword(self,Name ,NewPassword):
        conn = sqlite3.connect(self.DataBaseName)

        cursor = conn.cursor()

        cursor.execute(f"UPDATE Player SET password= '{NewPassword}' WHERE name='{Name}'")


        conn.commit()

        conn.close()




    def ShowDate(self):
        conn = sqlite3.connect(self.DataBaseName)

        cursor = conn.cursor()

        cursor.execute("SELECT * FROM Player")

        record = cursor.fetchall()

        print(record)

        conn.commit()

        conn.close()
        return record

    def InitializeData(self):


        print("Connecting DataBase!")

        conn = sqlite3.connect(self.DataBaseName)

        cursor = conn.cursor()

        cursor.execute("CREATE TABLE IF NOT EXISTS Player(name text, lastname text, password text)")

        conn.commit()

        conn.close()

        print("DataBase Connected!")

