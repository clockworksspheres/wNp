# Set Up For Building

Installing tools to set up for building the project.

## Install Chocolatey

Chocolatey is a package manager for Windows, similar to homebrew for macos, apt for debian linux based systems and yum/dnf for redhat based systems.

To install chocolatey, open an admin powershell, and run the following:

```
Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
```

To use chocolatey, close the powershell window, and open a new admin powershell window.

## Set up Chocolatey to run as a User

AI generated instructions for setting Chocolatey up - - [[chocolateyAsUser]]

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
choco install positron
```

To be able to use the command line tools above, you will need to close the powershell window, then open a new powershell window.

### Python libraries the project depends on

### By way of build scripts

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



### Without Chocolatey

## Set up git to connect to github with ssh

