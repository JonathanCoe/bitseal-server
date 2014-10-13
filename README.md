Bitseal-Server
=======

[![tip for next commit](https://tip4commit.com/projects/1002.svg)](https://tip4commit.com/github/JonathanCoe/bitseal-server)

Bitseal is a Bitmessage client for Android, currently in Beta. 

The Bitseal server application is a slightly modified version of  [PyBitmessage](https://github.com/bitmessage/pybitmessage)

**See Bitseal's main respository: [https://github.com/JonathanCoe/bitseal](https://github.com/JonathanCoe/bitseal)**


Instructions for setting up bitseal-server
---------------

1) Download the zip file of the source code from Github

2) Extract the source code files to the desired location on your server

3) Run bitmessagemain.py

4) After a few seconds, stop PyBitmessage. PyBitmessage will have created a keys.dat file, which you can now use to specify your API settings

5) Open the keys.dat file. You can find its location using this reference: https://bitmessage.org/wiki/Keys.dat

6) Add the following lines to the "bitmessagesettings" section of the keys.dat file, replacing the port number, username, and password values as appropriate:  

```
daemon = true
apienabled = true
apiport = YOUR_API_PORT_NUMBER
apiinterface = 0.0.0.0
apiusername = YOUR_API_USERNAME
apipassword = YOUR_API_PASSWORD
```  
                    
7) Save and close the keys.dat file

8) Ensure that your server's firewall is set up allowing incoming + outgoing TCP connections on port 8444 (PyBitmessage default) and the API port you specified in the keys.dat file

9) Run bitmessagemain.py

10) Open Bitseal and add your server's URL, API username, and API password via the 'Server Settings' page

11) Done!



License
---------------
Copyright 2014 Jonathan Coe

Licensed under the [Gnu General Public License Version 3](https://www.gnu.org/licenses/gpl-3.0.html)


Support the project!
---------------
The development of Bitseal has been a large project, taking many months of work. I'm doing it on a purely non-profit basis. 

Bitcoin donations are very gratefully received: 
[**1L7amdWrPv4R4f1vLdanr2xU71TPs3wUEC**](https://www.blocktrail.com/address/1L7amdWrPv4R4f1vLdanr2xU71TPs3wUEC)
