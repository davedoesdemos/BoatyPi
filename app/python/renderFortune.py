#!/usr/bin/python

import requests
from jinja2 import Template

basedir = "/home/lustyd/repos/BoatDisplay/app"

with open(f"{basedir}/jinjaTemplates/fortune.html.jinja") as f:
    tmpl = Template(f.read())
    try:
        fortuneText1 = open(f"{basedir}/html/fortune.txt").read().replace('\n', '<br />')
        print(tmpl.render(
            fortuneText = fortuneText1
        ))
    except Exception as e:
        print(f"Error: {e}")

