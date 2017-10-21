#!/bin/bash
REPONAME="hirethissnake"

echo "You will need to provide sudo access to update and install some packages, as well as your GitHub credentials to download the repo.
Be warned: This installer produces a LOT of output."
read -p "Do you want to continue? (y/n) " -n 1 -r

if [[ $REPLY =~ ^[Yy]$ ]]
then

    # Download Python 3.5+, pip
    sudo apt-get update
    sudo apt-get install -y python3 python3-pip
    
    # Install Virtualenv and it's wrapper
    pip3 install virtualenv virtualenvwrapper

    # Add wrapper defaults to .bashrc and .zshrc
    # source .bashrc (or source .zshrc)
    SHELL="$(getent passwd $LOGNAME | cut -d: -f7)"
    RCFILE=""

    if [ "$SHELL" = "/usr/bin/zsh" ] || [ "$SHELL" = "/bin/zsh" ]
    then
        RCFILE="$HOME/.zshrc"
    elif [ "$SHELL" = "/usr/bin/bash" ] || [ "$SHELL" = "/bin/bash" ]
    then
        RCFILE="$HOME/.bashrc"
    fi

    if [ ! -e "$RCFILE" ]; then
        touch $RCFILE
        echo $RCFILE
    fi

    echo "Adding virtualenv variables to $RCFILE"
    source /usr/local/bin/virtualenvwrapper.sh
    echo "export PROJECT_HOME=$HOME/Devel" >> "$RCFILE"
    echo "export VIRTUALENVWRAPPER_PYTHON=/usr/bin/python3" >> "$RCFILE"
    echo "export VIRTUALENVWRAPPER_VIRTUALENV=/usr/local/bin/virtualenv" >> "$RCFILE"
    echo "export WORKON_HOME=$HOME/.virtualenvs" >> "$RCFILE"
    echo "source /usr/local/bin/virtualenvwrapper.sh" >> $RCFILE
    source $HOME/.bashrc
    mkdir -p $WORKON_HOME

    export PATH=/usr/local/bin:$PATH
    source $RCFILE

    # ask for virtualenv name (venvname)
    read -p "Input Virtual Environment Name: " VENVNAME

    # create virtualenv with name venvname
    mkvirtualenv $VENVNAME
    workon $VENVNAME
    
    # go into virtualenv
    find ./$REPONAME >> /dev/null
    if [ $? -eq 0 ]; then
        echo "File already exists"
        cd hirethissnake
    else
        git clone https://github.com/phildenhoff/$REPONAME.git
        cd hirethissnake
    fi
    pip install -r requirements.txt
fi

