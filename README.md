## Sneaky Snake
[![codecov](https://codecov.io/gh/phildenhoff/hirethissnake/branch/master/graph/badge.svg?token=loYR0W8K2L)](https://codecov.io/gh/phildenhoff/hirethissnake) [![Build
Status](https://travis-ci.com/phildenhoff/hirethissnake.svg?token=zfsf2J47jwdz7GuKxCSd&branch=master)](https://travis-ci.com/phildenhoff/hirethissnake)

An Battlesnake AI implementation based heavily on graphing. Written by Phil Denhoff, Daniel Frankcom, Eric Showers, Kyle Thorpe, and Alex Welsh-Piedrahita, on Python 3.5.

Current feature list is in the `features.md` file. 

### Installation

#### Docker - Windows / Linux / Mac

You'll have to install [Docker](https://www.docker.com/) yourself, however once
that is done installation and execution is relatively simple. The basic concept
is that you install a Docker container which has all the required files
built into it, so you don't have to worry about having the right version of
Python on this project, and another project, all at once.

For now, you'll have to *build* the docker image on your local machine - soon
you'll (hopefully) be able to build to container pre-built for you.

First, git clone this repository to your local machine (using command line or
a GUI). In command line, traverse to the the directory. Then build the docker
image.

```
docker build -t hirethissnake .
```

`docker` initiates the docker program, build is the instruction to create an
image, -t designates the name of the image, and we use '.' to say 'look for
a Dockerfile in the current folder'.


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

#### Unsupported / Outdated

To run the server on Windows, on Python 2.7, you required the Microsoft Visual
C++ compiler available here: [aka.ms/vcpython27](http://aka.ms/vcpython27).

The required Python packages are listed in `requirements.txt`. They can be batch installed, as an administrator (use sudo), with

```
pip install -r requirements.txt
```

and python-igraph can be installed by following instructions at
[python-igraph install](http://igraph.org/python/#pyinstall). For Windows, use Christoph Gohlke's unofficial installers (pick \*-cp27), and

```
python -m pip install /path/to/igraph.whl
```

### Running

#### Docker
Following the successful completion of `docker build`, we will need to actually
run the container with our current code. One of the issues is that we want
a constant base-system (Python with required packages) but constantly changing
files. We manage this by mounting a *volume* a volume in docker. Issue this
command:

**Linux / Mac**
```
docker run -p 8080:8080 -v$(pwd)/app:/data/app hirethissnake python
/data/app/main.py
```

**Windows - Command Prompt**
```
docker run -p 8080:8080 -v%cd%/app:/data/app hirethissnake python /data/app/main.py
```

**Windows - Power Shell**
```
docker run -p 8080:8080 -v $pwd/app:/data/app hirethissnake python /data/app/main.py
```

Oh boy, there is a lot to unpack here. What are all these things? Why do
Windows and Linux / Mac have different commands?

In a list:

 - docker : runs docker on CLI
 - run : execute an image (either start it and keep it started, or execute
   command in that environment)
 - -p 4000:8080 : Pass all data from port 4000 on the host computer into the
   docker image on port 8080, and vice-versa. 4000 can be changed on the CLI,
but 8080 is the port that main.py executes on.
 - -v$(pwd)/app:/data/app : (**Linux**) The command is roughly the same on
   Windows. $(pwd) == %cd%, and returns the current location of the terminal.
-v tells Docker to mount the folder before the colon (":") from the host
computer to the folder after the colon on the Docker image. In this way, files
located at %cd%/app are available inside the image at /data/app everytime you
run the command, instead of having to re-build the image.
 - hirethissnake : the name of the image. This can be changed, and if you have
   many images, should be changed.
 - python /data/app/main.py : This command is passed along to the Docker image,
   and is executed inside its environment. It runs the
server.

You can now make any changes you'd like to the local files in ./app and then
run the `docker run` command above, and see those changes represented.

#### Manually
To run the server, execute

```python
python app/main.py
```

and then test the client in your browser: [http://localhost:8080](http://localhost:8080)

## Questions?

Email [phildenhoff@gmail.com](mailto:phildenhoff@gmail.com).
