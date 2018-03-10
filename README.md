## hirethissnake 2018 
[![codecov](https://codecov.io/gh/phildenhoff/hirethissnake/branch/master/graph/badge.svg?token=loYR0W8K2L)](https://codecov.io/gh/phildenhoff/hirethissnake) [![Build Status](https://travis-ci.org/hirethissnake/2018.svg?branch=master)](https://travis-ci.org/hirethissnake/2018)

A Battlesnake AI based heavily on graphing algorithms. Written in Python 3.7 by Daniel Frankcom, Eric Showers, Kyle Thorpe, and Phil Denhoff, with contributions from Alex Welsh-Piedrahita.

### Installation

#### Docker - Windows / Linux / Mac

You'll have to install [Docker](https://www.docker.com/) yourself, however once
that is done installation and execution is relatively simple. The basic concept
is that you install a Docker container which has all the required environment to
run this project without installing a different version of Python, plus all the
required packages.

For now, you'll have to build the docker image on your local machine - soon
you'll (hopefully) be able to download a pre-built image.

First, git clone this repository to your local machine (using command line or
a GUI). In command line, traverse to the the directory. Then build the docker
image using this command

```
docker build -t hirethissnake .
```

`docker` initiates the docker program, build is the instruction to create an
image, -t designates the name of the image, and we use '.' to say 'look for
a Dockerfile in the current folder'.

Go to [Running](#running) to see how to use the program.

#### Script - Linux Only

An installer file is provided to run the download the repo and all neccessary
packages and programs to run the server. Currently only Linux is supported.

Download the `install.sh` file to your local server, where you'd like to the
`hirethissnake` folder. Add execution permissions to the script and execute it.
It will ask for your password to sudo-install some packages, and will request
your github credentials to access the repo if it's private. Please feel free to
expect the installer if you aren't comfortable with that, or do those steps
yourself.

```bash
chmod +x ./install.sh
./install.sh
```

### Running

#### Docker
Following the successful completion of `docker build`, we will need to actually
run the container with our current code. One of the issues is that we want
a constant environment (Python with required packages) but constantly changing
source code. We manage this by mounting a volume in docker. Run this command:

**Linux / Mac**
```
docker run --rm -it -p 8080:8080 -v $(pwd)/app:/data/app -v $(pwd)/static:/data/static hirethissnake python "-mapp.main"
```

**Windows - Command Prompt**
```
docker run --rm -it -p 8080:8080 -v %cd%/app:/data/app -v $(pwd)/static:/data/static hirethissnake python "-mapp.main"
```

**Windows - Power Shell**
```
docker run --rm -it -p 8080:8080 -v $pwd/app:/data/app -v $(pwd)/static:/data/static hirethissnake python "-mapp.main"
```

Oh boy, there is a lot to unpack here. What are all these things? Why do
Windows and Linux / Mac have different commands?

In a list:

 - docker : Runs docker on CLI
 - run : Execute an image (either start it and keep it started, or execute
   command in that environment)
 - --rm : Deletes the container when it closes (to keep your comptuter clean)
 - -it : Make the container interactive, so we can see what's going on!
 - -p 4000:8080 : Pass all data from port 8080 on the host computer into the
   docker image on port 8080, and vice-versa. 8080 can be changed on the CLI,
but 8080 is the port that main.py executes on.
 - -v $(pwd)/app:/data/app : (**Linux**) The command is roughly the same on
   Windows. $(pwd) == %cd%, and returns the current location of the terminal.
-v tells Docker to mount the folder before the colon (":") from the host
computer to the folder after the colon on the Docker image. In this way, files
located at %cd%/app are available inside the image at /data/app everytime you
run the command, instead of having to re-build the image.
 - hirethissnake : The name of the image. This can be changed, and if you have
   many images, should be changed.
 - python "-mapp.main" : This command tells the docker image that we would like to use the python executable, and that we would like to run the file in the 'app' module called 'main'. This file is then executed inside its environment, running the server.

You can now make any changes you'd like to the local files in ./app and then
run the `docker run` command above, and see those changes represented.

#### Manually
To run the server, execute

```
python app/main.py
```

and then test the client in your browser: [http://localhost:8080](http://localhost:8080)

#### Docker Compose
For advanced users, we have included a `docker-compose.yml` file which is currently set up to pit 3 of our snakes against each other.

The primary usecase for this is currently using the included batch game server found at `utilities/batchserver/`. The `docker-compose.yml` file can easily be modified to run 1 snake, or for that matter any number of snakes providing the user has a basic understanding of the Docker Compose syntax. Additionally, it is not directly tied to the batch server in any way, and simply makes the various snake URLs available for access however you see fit. 

In order to run the snake in this manner, [Docker Compose](https://docs.docker.com/compose/) must be installed.

First, build the snake image as instructed in the [Installation](#installation) section.

Then run the following command to start the snakes

```
docker-compose up
```

## Questions?

Please email any questions you have to [phildenhoff@gmail.com](mailto:phildenhoff@gmail.com) and he'll make sure they get to the right person.
