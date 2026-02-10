#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
import os
from PIL import Image

basedir = "/home/lustyd/repos/BoatDisplay/app"

picdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'pic')
libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')
libdir = "/home/lustyd/repos/e-Paper/RaspberryPi_JetsonNano/python/lib/"
if os.path.exists(libdir):
    sys.path.append(libdir)

import logging
from waveshare_epd import epd7in3e
import time
from PIL import Image,ImageDraw,ImageFont
import traceback

try:

    epd = epd7in3e.EPD()
    epd.init()
    # read bmp file
    logging.info("load weather.png")
    Himage = Image.open(f'{basedir}/renders/weather.png')
    epd.display(epd.getbuffer(Himage))
    epd.sleep()

except IOError as e:
    logging.info(e)

except KeyboardInterrupt:
    logging.info("ctrl + c:")
    epd7in3e.epdconfig.module_exit(cleanup=True)
    exit()
