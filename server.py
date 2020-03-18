from usuarios import Usuario
from http.server import BaseHTTPRequestHandler
import json
from urllib import parse
from cliente import *
from datetime import datetime
import threading

ip_server = "10.128.0.3"

class GetHandler(BaseHTTPRequestHandler):
    global message_list
    message_list=[]
    def __init__(self, *args, **kwargs):
        BaseHTTPRequestHandler.__init__(self, *args, **kwargs)
        
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

    def do_GET(self):
        if self.path=='/messages':
            content_length = int(self.headers['Content-Length'])
            parametros = self.rfile.read(content_length).decode("utf-8")
            j_parametros = json.loads(parametros)
            self._set_headers()
            filtered_messages=self.filtered_out(j_parametros["conexion"],j_parametros["direccion"])
            self.wfile.write(str(json.dumps(filtered_messages)).encode('utf-8'))
        elif self.path=='/users':
            self._set_headers()
            global users_list
            self.wfile.write(str(json.dumps(users_list)).encode('utf-8'))
        elif self.path=='/verify_user':
            content_length = int(self.headers['Content-Length'])
            parametros = self.rfile.read(content_length).decode("utf-8")
            j_parametros = json.loads(parametros)
            self._set_headers()
            res=self.verify_user(j_parametros["direccion"])
            print(res)
            self.wfile.write(str(res).encode("utf-8"))

        
    def do_POST(self):
        if self.path=="/register":
            content_length = int(self.headers['Content-Length'])
            parametros = self.rfile.read(content_length).decode("utf-8")
            j_parametros = json.loads(parametros)

            res=self.register_user(j_parametros["direccion"],j_parametros["usuario"])
            print("respuesta del registro:   ",res)
            self._set_headers()
            self.wfile.write(str(res).encode("utf-8"))

            
        elif self.path=="/add_message":
            content_length = int(self.headers['Content-Length'])
            datos = self.rfile.read(content_length)
            msg=datos.decode('utf-8')
            global message_list
            message_list.append(json.loads(msg))
        

    def do_PUT(self):
        content_length = int(self.headers['Content-Length'])
        parametros = self.rfile.read(content_length).decode("utf-8")
        j_parametros = json.loads(parametros)

        self.update_last_time(j_parametros["ahora"],j_parametros["ip"])
        
    def filtered_out(self,conexion,ip):
        lista=[]
        
        global message_list
        global users_list
        for mensaje in message_list:
            if mensaje["hora"] >= conexion:
                if mensaje["direccion"] == ip:
                    u = "[YO..][{}]".format(mensaje["hora"])
                    msg = {"user":u,"mensaje": mensaje["mensaje"]}
                    json_datos = json.dumps(msg)
                    lista.append(json.loads(json_datos))
                else:
                    for usu in users_list:
                        if usu["ip"]==mensaje["direccion"]:
                            u = "[{}][{}]".format(usu["usuario"], mensaje["hora"])
                            msg = {"user":u,"mensaje": mensaje["mensaje"]}
                            json_datos = json.dumps(msg)
                            lista.append(json.loads(json_datos))
        return lista     

    def verify_user(self,ip):
        usuario=Usuario()
        return usuario.verify_User(ip)
    
    def register_user(self,ip,usuario):
        usu=Usuario()
        return usu.register_User(ip,usuario)
        
        

    
    def update_last_time(self,ahora,ip):
        u=Usuario()
        u.update_Last_Time(ahora,ip)
    
    def update_Users():
        user=Usuario()
        global users_list
        global ip_list
        ip_list=[]
        while True:
            listas=user.getUsers()
            users_list=listas[0]
            ip_list=listas[1]
            print(users_list)

            time.sleep(2)
    hilo_usuarios=threading.Thread(target=update_Users, daemon=True)
    hilo_usuarios.start()

if __name__ == '__main__':
    from http.server import HTTPServer
    server = HTTPServer((ip_server, 8000), GetHandler)
    print("SERVIDOR CORRIENDO....")
    server.serve_forever()
