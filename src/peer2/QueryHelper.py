import Pyro4
import QueryMessage
import InvalidMessage
from threading import Timer

Pyro4.config.SERIALIZER = 'pickle'
Pyro4.config.SERIALIZERS_ACCEPTED.add('pickle')
class QueryHelper():
    def __init__(self,client):
        self.client = client

    #### This is called from other peers, and calls this on neigbhors

    def query(self, qmessage):
        messageId = qmessage.messageId
        file_name = qmessage.file_name
        TTL = qmessage.TTL
        sender_info = qmessage.sender_info

        if self.client.messages_received.has_key(messageId) or self.client.messages_sent.has_key(messageId):
            #print "Not sending query from " + str(self.client.ip_address)
            return
        else:
            if self.client.ip_address == sender_info:
                self.client.messages_sent[messageId] = [file_name]
            else:
                self.client.messages_received[messageId] = sender_info
        if TTL > 0:
            TTL = TTL -1
            Qmessage = QueryMessage.QueryMessage(messageId,TTL,file_name,self.client.ip_address)
            for peer in self.client.peers.values():
                peer.query(Qmessage)

        if self.client.meta_data.has_file(file_name) and not self.client.messages_sent.has_key(messageId):
            f = self.client.meta_data.get_file(file_name)
            if f.state == "valid":
                print "Sending a valid message"
                self.client.send_hit_query(Qmessage)
            else :
                print "Message is not valid"

   #### called from peer that is relaying a query message back
    def hit_query(self, qmessage):
        messageId = qmessage.messageId
        file_name = qmessage.file_name
        TTL = qmessage.TTL
        sender_info = qmessage.sender_info

        if self.client.messages_sent.has_key(messageId):
            #print str(sender_info) + " has the file from client " + str(self.client.ip_address)
            self.client.messages_sent[messageId].append(sender_info)
            if(self.client.files_to_download.has_key(file_name)):
                self.client.files_to_download[file_name].append(sender_info)
            else:
                self.client.files_to_download[file_name] = [sender_info]
            #print self.client.messages_sent[messageId]
        else:
            self.client.send_hit_query(qmessage)


##### If peer as the file, send a hit query

    def send_hit_query(self, qmessage):
        messageId = qmessage.messageId
        #print "Sending a Hit for: " + file_name + " from client: " + str(self.client.ip_address) + " orgin: " + str(sender_info)
        peer_info = self.client.messages_received[messageId]
        peer = self.client.peers[peer_info]
        peer.hit_query(qmessage)


####  These methods are used for push mode ####
    def invalidate_message(self, imessage):
        #if ive seen this message return
        #invalidate file if i have it

        messageId = imessage.msg_id
        if self.client.messages_received.has_key(messageId) or self.client.messages_sent.has_key(messageId):
            return
        sender_info = imessage.origin_server
        if self.client.ip_address == sender_info:
            self.client.messages_sent[messageId] = [imessage.file_name]
        else:
            self.client.messages_received[messageId] = sender_info

        self.client.meta_data.invalidate_file(imessage.file_name)

        self.send_invalid_message(imessage)

    def send_invalid_message(self, imessage):
        for peer in self.client.peers.values():
            peer.invalidate_message(imessage)

    def generate_invalid_message(self, f):
        im = InvalidMessage.InvalidMessage(self.client.generate_next_message_id(), self.client.ip_address,f.name, f.version_id)
        self.invalidate_message(im)


#### These methods are for pull mode ###

    def is_file_valid_on_origin(self, file_name):
        print "Asking server if file is valid"
        f = self.client.meta_data.get_file(file_name)
        peer_id = int(f.owner) + 9000
        peer = self.client.peers[peer_id]
        return peer.is_file_valid(file_name)



    def set_timer_for_refresh(self, file_name, TTR):
        print "setting timer for refresh"
        t = Timer(TTR, self.refresh_file,[file_name])
        t.start()

    def refresh_file(self, file_name):
        print "refreshing file"
        response = self.is_file_valid_on_origin(file_name)
        if response == -1:
            print "file was invalid"
            self.client.meta_data.invalidate_file(file_name)
        else:
            print "file was valid"
            self.client.meta_data.set_ttr(file_name,response)
            self.set_timer_for_refresh(file_name,response)


    def is_file_valid(self, file_name):
        print "someone calling for file state"
        f = self.client.meta_data.get_file(file_name)
        if f.state == "valid":
            return f.get_ttr();
        else:
            return -1



