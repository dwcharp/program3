class QueryMessage():
    """docstring for QueryMessage"""
    def __init__(self, messageId,TTL,file_name,sender_info):
        self.messageId = messageId
        self.TTL = TTL
        self.file_name = file_name
        self.sender_info = sender_info
