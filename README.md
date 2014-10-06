program3
========

Distributed Operating Systems peer system project


Manual :
The mode needs to be set in the PeerDriver.py file at the top
The only dependency that Python needs is PYRO4. This is include in the source folder. Navigate to the Pyro4 folder and run Python install( install like any other python module). This will install Pyro4.
For every directory that you are running the server and Peer in, include all of the .py files. I have made 2 peer folders with all of the necessary files. Just run python PeerDriver.py in each.
In the PeerDriver.py, the topology can be changed. This is towards the top of the file.
The PeerDriver also needs to be set to push or pull prior to operation.
The topology files are formatted as follows:
Mesh:
Peer1,n2,.... Peer2,n1....
Each Peer listing in the MESH topology needs to be symmetric for the clients. I.E ­> If peer1 knows about peer2, then the reverse needs to be true.
Before starting the Peers we will need to start the Pyro4 naming server. To do this enter the following 2 commands:
export PYRO_SERIALIZERS_ACCEPTED=pickle
python ­m Pyro4.naming
The first command uses pickling as the format for transferring the files. The second one starts the the naming server.
Now run the all of the Peers
All of the Peers need to be up before any system operation begins. Right now I have the configuration file to setup up 2 peers. Once all Peers are up, run get Peer proxies from the command line for each Peer. Once this is done, normal system operation can take place.
