from Peer import Client
from MetaData import *
import random
import string
import socket
import time
import Pyro4
import os

Pyro4.config.SERIALIZER = 'pickle'
Pyro4.config.SERIALIZERS_ACCEPTED.add('pickle')
MESH = "mesh.txt"
TOPOLGY = MESH
MODE = "pull"

#### This the driver class that helps run a client.


num_clients = 10
clients = []
max_file_size = 2000 #  max_file_size * file_name to keep things i.e "a" * 2 = "aa"
max_num_files = 15
file_names = []

def main():

    #create_random_file_names()
    #create_meta_data_files()
    createSingleClient(TOPOLGY)
    user_input()

####command prompt to allow a user to run a client
def user_input():
    got_peers = False

    prompt_with_invalidate = "1) List Files on this Server\n2) List Searches\n3) Search\n4) Download File\n5)Find Peers(Do this first!!)\n6) Invalidate file\n7) Validate file\n8) Stop Client\n"

    while True:
        print prompt_with_invalidate
        selection = raw_input("Enter your input: \n")

        if got_peers == False and not (selection =="5" or selection =="8") :
            print "Get your Peers first\n"
            continue

        if selection == "1":
            print "Your Files:"
            list_files_on_client()

        elif selection == "2" :
            print "Your Searches: \n"
            clients[0].list_queries()
            print "\n"

        elif selection == "3" :
            print "Which File: "
            fn = raw_input("Enter your input:\n")
            search(fn)

        elif selection == "4" :
            print "Which File: "
            f= raw_input("Enter your input:\n")
            pn = raw_input("From which Peer(port number):\n")

            if not get_file(f,int(pn)):
                print " \nThe file name or port is not valid!!!!!!\n"

        elif selection == "5" :
            clients[0].get_peer_proxys()
            got_peers = True

        elif selection == "6":
            fn = raw_input("Enter the file to invalidate:\n")
            clients[0].invalidate_file(fn)

        elif selection == "7":
            fn = raw_input("Enter the file to validate:\n")
            clients[0].validate_file(fn)

        elif selection == "8" :
            stop_clients()
            print "GoodBye\n"
            break




#### have the client download the file
def search(file_name):
    c1 = clients[0]
    print "Testing with file " + file_name
    c1.obtain(file_name)

def get_file(file_name,client_port):
    clients[0].get_file(file_name,client_port)


def list_files_on_client():
    clients[0].list_files_on_index()
    print "\n"

def delete_file(file_name):
    client = clients[0]
    client.delete_file(file_name)



def createSingleClient(file_name):
    filz  = open(file_name)
    clients_dict = dict()
    info = filz.readline()
    info = info.strip("\n")
    info = info.split(",")
    cID = info[0]
    del info[0]
    filz.close()

    client = Client(cID, MODE)
    client.set_meta_data(create_files(cID))
    client.start_client()
    #print info
    for neigbhor in info:
        client.add_peer(int(neigbhor))
    clients.append(client)

def get_client(id):
    ns  = Pyro4.locateNS()
    uri = ns.lookup(id)
    print uri
    return Pyro4.Proxy(uri)

def stop_clients():
    for client in clients:
        client.stop_client()

def create_random_file_names():
    names = []
    for i in range(num_clients * 4):
        file_name = "file" + str(random.randint(0,40))
        while file_name in names:
            file_name =  "file" + str(random.randint(0,40))
        random_size = random.randint(1,max_file_size)
        names.append(file_name)
        file_names.append((file_name,random_size))

def create_file_contents(size):
    s = ':)' * size
    return s

def create_files(client_id):
    #peer_folder = "peer" + str(client_id) + "/"
    meta_file_name = "meta_data_" + str(client_id)
    meta_file  = open(meta_file_name + ".txt")
    m_files = []
    client_files =[]

    while 1 :
        info = meta_file.readline()
        if not info:
            break
        else:
            info = info.strip("\n")
            info = info.split(",")
            file_name = info[0]
            size = info[1]
            m_files.append((file_name,size))
    meta_file.close()

    directory = "test_files/"
    if not os.path.exists(directory):
        os.mkdir(directory)

    if not os.path.exists("downloads/"):
        os.mkdir("downloads/")

    for f in m_files:
        file_name,size = f
        new_file = open(directory + file_name,"wb+")
        new_file.write(create_file_contents(int(size)) + "\n")
        new_file.close()
        client_files.append(FileInfo(file_name,size,time.localtime(),client_id))
    return MetaData(directory,client_files)


def create_meta_data_files():
    num_files_names = len(file_names) -1
    for i in range(3):
        files_picked = []

        file  = open("meta_data_" + str(i) + ".txt","wb+")
        for i in range(1, max_num_files +1):
            file_name,size = file_names[random.randint(0,num_files_names)]
            while file_name in files_picked:
                file_name,size = file_names[random.randint(0,num_files_names)]
            file.write(file_name +"," + str(size) + "\n")
            files_picked.append(file_name)
        file.close()



if __name__=="__main__":
    main()

