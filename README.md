# BoatDisplay
ePaper/RPi display

This project uses a Raspberry Pi (3, 4, 5 or Zero 2W) alongside an eInk/ePaper screen from WaveShare to create a screen which takes data from the Internet, a Victron Cerbo/VenusOS using Signal K, and Ruuvi sensors to make a dashboard.

Please check out InkyPi, which inspired the project and from where I took many hints. I considered making plugins for that project, but I wanted this to work differently. BoatyPi publishes the html pages as both png (for the epaper) and html for a locally hosted webpage on board the boat. I also use crontab for the scheduling - time will tell whether that's better or worse.
https://github.com/fatihak/InkyPi

Currently showing:
- Fuel level (% and capacity) (Cerbo connected to fuel sender and calibrated)
- Battery SOC (Cerbo)
- Inside and outside temperature and humidity (Ruuvi, Bluetooth to Cerbo)
- Barometer graph for past X hours from vrm API (Ruuvi to Cerbo then to VRM)

- Weather (Openweathermap.org)

- YouTube Stats (Google API)

- Fortune (Linux command line)

Install
Download the Waveshare drivers from their git repo
Install Apache2 for hosting the web pages
Install the various Python packages.

Clone the repo to your Pi
Edit the python files to set your own paths etc.

Create a .env file with your keys in containing:

VICTRON_KEY=Token xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
VICTRON_SITE=xxxxxx
WEATHER_KEY=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
GOOGLE_KEY=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

Add lines to /etc/crontab:
-Refresh the data and render png files every five minutes between 7am and 9pm

*/5 7-21 * * * lustyd    sh /path/to/repo/BoatyPi/app/refreshdata.sh

-display the various pages at different times

8,38 7-21 * * * lustyd    /usr/bin/python /path/to/repo/BoatyPi/app/python/displayYoutube.py
18,48 7-21 * * * lustyd    /usr/bin/python /path/to/repo/BoatyPi/app/python/displayFortune.py
28,58 7-21 * * * lustyd    /usr/bin/python /path/to/repo/BoatyPi/app/python/displayWeather.py

-display the main dashboard more often

3,13,23,33,43,53 7-21 * * * lustyd    /path/to/repo/BoatyPi/app/python/displayBoatData.py

-clear the display at 10pm

0 22 * * * lustyd    /usr/bin/python /path/to/repo/BoatyPi/app/python/displayShutdown.py
