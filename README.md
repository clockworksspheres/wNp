# wNp

# What it is:

Starting as a weather tracking app, being used to track weather against pain/health issues manually.  Eventually will have features added to track and analyze pain/health conditions against weather patterns.

Initially developed and tested on macOS, although should also work on other operating systems, should someone create a build script for it.  Build scripts available for rhel based systems and ubuntu based systems.

# Who it is targeted for:

Applicable to people with health issues that are affected by the weather.


# Why write something like this:

Adding weather forecasts may help people with weather related health issues better plan activities around bad pain related weather.

Why write something with this intention when there are other apps out there that do the job better?  Also intended as a project for the developer(s) to learn the tech to build such an app.

# When is it useful?:

* Planning activities to avoid bad health consequences due to weather
* Learning and understanding the personal connection with weather and pain
* and more...

## When it started

Project started in 2010 origionally as a C++ & Qt project on my own time, dropped for a decade and restarted as a new pyside6 project in 2025.

# Where is this software useful?:

This app is designed for anywhere that the US NOAA collects data from, locally and collaboratively.  The app is zip code driven at this time.

# How:

## How to build & package

Still in the process of building the build pipeline.  BuildScripts borrowed from another project.  Only the build.macos.sh functions to build the dev environment, using python venv to create a python environment for development of the project.

Will be using PyInstaller to create an app or integrated binary, depending on the operating system.

macOS, Linux and Windows build scripts to set up the build environment are tested.

Pyinstaller spec files and builds to create either 'onefile' or apps for each OS has not been flushed out yet - they are borrowed from another clockworksspheres project.

## How to release

No release process yet, project to new.


## How CI/CD works

No CI/CD at this time.


