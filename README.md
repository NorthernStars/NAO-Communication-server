NAO-Communication-server
========================

Python server for NAO Communication project

Installation
------------
Copy content of src folder into new folder named naocom inside the home folder on the NAO (/home/nao/naocom).
Load the programms inside choregraphe folder with Choregraphe and upload them to your NAO. Set them as default and start them using Choregraphe.

The NAO-Com Android App (https://github.com/NorthernStars/NAO-Com) can install the server automatically.

Usage
-----
You can start the server using python command:

    python communication_server.py

You can use several command line arguments to configure the communication sevrer:

* -naohost      NAOqi hostname or IP (default localhost/127.0.0.1)
* -naoport      Port of NAOqi (default 9559)
* -serverip     IP the communication server should bind its socket to (default 127.0.0.1)
* -serverport   Port the communication server should open (default 5050)
* -servicetype  Network service type name to publish if communication server is running (default _naocom._tcp)
* -resenddelay  Delay between sending nao status information data to remote application in sec. (default 1.0)

If you want to modify the build in commands, it's recommended to install the communication server on a local computer and use the arguments above to connect to a remote NAOqi (simulated or real robot).

Implementig own commands
------------------------
The communication server already allows to stimulate custom ALMemory key values. The recommendes way to implement own features or commands is to add a custom ALMemory key any own program (Choreographe, Python, C++, ...) listens to.

All available commands of the communication server are implemented as python modules inside src/commands/usrcommands folder.
Each module needs to set the cmd attribute in its constructor:

    def __init__(self):
      self.cmd = "OPEN_HAND"

The cmd attribute defines the command that starts the module. For that it need to implement the following exe function:

    def exe(self, args=None, addr=None):

Where args are the commands arguments send from remote application and addr is the address/IP of the remote application.
Take a look at the build in commands as reference how to use these arguments.

To us a new command module, add it to the commands list inside src/commands/Command.py
