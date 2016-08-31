****************
Economy Minigame
****************
Playtest and refine a set of ideas for how the economy should work in seacow.  
The basic idea revolves around players investing in various industries.  The 
return on investment the players receive from each industry depends on what is 
happening in the game, and in particular how other players are investing.  The 
goal is to create an economic system in which the players are competing with 
each other as directly as possible.

.. image:: https://img.shields.io/travis/kxgames/seacow_economy_minigame.svg
   :target: https://travis-ci.org/kxgames/seacow_economy_minigame

.. image:: https://img.shields.io/coveralls/kxgames/seacow_economy_minigame.svg
   :target: https://coveralls.io/github/kxgames/seacow_economy_minigame?branch=master

Installation
============
The basic step to install the minigame are to clone the repository, create a 
``python3`` virtual environment, and to build the game using ``pip`` in 
editable mode::

   $ git clone https://github.com/kxgames/seacow_economy_minigame
   $ cd seacow_economy_minigame
   $ virtualenv -p python3 --system-site-packages env
   $ pip install -e .

The game must be installed in a virtual environment to avoid name conflicts 
with other ``kxg`` minigames.  The reason is that the code is installed into a 
package called ``src`` to work around a limitation in ``pip``.  Because other 
minigames use the same work-around, you cannot have two minigames installed in 
the same environment.

Usage
=====
Installation creates an executable called ``economy_minigame`` in the virtual 
environment.  Activate the environment if it isn't configured to activate 
itself automatically, then run the executable::

   $ economy_minigame --help
   Run a game being developed with the kxg game engine.
   
   Usage:
       economy_minigame sandbox [<num_ais>] [-v...]
       economy_minigame client [--host HOST] [--port PORT] [-v...]
       economy_minigame server <num_guis> [<num_ais>] [--host HOST] [--port PORT] [-v...] 
       economy_minigame debug <num_guis> [<num_ais>] [--host HOST] [--port PORT] [-v...]
       economy_minigame --help

   Commands:
       sandbox
           Play a single-player game with the specified number of AIs.  None of 
           the multiplayer machinery will be used.
   
       client
           Launch a client that will try to connect to a server on the given host 
           and port.  Once it connects and the game starts, the client will allow 
           you to play the game against any other connected clients.
   
       server
           Launch a server that will manage a game between the given number of 
           human and AI players.  The human players must connect using this 
           command's client mode.
   
       debug
           Debug a multiplayer game locally.  This command launches a server and 
           the given number of clients all in different processes, and configures 
           the logging system such that the output from each process can be easily 
           distinguished.
   
   Arguments:
       <num_guis>
           The number of human players that will be playing the game.  Only needed 
           by commands that will launch a multiplayer server.
   
       <num_ais>
           The number of AI players that will be playing the game.  Only needed by 
           commands that will launch a single-player game or a multiplayer server.
   
   Options:
       -x --host HOST          [default: localhost]
           The address of the machine running the server.  Must be accessible from 
           the machines running the clients.
   
       -p --port PORT          [default: 53351]
           The port that the server should listen on.  Don't specify a value less 
           than 1024 unless the server is running with root permissions.
   
       -v --verbose 
           Have the game engine log more information about what it's doing.  You 
           can specify this option several times to get more and more information.
   
   ...
