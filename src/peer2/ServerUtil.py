import Pyro4
import FileServer
Pyro4.config.SERIALIZER = 'pickle'
Pyro4.config.SERIALIZERS_ACCEPTED.add('pickle')

class ServerHelper():
    def __init__(self, client):
        self.client = client


    #### This is started in a seperate thread ####
    def register_with_servers(self):
        self.client.client_daemon = Pyro4.Daemon()
        self.start_file_server()
        self.register_to_naming_server()
        self.client.client_daemon.requestLoop()

    def register_to_naming_server(self):
        client_uri = self.client.client_daemon.register(self.client)
        port = self.client.ip_address
        self.client.name_server.register(str(port),client_uri)


    def start_file_server(self):
        self.client.file_server = FileServer.FileServer(self.client)
        self.client.file_server.start_server()



def create_downloads_folder(self):
        cwd = os.getcwd()
        self.client.download_folder = download_folder = cwd + "/" + "downloads"
        if  not os.path.exists(download_folder):
            os.mkdir(download_folder)
        else:
            print "Folder exist"
