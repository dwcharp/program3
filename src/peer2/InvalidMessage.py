class InvalidMessage() :
    def __init__(self, msg_id, origin_server, file_name, version_id) :
        self.msg_id = msg_id
        self.origin_server = origin_server
        self.file_name = file_name
        self.version_id = version_id
