class MetaData():

#### This class represents it file that the Peers own
    def __init__(self,working_dir, files):
        self.working_directory = working_dir
        self.files = files
        self.client = None

    def set_peer(self, peer):
        self.client = peer

    def add_file(self,f):
        self.files.append(f)

    def get_file(self, file_name):
        for f in self.files:
            if f.name == file_name:
                return f
        return None

    def remove_file(self,file_name):
        for f in self.files:
            if f.name == file_name:
                print "Removing File"
                self.files.remove(f)

    def invalidate_file(self, file_name):
        f = self.get_file(file_name)
        if f:
            f.set_state("invalid")
        return f


    def validate_file(self, file_name):
        f = self.get_file(file_name)
        if f:
            f.set_state("valid")
        return f

    def set_ttr(self,file_name,ttr):
        f = self.get_file(file_name)
        f.set_ttr(ttr)


    def has_file(self,file_name):
        for f in self.files:
            if f.name == file_name:
                #print "Found File in Index"
                return True

    def list_files(self):
        f_names= []
        for file in self.files:
            f_names.append(file.name)
        f_names.sort()
        return f_names

class FileInfo():
    def __init__(self,name,size,time_last_modified,owner):
        self.size = size
        self.name = name
        self.TTR = 5
        self.version_id = 0
        self.owner = owner
        self.time_last_modified = time_last_modified
        self.state = "valid"

    def get_name(self):
        return self.name

    def get_size(self):
        return size

    def set_ttr(self, new_ttr):
        self.TTR = new_ttr

    def get_ttr(self):
        return self.TTR

    def get_owner(self):
        return self.owner

    def set_state(self,state):
        self.state = state

    def increment_version(self):
        self.version_id = self.version_id + 1
