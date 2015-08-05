Bitseal-Server
=======

Bitseal is a [Bitmessage](https://bitmessage.org) client for Android. 

Bitseal Server is a slightly modified version of [PyBitmessage](https://github.com/bitmessage/pybitmessage).

<img src=https://i.imgur.com/DmkWNqe.png" align="left" height="399" width="800" vspace="20">

---------------
**See also Bitseal's main respository: [https://github.com/JonathanCoe/bitseal](https://github.com/JonathanCoe/bitseal)**

Instructions for setting up bitseal-server
---------------

1) Download the zip file of the source code from Github

2) Extract the source code files to the desired location on your server

3) Run bitseal-server.py

4) After a few seconds, stop bitseal-server. The program will have created a keys.dat file, which you can now use to specify your API settings

5) Open the keys.dat file in a text editor. On Linux systems it will be located at "~/.config/bitseal-server". On Windows systems it will be located at "%APPDATA%\bitseal-server". On OSX systems it will be located at "~/Library/Application Support/bitseal-server".  

6) Add the following lines to the "bitmessagesettings" section of the keys.dat file, replacing the port number, username, and password values as appropriate (port 8447 is suggested as a default choice):  

```
daemon = true
apienabled = true
apiport = YOUR_API_PORT_NUMBER
apiinterface = 0.0.0.0
apiusername = YOUR_API_USERNAME
apipassword = YOUR_API_PASSWORD
```  
                    
7) Save and close the keys.dat file

8) Ensure that your server's firewall is set up allowing incoming + outgoing TCP connections on port 8446 (bitseal-server default) and the API port you specified in the keys.dat file

9) Run bitseal-server.py

10) Open Bitseal and add your server's URL, API username, and API password via the 'Server Settings' page

11) Done!



License
---------------
Copyright 2014, 2015 Jonathan Coe

Licensed under the [Gnu General Public License Version 3](https://www.gnu.org/licenses/gpl-3.0.html).
