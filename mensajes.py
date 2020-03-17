from conexion import Conexion

class Mensaje:
    def __init__(self):
        global conexion
        conexion = Conexion()
        
    def getAllMessages(self):
        lista=[]

        try:
            if conexion.connect():
                con = conexion.connect()
                cursor = con.cursor()
                cursor.callproc('cat.getallmessages')
                usuarios = cursor.fetchall()
                for mensaje in mensajes:
                    datos={"id":mensaje[0],"message":mensaje[1],"emisor":mensaje[2],"receptor":mensaje[3],"hora_fecha":str(mensaje[4])}
                    json_datos = json.dumps(datos)
                    lista.append(json.loads(json_datos))
                
        except Exception as e:
            print("Error: ", e)
        else:
            return lista
        finally:
            cursor.close()
            conexion.disconnect()
            
men=Mensaje()
men.register_Message("hola tona","192.168.0.179","a","2020-02-24 16:25:36.935793")

