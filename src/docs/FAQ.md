# Frequently Asked Questions (FAQ)

**Q. Is this app meant for real people with real pain and health problems?**

**A.** NO.  This is a personal project for the author and contributors to study issues relating to an app like that.

**Q. Where does the weather data come from?**

**A.** the National Oceanic and Atomospheric Administration - noaa.gov

**Q. What python library are you using to acquire observation data?**

**A.** For observation data, we are using the [https://pypi.org/project/noaa-sdk/](https://pypi.org/project/noaa-sdk/) library.  We plan on using the same library for forecast data.  The 'proto' directory may have a few to several different simple examples of how to use the library.  Not all may work.

**Q. Are you useing some kind of caching in order to not hit the servers too often?**

**A.** Yes,  we're using the [https://pypi.org/project/cachetools/](https://pypi.org/project/cachetools/) library.  Check the source code for the actual usage.  The 'proto' directory may have a few different simple examples of how to use the library.

**Q. There are a bunch of filies in the proto directory that don't work.  Why not?**

**A.** The proto directory is like the wild west of code examples.  Some may work, and some may not.  Some may just not work as expected.  Once useage of internal libraries are stable, the stable proto files will be copied/moved to the examples directory. 

**Q. Are there OS spec issues programming this project?**

**A.** Very little if any.  

**Q. What are the differences in the setup of the build and run environments for each OS?**

**A.** Each OS has different requirements with installing the build environment for the project.  The project uses software package managers as much as possible to handle installation and configuration of the build and run environments.

Please look in the [[src/docs/osNotes/README.md]] and child directories for OS specific information.

**Q. What python packages are being used by this project?**

**A.** Python packages being used can be found in the build scripts:

* pyside6
* noaa_sdk
* cachetools
* pyqtgraph
* pywin32 (on Windows)

Looking to include (as project grows and as needed):
* pyinstaller  (create an "app" or "onefile app")
* pyinstaller-hooks-contrib (if needed - with pyinstaller)
* packaging

Eventually may switch from pyside6 to kivy, maybe beeware(toga) as the graphical interface to make it easier to have graphics interfaces on mobile devices as well as desktop.  There is no official support for pyside6 on mobile devices, and it can be used on Android with difficulty and is experimental on iOS.

Alternatives for Mobile Python GUIs:

|Framework|Android|iOS|Notes|
|---|---|---|---|
|**PySide6**|Strong|Emerging|Qt-based, best for desktop-to-mobile ports.|
|**Kivy**|Excellent|Excellent|Touch-focused, easier deployment via Buildozer.|
|**BeeWare (Toga)**|Good|Good|Native look-and-feel, but steeper learning curve.|
|**PyQt6**|Similar to PySide6|Similar to PySide6|Near-identical to PySide6 (LGPL vs. GPL licensing).|

Kivy is also used for cross platform desktop systems as well.

# References

* Information for the question "What python packages are being used by this project?" was collected from chatGPT.com and grok.com, based on the question - "can pyside6 work on mobile devices?".

