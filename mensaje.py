from conexion import Conexion

class Mensaje:
    def __init__(self):
        global conexion
        conexion = Conexion()
        
    def register_Message(self,message, emisor, receptor, fecha_hora):
        ip="[{"ip": '192.168.0.179'},{'ip': '192.168.0.135'}]"
        datos = [{"ip": "192.168.0.123"},{"ip": "192.168.0.123"}]
        json_datos = json.dumps(datos)

        query = "cat.adduser"
        try:
            if conexion.connect():
                con = conexion.connect()
                cursor = con.cursor()
                cursor.callproc(query,())
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
            
men=Mensaje()
men.register_Message("hola tona","192.168.0.179","a","2020-02-24 16:25:36.935793")

