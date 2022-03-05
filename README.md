# Simple-Chat Final Project


<!-- TABLE OF CONTENTS -->
<details open="open">
  <summary>Content</summary>
  <ol>
    <li><a href="#about-the-project">About The Project</a></li>
    <li><a href="#plot-graph">System's Structure</a></li>
    <li><a href="#algorithms">Fast Reliable UDP Via Go-Back-N With CC</a></li>
    <li><a href="#code-details">Code Details</a></li>
    <li><a href="#how-to-run">How  to run</a></li>
    <li><a href="#languages-and-tools">Languages and Tools</a></li>
    <li><a href="#acknowledgements">Acknowledgements</a></li>
    <li><a href="#contact">Contact</a></li>
  </ol>
</details>

----------------

<!-- ABOUT THE PROJECT -->
# About The Project
**_A final project in a communication and computing course_**

In this project we had to design a system of a primitive instant messaging, 
like whatsapp, messanger, etc., which based on communication. In addition, 
we had to append a file transferring layer above UDP, with CC (i.e. congestion control)
and applying an RDT (i.e. reliable data transfer) protocol, such as: 'stop and wait', 'go back N', and so on... 


----------------

<!-- System's Structure -->
## System's Structure
This is a glance from above of the server's architecture. 
<p align="center">
<a href="https://gifyu.com/image/SMWtE"><img src="https://s7.gifyu.com/images/Screenshot_35607dc5643cf3c59.png" alt="Screenshot_35607dc5643cf3c59.png" border="0" /></a>
</p>

###Explanation of Server's Architecture 

In the server there exist a listening unit, which waits for user connections.
In addition, there is also a client's service unit, which provides 
thread for each user that has just connected to the server. In this 
thread, the latter serves the client for some features the server provides.
The methods which enable this client's treatment by the logic unit.
In order to figure out what the client's message exactly says, 
the data analysis unit will analyze client's message following the protocol.

- For some more information about the protocol, click [here](put here a link)


###Explanation of Client's Architecture 

This is a glance from above of the client's architecture. 

<p align="center">
<a href="https://gifyu.com/image/SMWtG"><img src="https://s7.gifyu.com/images/Screenshot_47ddc60a39f32fdc4.png" alt="Screenshot_47ddc60a39f32fdc4.png" border="0" /></a></p>

The existed units for the client are similar to those of the server. There is 
an analyzing unit of server's updates and responses. Additionally, there is 
a logic unit which responsible for making queries that are corresponding to 
the commands arrived from the graphical interface (GUI). The logic
unit uses methods to make the queries according to the client's interest,
these queries will be analyzed in server's side, and the latter
returns a corresponded response, following the protocol, back to the logic unit.
---
##Fast Reliable UDP Via Go-Back-N With CC
<p align="center">
<img align="center" src="https://s7.gifyu.com/images/Fast_realble_UDP_with_CC.drawio-2.png" />
</p>

---

<!-- code-details -->

## Code Details


Unified Modeling Language (UML) :

Click the image for zoom in.

// Put a picture right here 

<p align="center">
<img align="center" src="" />
</p>


---------

<!-- how-to-run -->
# How to run


First, it's important to make sure you clone this project in Pycharm through Terminal.
To be sure:
```
https://github.com/amirg00/Simple-Chat.git
```
Now, there are two directories: Server and Client.  

**Running The Server**

In order to run the server, either run **main.py** in **Server** directory, or run through terminal and write 
the following command: 

```
Simple-Chat/Server/main.py
```


**Running The Client**

In order to run the server, either run **GUI.py** in **Client** directory,
but then you **can't** run multiple clients, or run through terminal and then for 
multiple clients run the command many times you want to. 
 
To run the client through terminal write the following command: 

```
Simple-Chat/Client/GUI.py
```

###Running Example

Such an example can be found in the project book. 

We will first run the server.

<p align="center">
<img align="center" src="https://s7.gifyu.com/images/Screenshot_9.png" />
</p>

Now, let's run a client and connect to the server by filling the details correctly, and after pressing the connect button.


<p align="center">
<img align="center" src="https://s7.gifyu.com/images/Screenshot_103154d41d5317d169.png" />
</p>

And the client has successfully connected, we can of course
run another client with the terminal as the done previously. 

<p align="center">
<img align="center" src="https://s7.gifyu.com/images/Screenshot_7a2cf794903b3c8bd.png" />
</p>

We will fill up the details (ip_address = 127.0.0.1, port = 13337, and username - could be whatever we want, e.g. BOB ) and click the Connect button.


<p align="center">
<img align="center" src="https://s7.gifyu.com/images/Screenshot_146705e437e86b6412.png" />
</p>

We are finally connected to the server, and can now send and receive 
messages, etc...


_**Python Version:**_ ```3.9```

---------


## Languages and Tools

 <div align="center">
 <code><img height="40" width="40" src="https://upload.wikimedia.org/wikipedia/commons/thumb/c/c3/Python-logo-notext.svg/1200px-Python-logo-notext.svg.png"></code>  <code><img height="40" width="70" src="https://upload.wikimedia.org/wikipedia/commons/d/d5/UML_logo.svg"/></code>
 <code><img height="40" width="40" src="https://upload.wikimedia.org/wikipedia/commons/thumb/1/1d/PyCharm_Icon.svg/1024px-PyCharm_Icon.svg.png"/></code>
 <code><img height="40" width="40" src="https://raw.githubusercontent.com/github/explore/80688e429a7d4ef2fca1e82350fe8e3517d3494d/topics/git/git.png"></code>
 <code><img height="40" width="40" src="https://raw.githubusercontent.com/github/explore/80688e429a7d4ef2fca1e82350fe8e3517d3494d/topics/terminal/terminal.png"></code>
 <code><img height="40" width="40" src="https://upload.wikimedia.org/wikipedia/commons/b/b6/PuTTY_icon_128px.png"></code>
 <code><img height="40" width="40" src="https://media.trustradius.com/product-logos/dT/3e/JWKABGMWXUZ3.PNG"></code>
 </div>


<!-- ACKNOWLEDGEMENTS -->
## Acknowledgements
* [Our Protocol](https://docs.google.com/document/d/1jNmEHspdIJdHrGw9TxRJ0lU0Rt1J5uhz/edit?usp=sharing&ouid=110205518348656225965&rtpof=true&sd=true)
* [Python](https://www.python.org/)
* [PuTTYtm](https://en.wikipedia.org/wiki/PuTTY)
* [Wirshark](https://he.wikipedia.org/wiki/Wireshark)
* [UML](https://en.wikipedia.org/wiki/Unified_Modeling_Language)
* [Git](https://git-scm.com/)
* [Pycharm](https://www.jetbrains.com/pycharm/)
* [Git-scm](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)


<!-- CONTACT -->
## Contact <small>[Top▲](object-oriented-programming-exercise-3)</small>


 Amir - [here](https://github.com/amirg00/)
 
 Simcha - [here](https://github.com/SimchaTeich)

Project Link: [here](https://github.com/amirg00/Simple-Chat)

___

Copyright © _This Project last modified on March 5, 2022, by [Amir](https://github.com/amirg00/) & [Simcha](https://github.com/SimchaTeich)_.
