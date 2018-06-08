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

### Register own commands
To register your own command inside the server, add it to the commands list inside src/commands/Command.py

    NAOCommand.lst.append( yourmodule.YourClass() )

Also add your commands class name to the src/commands/usrcommands/__init__.py

## Protocol
Communication server accepts JSON formatted data over UDP connections. Multiple clients can connect to a server. And the server automatically creates a socket on every network interface available.
Every data request package send to the server has to look like this:

    {'command': '<COMMAND>', 'commandArguments': [:<ARGS>]}
    
command must be a valid command string. commandArguments can also be an empty list if no command arguments are used.

After establishing connection, the server waits for a SYS_CONNECT command (see build-in commands below).
On every request the server sends back a data response packege containing following information:

    {
        'request': <request data package>,
        'requestSuccessfull': <true if command was executed successful>,
        'revision': <communication servers revision>,
        'naoName': <robots name>,
        'batteryLevel': <battery level>,
        'lifeState': <robots life-state>,
        'stiffnessData': <dictionary of robots joint stiffnesses>,
        'audioData': <dictionary of robots audio data>,
        'customMemoryEvents': <dictionary of custom memroy events> }
    }

Hint: IPv6 addresses are used, but currently are (why ever) not working!

### Build-in commands
The following commands are hard programmed inside the server.

* SYS_CONNECT: For connection handshake with server. Has to be send after connecting to the server.
* SYS_DISCONNECT: To disconnect from server
* SYS_SET_REQUIRED_DATA: Set required system data.
Requires an array of string as arguments to define system data that should be send.
Following values are accepted.
    * stiffnessData: stiffness data of joints
    * masterVolume: system overall sound volume
    * playerVolume: audio player volume
    * speechVolume: voice volume
    * speechVoice: selected voice name
    * speechLanguage: selected voice language
    * speechLanguagesList: list of available languages
    * speechVoicesList: list of available voices
    * speechPitchShift: pitch shift of text-to-speech
    * speechDoubleVoice: double voice value
    * speechDoubleVoiceLevel: double voice effect level
    * speechDoubleVoiceTimeShift: double voice time shift value 
* SYS_GET_INFO: Request to send system information

Hint: some system data, like battery level, will always be transmitted.