# DEVELOPERS

## Mike Simpson's setup (10/10/2016).

### Base platform.

My development environment is a recent-edition MacBook Pro, running MacOS X 10.11.6.

My command-line shell is Zsh 5.0.8 (as delivered by Apple).

I also use Eclipse 4.6.0 as my IDE, with a number of useful plugins (PyDev, Markdown, YEdit, etc.).

I'm also trying out SmartGit 8.0.2 for source code control GUI (but still use CLI Git a bunch as well).

### Initial project setup.

#### Installed pyenv and pyenv-virtualenv using administrator account.

    % brew update
    % brew install pyenv
    % brew install pyenv-virtualenv
    % vi .zshrc

        [ added magic lines to startup file and re-started terminal ]

#### Installed latest-version Python 3.5 under local account.

    % pyenv install 3.5.2

#### Created project-specific virtual environment.

    % pyenv virtualenv 3.5.2 ual-ireportedthis

#### Initialized project directory.

    % cd ~/Desktop/Professional/Projects
    % mkdir ual-ireportedthis
    % cd ual-ireportedthis
    % pyenv local ual-ireportedthis

        [ set up basic project structure with "setup.py" file ]
	
    % pip install -e .

### Initialized source code control.

    [ created "ualibraries/ireportedthis" repository on Github ]

    % git init
    % vi .gitignore

        [ added the usual suspects ]

    % git add [ ... ]
    % git commit -m "First commit and push to Github repository."
    % git remote add origin git@github.com:ualibraries/ireportedthis.git
    % git push -u origin master
