import socket
class DownloadHelper:
    def __init__(self, client):
        self.client = client


##### This is called in a seperate Thread, pulla job from the queue and
#####download into the test_files folder, let the index know u have it
    def download_file(self):
        peer_port, file_name = self.client.download_queue.get()
        peer = self.client.peers[int(peer_port)]
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        f  = open(self.client.download_folder + file_name,"wb+")
        try:
            #print "\nConnecting to fileserver!!!!\n"
            sock.connect(("localhost",peer_port))
            sock.sendall(file_name + "\n")
            while 1:
                file_data = sock.recv(1024)
                if not file_data:
                    #print "\nData was empty"
                    break
                else:
                    #print file_data
                    f.write(file_data)
            file_meta = peer.retrieve_file_info(file_name)
            self.client.add_file(file_meta)

        finally:
            f.close()
            sock.close()
