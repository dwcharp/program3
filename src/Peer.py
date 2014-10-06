from MetaData import *
from QueryHelper import *
from DownloadHelper import *
from ServerUtil import *
import QueryMessage
import InvalidMessage
import InvalidMessage
import Pyro4
import threading
import socket
import FileServer
import Queue
import time

Pyro4.config.SERIALIZER = 'pickle'
Pyro4.config.SERIALIZERS_ACCEPTED.add('pickle')
TTL = 10
PULL = "pull"
PUSH = "push"

class Client():

    def __init__(self,id_num,mode):
        self.id_num = id_num
        self.meta_data = None
        self.download_folder = "downloads/"
        self.peers = dict()
        self.poll_mode = mode
        self.messages_received = dict()
        self.messages_sent = dict()
        self.files_to_download = dict()
        #message id = id_num + next_message_id
        self.next_message_id = 0
        self.next_invalid_message = 1000

        self.download_queue = Queue.Queue()

        self.name_server= Pyro4.locateNS()
        self.file_server = None
        self.ip_address = 9000 + int(id_num)
        self.client_daemon = None
        self.query_helper = QueryHelper(self)
        self.download_helper = DownloadHelper(self)
        self.server_helper = ServerHelper(self)

    ####

      #### This intiates the Search
    def obtain(self,file_name):
        if self.meta_data.has_file(file_name):
            print "You have this file !!!"
            return
        self.generate_query(file_name)



    #### This is called to generate a new query for this client
    def generate_query(self,file_name):
        id = self.generate_next_message_id()
        Qmessage = QueryMessage.QueryMessage(self.generate_next_message_id(),TTL,file_name,self.ip_address)
        self.query(Qmessage)

    def generate_next_message_id(self):
        mId = str(self.id_num) + str(self.next_message_id)
        self.next_message_id = self.next_message_id + 1
        return mId


    def query(self,qmessage):
        self.query_helper.query(qmessage)

    ##### If peer as the file, send a hit query

    def send_hit_query(self,qmessage):
        self.query_helper.send_hit_query(qmessage)

    #### called from peer that is relaying a query message back
    def hit_query(self,qmessage):
        self.query_helper.hit_query(qmessage)



    #### put the job in the Queue
    def get_file(self,file_name,peer_port):
        if self.files_to_download.has_key(file_name) and peer_port in self.files_to_download[file_name]:
            self.download_queue.put((peer_port,file_name))
            getter = threading.Thread(target= self.download_file)
            getter.start()
            print "Starting download thread"
            return True
        else:
            return False


    ##### This is called in a seperate Thread, pulla job from the queue and
    #####download into the test_files folder, let the index know u have it
    def download_file(self):
        self.download_helper.download_file()

    #### this called prior to a download
    def retrieve_file_info(self, file_name):
        return self.meta_data.get_file(file_name)

    #### Intially the peer id are taken in and the first
    #### the peer is contacted and the proxy will be generated and stored
    def add_peer(self,peer_id):
        #print "\nFrom client : " + str(self.id_num) + " adding peer : " + str(peer_id)
        peer_port = 9000 + int(peer_id)
        self.peers[peer_port] = None

    def get_peer_proxys(self):
        for id in self.peers.keys():
            uri = self.name_server.lookup(str(id))
            self.peers[id] = Pyro4.Proxy(uri)

    def get_addr(self):
        return (self.ip,self.port)

    def delete_file(self,file_name):
        self.meta_data.remove_file(file_name)
        #delete from disk

    def invalidate_message(self, imessage):
        self.query_helper.invalidate_message(imessage)

    def is_file_valid(self, file_name):
        return self.query_helper.is_file_valid(file_name)

    def invalidate_file(self, file_name):
        f = self.meta_data.invalidate_file(file_name)
        if not f :
            return False
        self.query_helper.generate_invalid_message(f)
        print "file now invalid"
        return True

    def validate_file(self,file_name):
        f = self.meta_data.validate_file(file_name)
        if not f :
            return False
        print "file now valid"
        return True


    def set_meta_data(self, meta_data):
        self.meta_data = meta_data
        self.meta_data.client = self

    def add_file(self,f):
        self.meta_data.add_file(f)
        if int(f.owner) != self.id_num and self.poll_mode == "pull":
            self.query_helper.set_timer_for_refresh(f.name, f.get_ttr())


    def list_files_on_index(self):
        print "Client: " + str(self.id_num) + " : " +  str(self.meta_data.list_files())

    def list_queries(self):
        for key in self.messages_sent.keys():
            print str(self.messages_sent[key]) + "\n"

    def set_poll_mode(self,mode):
        self.poll_mode = mode

    def start_client(self):
        daemon_thread = threading.Thread(target=self.server_helper.register_with_servers)
        daemon_thread.start()
        print "returning from start"

    def stop_client(self):
        self.file_server.stop_server()
        self.client_daemon.shutdown()
        print "Stopping client: " + str(self.id_num)




