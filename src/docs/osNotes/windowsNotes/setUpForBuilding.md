# Set Up For Building on Windows

Installing tools to set up for building the project.

## Install Chocolatey

Chocolatey is a package manager for Windows, similar to homebrew for macos, apt for debian linux based systems and yum/dnf for redhat based systems.

To install chocolatey, open an admin powershell, and run the following:

```
Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
```

To use chocolatey, close the powershell window, and open a new admin powershell window.

## Set up Chocolatey to run as a User

AI generated instructions for setting Chocolatey up to be used in a user environment - - [[chocolateyAsUser]]

This will be tested and modified as necessary once there is time for someone to go through the document.

## Install software required for the project

* python (not the latest version as pyside6 doesn't work with it)
* git
* obsidian
* favorite editor (project prefers positron)

### With Chocolaty

```
choco install python312
choco install git
choco install obsidian
```

Download and install positron from:  https://positron.posit.co/download.html

To be able to use the command line tools above, you will need to close the powershell window, then open a new powershell window.

## Useful software to consider installing

* drawio
* brave browser (or other favorite browser)
* slack or other 'community software' like pidgin or discord (for OS specific communities)
* vym (if available)
* umbrello
* pytest
* meld
* qtcreator
* zotero

### With Chocolatey 

```
choco install drawio
choco install brave
choco install slack
choco install umbrello
choco install meld
choco install qtcreator
choco install qt6-base-dev
choco install zotero
```

to see if a piece of software is available via chocolatey, you can do:

```
choco search softwareName
```

like searching for the brave browser:

```
choco search brave
```

To make sure the software you are searching for is the right software, run:

``` 
choco info brave
```

to find out a variety of information on the brave chocolatey package.

### Without Chocolatey

Vym - Download and install the vym exe installer from: https://sourceforge.net/projects/vym/files/


## Set up git to connect to github with ssh

## Setting up the terminal and powershell to start and your user home



```
$USERNAME = <your username here>
icacls $PROFILE /grant "$env:USERNAME":RX
icacls $PROFILE /grant "$env:USERNAME":RX
icacls $PROFILE /remove:g Guests
notepad $PROFILE
```

and put the following into that file:

```


```
