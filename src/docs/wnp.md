# wnp

# Design Thoughts

* Chart Temp, Relative Humidity, Barometric Pressure, Dewpoint.  Initially individually eventually all in one chart.

* Print all in one chart 

* figure out y axis labeling for multiple on one chart

* Observations as well as forecasts

* Caching - to prevent over access of servers which leads to tracebacks due to denial of service from too frequent of access of the NOAA servers

* Make a phone app

* make ranged submitions for pain/health - track like weather, not sure, probably points rather than lines.

# Challenges

* y labeling on charts with multiple lines

* Normalizing lines on chart to overlay ranges

# Command Line options

To get the latest command line options, run the command:

```
wnp -h
```

# References

* National Oceaning and Atmospheric Administration, [NOAA](https://www.noaa.gov/)

* NOAA [sdk](https://pypi.org/project/noaa-sdk/)

* Python [Caching](https://pypi.org/project/cachetools/)

* [PyInstaller](https://pypi.org/project/pyinstaller/)

* [PySide6](https://pypi.org/project/PySide6/)

