from conexion import Conexion
from datetime import datetime
import ip
import json


class Usuario:
    def __init__(self):
        global conexion
        conexion = Conexion()

    def getUsers(self):
        lista=[]
        lista_ip=[]
        lst=[]
        try:
            if conexion.connect():
                con = conexion.connect()
                cursor = con.cursor()
                cursor.execute('SELECT * FROM cat.users')
                usuarios = cursor.fetchall()
                for usuario in usuarios:
                    datos={"id":usuario[0],"ip":usuario[1],"usuario":usuario[2],"hora":str(usuario[3])}
                    json_datos = json.dumps(datos)
                    lista.append(json.loads(json_datos))
                    dato_ip={"ip":usuario[1]}
                    json_datos_ip = json.dumps(dato_ip)
                    lista_ip.append(json.loads(json_datos_ip))
                
                lst=[lista,lista_ip]
        except Exception as e:
            print("Error: ", e)
        else:
            return lst
        finally:
            cursor.close()
            conexion.disconnect()

    def update_Last_Time(self,ahora,ip):
        query = "UPDATE cat.users SET last_seen= %s WHERE ip_address= %s;"
        try:
            if conexion.connect():
                con = conexion.connect()
                cursor = con.cursor()
                cursor.execute(query, (ahora, ip))
                con.commit()
        except Exception as e:
            print("Error: ", e)
        else:
            #print("Actualizado exitoso")
            pass
        finally:
            cursor.close()
            conexion.disconnect()

    def verify_User(self,ip):
        query="SELECT username FROM cat.users WHERE ip_address = %s;"
        try:
            if conexion.connect():
                con=conexion.connect()
                cursor=con.cursor()
                cursor.execute(query, (ip,))
                row=cursor.fetchone()
                if row is None:
                    return False         
        except Exception as e:
            print("Error: ", e)
        else:
            return True
        finally:
            cursor.close()
            conexion.disconnect()
    
    def register_User(self,ip,nombre):
        ahora = datetime.now() 
        print(ahora)
        query = "INSERT INTO cat.users(ip_address, username, last_seen) VALUES(%s, %s, %s)"
        try:
            if conexion.connect():
                con = conexion.connect()
                cursor = con.cursor()
                cursor.execute(query, (ip, nombre, ahora))
                con.commit()
        except Exception as e:
            print("Error: ", e)
            return False
        else:
            print("Registrado con exitoso")
            return True
        finally:
            cursor.close()
            conexion.disconnect()
                    
            

#uriel=Usuario()
#uriel.register_User("192.168.0.17","root")

#u=Usuario()
#print(u.getUsers())


