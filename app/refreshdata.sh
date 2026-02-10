#!/bin/bash
#set root directory for script
basedir="/home/lustyd/repos/BoatDisplay/app"

# Run boatData refresh
python3 "${basedir}/python/renderBaroGraph.py"
python3 "${basedir}/python/renderBoatData.py" > "${basedir}/html/boatData.html"
chromium-headless-shell "${basedir}/html/boatData.html" --headless --screenshot="${basedir}/renders/boatData.png" --window-size="800,480" --disable-gpu --no-sandbox

# Run weather refresh
python3 "${basedir}/python/renderWeather.py" > "${basedir}/html/weather.html"
chromium-headless-shell "${basedir}/html/weather.html" --headless --screenshot="${basedir}/renders/weather.png" --window-size="800,480" --disable-gpu --no-sandbox

# Run Fortune refresh
/usr/games/fortune > "${basedir}/html/fortune.txt"
python3 "${basedir}/python/renderFortune.py" > "${basedir}/html/fortune.html"
chromium-headless-shell "${basedir}/html/fortune.html" --headless --screenshot="${basedir}/renders/fortune.png" --window-size="800,480" --disable-gpu --no-sandbox

# Run Youtube refresh
python3 "${basedir}/python/renderYoutube.py" > "${basedir}/html/youtube.html"
chromium-headless-shell "${basedir}/html/youtube.html" --headless --screenshot="${basedir}/renders/youtube.png" --window-size="800,480" --disable-gpu --no-sandbox

cp -r "${basedir}/html/" "/var/www/"
#test display
#python3 "${basedir}/python/displayFortune.py"
#python3 "${basedir}/python/displayYoutube.py"
#python3 "${basedir}/python/displayBoatData.py"

