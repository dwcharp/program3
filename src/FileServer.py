import SocketServer
import threading
import os
#### Open the file and send it to the client, the file is known to exist
class FileServerHandler(SocketServer.StreamRequestHandler):
    def handle(self):
        test_folder = "test_files/"
        self.data = self.rfile.readline().strip()
        #print self.data + "\nfrom server !!!!"
        file_name = self.data
        try:
            f  = open(test_folder + file_name,"r")
            self.data = f.read()
            self.request.sendall(self.data)
        finally:
            f.close()


class ThreadFileServer(SocketServer.ThreadingMixIn,SocketServer.TCPServer):
    pass

class FileServer():
    def __init__(self,client):
        self.client = client
        self.server = None

    def start_server(self):
        HOST, PORT = "localhost",self.client.ip_address
        self.server = ThreadFileServer((HOST,PORT),FileServerHandler)
        server_thread = threading.Thread(target=self.server.serve_forever)
        server_thread.daemon = True
        server_thread.start()
        return self.server.server_address

    def stop_server(self):
        self.server.shutdown()


def main():
    server = FileServer(None)
    print server.start_server(9999)
    # Exit the server thread when the main thread terminates
    while True:
        pass

if __name__ == '__main__':
    main()





