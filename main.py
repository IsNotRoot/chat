from cliente import *
import time,threading
from os import system
class Principal:
    def __init__(self):
        global cliente
        cliente = Cliente()

        res=cliente.verify_user()
        if res=="True":
            hilo_update_last_time=threading.Thread(target=cliente.update_last_time, daemon=True)
            hilo_update_last_time.start()

            hilo1 = threading.Thread(name='show', target=self.receive_msgs_users, daemon=True)
            hilo1.start()
            while True:
                self.send_msg()
        else:
            print("Usted no esta Registrado por favor registrese")
            u=input("Nombre del Usuario:  ")
            res=cliente.register_user(u)
            if res=="True":
                
                hilo_update_last_time=threading.Thread(target=cliente.update_last_time, daemon=True)
                hilo_update_last_time.start()

                hilo1 = threading.Thread(name='show', target=self.receive_msgs_users, daemon=True)
                hilo1.start()
                while True:
                    self.send_msg()
            else:
                print("Lo sentimos no se pudo realizar el registro")
                
            
            
            
    def receive_msgs_users(self):
        cliente.recibir("si")

        
    def send_msg(self):
        try:
            msg=input()
            cliente.enviar(msg)
            cliente.recibir()

        except Exception as identifier:
            print("Error: ",identifier)
        
main=Principal()