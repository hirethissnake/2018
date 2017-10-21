## Sneaky Snake
[![codecov](https://codecov.io/gh/phildenhoff/hirethissnake/branch/master/graph/badge.svg?token=loYR0W8K2L)](https://codecov.io/gh/phildenhoff/hirethissnake) [![Build
Status](https://travis-ci.com/phildenhoff/hirethissnake.svg?token=zfsf2J47jwdz7GuKxCSd&branch=master)](https://travis-ci.com/phildenhoff/hirethissnake)

An Battlesnake AI implementation based heavily on graphing. Written by Phil Denhoff, Daniel Frankcom, Eric Showers, Kyle Thorpe, and Alex Welsh-Piedrahita, on Python 3.5.

Current feature list is in the `features.md` file. 

### Installation

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

To run the server, execute

```python
python app/main.py
```

and then test the client in your browser: [http://localhost:8080](http://localhost:8080)

## Questions?

Email [phildenhoff@gmail.com](mailto:phildenhoff@gmail.com).
