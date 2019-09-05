# import socket, struct
# import django.apps
# from time import sleep
#
# class ServerApp:
#     def __init__(self):
#         self.UDP_PORT = 7777
#         self.UDP_HOST = 'localhost'
#         print("At least i'm alive!")
#
#
#     def run(self):
#         addr = (self.UDP_HOST,self.UDP_PORT)
#         print(addr)
#
#         server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#         #server.settimeout(20)
#         server.bind((self.UDP_HOST, self.UDP_PORT))
#         while (True):
#             try:
#                 data = server.recvfrom(25)
#                 received = data[0]
#                 addr = data[1]
#                 print(received.decode('utf-8'))
#                 if(received!= None):
#                     msg = "OK"
#                     server.sendto(msg.encode('utf-8'), addr)
#                     continue
#             except socket.timeout:
#                 server.close()
#                 return

# UDP_SERVER = ServerApp()
# UDP_SERVER.run()
# from receiver_app.apps import RESULT
# print(RESULT)
#
#
# while(True):
#     if django.apps.apps.ready:
#         try:
#             SERVER = ServerApp()
#             SERVER.run()
#         except:
#             print("Not ok")
#     else:
#         print("No")
#         sleep(1)