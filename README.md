# NAO-Communication-server

Python server for NAO Communication project

## Installation
Copy content of src folder into new folder named naocom inside the home folder on the NAO (/home/nao/naocom).
Load the programms inside choregraphe folder with Choregraphe and upload them to your NAO. Set them as default and start them using Choregraphe.

The NAO-Com Android App (https://github.com/NorthernStars/NAO-Com) can install the server automatically.

## Usage
You can start the server using python command:

    python communication_server.py

You can use several command line arguments to configure the communication sevrer. Use following command for more information:

    python communication_server.py -h

## Implementing own commands
The communication server already allows to stimulate custom ALMemory key values.
The recommended way to implement own features or commands is to add a custom ALMemory key and let your own program (Choreographe, Python, C++, ...) listens to.

## Implementing own commands as command classes (alternative)
You can also create new build in commands. They are organized as own classes inside src/commands/usrcommands folder.
Each class needs to set the cmd attribute in its constructor. Like:

    def __init__(self):
      self.cmd = "OPEN_HAND"

The cmd attribute defines which command string starts the class.
If the server receives a command for a registered command class, it tries to start it's exe function as new thread.
The exe function receives optional command arguments and server object to be able to send a response. The functions header should look like this:

    def exe(self, args=None, server=None):
        # your code here

You can use the server object to send data back to the client using it's send function:

    server.send("your data string here")

Data can be any object that can be conferted into a string and that the remote client understands.

### Registering own commands
To register your own command inside the server, add it to the commands list inside src/commands/Command.py

    NAOCommand.lst.append( yourmodule.YourClass() )

Also add your commands class name to the src/commands/usrcommands/__init__.py

