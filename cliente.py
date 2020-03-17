import http.client,json,socket,time
from os import system
import os
import ip,threading
from datetime import datetime,timedelta

class Cliente:

    def __init__(self):
        global conexion,var
        self.conexion=time.strftime("%H:%M:%S")
        self.headers = {'Content-type': 'application/json'}
        if os.name == "posix":
            self.var="clear"
        elif os.name == "ce" or os.name == "nt" or os.name == "dos":
            self.var="cls"

    
    def enviar(self, dato): 
                     
        fecha = time.strftime("%d/%m/%y")
        hora = time.strftime("%H:%M:%S")
        datos = {"direccion": ip.getIp(),"mensaje": dato, "fecha": fecha, "hora": hora}
        json_datos = json.dumps(datos)
        connection = http.client.HTTPConnection('192.168.0.179', 8080, timeout=10)
        connection.request('POST', '/add_message', json_datos, self.headers)
        connection.close()

    def recibir(self,opc="no"):
        if opc=="si":
            while True:
                system(self.var)
                self.request_messages()
                self.request_users()
                time.sleep(5)
        elif opc=="no":
                system(self.var)
                self.request_messages()
                self.request_users()

            
            
    def request_messages(self):
        num_msg=0
        connection = http.client.HTTPConnection('192.168.0.179', 8080, timeout=10)
        headers = {'Content-type': 'application/json'}

        datos = {"direccion": ip.getIp(),"conexion": self.conexion}
        json_datos = json.dumps(datos)
        
        connection.request("GET", "/messages",json_datos,headers)
        response = connection.getresponse()
        datos = response.read().decode("utf-8")
        mensajes = json.loads(datos)
        if num_msg < len(mensajes):
            num_msg = len(mensajes)
            #system("clear")
            Tabla = """\
+---------------------------------------------------------------------+
|    Usuario-Hora                                Mensaje              |
|---------------------------------------------------------------------|
{}
+---------------------------------------------------------------------+\
"""
            Tabla = (Tabla.format('\n'.join("| {0:<30} {1:>36} |".format(fila["user"],fila["mensaje"])for fila in mensajes)))
            print (Tabla)
                


            connection.close()
            
    def request_users(self):
        connection = http.client.HTTPConnection('192.168.0.179', 8080, timeout=10)
        headers = {'Content-type': 'application/json'}
        #while True:
            #time.sleep(6)
        url="http://192.168.0.179:8080"
        connection.request("GET", "/users")
        response = connection.getresponse()
        datos = response.read().decode("utf-8")
        users = json.loads(datos)
        ya=datetime.now()

        for user in users:
            hr=user["hora"] 
            datetime_object = datetime.strptime(hr, '%Y-%m-%d %H:%M:%S.%f')
            diferencia=ya-datetime_object
            segundos = diferencia / timedelta(seconds=1)  
            hro=str(datetime_object).split(" ")
            hh=hro[1].split(".")
            h=hh[0]
            if segundos>10:
                print ('{3}{0:21s}{3} {3}{1:21s}{3} {3}{2:21s}'.format("Usuario: "+user["usuario"],"Estado: "+"\033[1;31m"+ "offline"+"\033[0;m","conectado a las: "+h, '|'))
            elif segundos <=10:
                print ('{2}{0:21s}{2} {2}{1:21s}{2}'.format("Usuario: "+user["usuario"],"Estado: "+ "\033[1;34m"+ " online"+"\033[0;m", '|'))

                      
        connection.close()
    
    def update_last_time(self):
        p=0
        connection = http.client.HTTPConnection('192.168.0.179', 8080, timeout=10)
        headers = {'Content-type': 'application/json'}
        while True:
            ahorita = datetime.now()
            datos = {"ahora": str(ahorita),"ip":ip.getIp()}
            json_datos = json.dumps(datos)
            connection.request("PUT", "/update_last_time",json_datos)
            connection.close()
            time.sleep(2)
            if p==0:
                self.recibir()
            p=p+1

    def verify_user(self):
        connection = http.client.HTTPConnection('192.168.0.179', 8080, timeout=10)
        headers = {'Content-type': 'application/json'}

        datos = {"direccion": ip.getIp()}
        json_datos = json.dumps(datos)
        
        connection.request("GET", "/verify_user",json_datos,headers)
        response = connection.getresponse()
        respuesta = response.read()
        a=respuesta.decode("utf-8")
        return a   
    
    def register_user(self,usuario):
        connection = http.client.HTTPConnection('192.168.0.179', 8080, timeout=10)
        headers = {'Content-type': 'application/json'}

        datos = {"direccion": ip.getIp(),"usuario":usuario}
        json_datos = json.dumps(datos)
        
        connection.request("POST", "/register",json_datos,headers)
        response = connection.getresponse()
        respuesta = response.read()
        a=respuesta.decode("utf-8")
        return a
        
             
        

      
    
