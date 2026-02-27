# Cerbo and Ruuvi Setup

For these instructions, it's best to work from a computer browser to access the Cerbo interface and subsequently the Signal K and Node-Red stuff. None of this is hard or scary so don't be put off with new terms.

## Ruuvi

The RuuviTag 4 in 1 sensors, or the pro variant of them offer temperature, Barometer, Humidity and movement (3 axis accelerometer). They're around £30-£40 at the moment from Amazon (https://www.amazon.co.uk/INNOVATIONS-2024-RUUVITAG-Sensor-DRU-001-Multicolor/dp/B09FMYRYBR) and connect via Bluetooth Low Energy, giving a battery life of up to two years. They have a great app to use standalone, but can also integrate with boat systems nicely. This will enable barometer, humidity and temperature data via NMEA 2000 to the plotter as well in the Cerbo display.

They are directly compatible with Victron VenusOS devices including Cerbo and any Raspberry Pi running the OS. They do need Bluetooth, and for this I bought a TP-Link UB4A from Amazon for £4 (https://www.amazon.co.uk/dp/B07YLDVM6B). I also added a cheap unpowered USB hub as I was already using the USB ports - unpowered is working fine for my use with VE-Direct and BTLE adapter but your system may need a powered hub if you do anything fancy like a USB GPS dongle.
The Cerbo GX does have Bluetooth, but mine is one of the versions where the processor overheats and disables Bluetooth. The manual has this to say:

> "For Cerbo GX units with serial numbers up to and including HQ2207, internal Bluetooth is disabled when CPU
temperature exceeds 53 °C. In such cases, a USB Bluetooth adapter is required for reliable operation. Units
with serial numbers HQ2208 and later, as well as Cerbo-S GX, are not affected."

To pair the sensors, open the Victron interface and go to Settings, Integrations, Bluetooth Sensors. Here you should see your Ruuvi sensor(s), just toggle them on to pair and your Victron system will start getting temperature, Barometer, etc. immediately. At this stage, your Cerbo will display the sensor under the environment tab of the Levels page (using interface v2 here!). Your Device will also begin uploading this data to VRM for long term collection and viewing.

![Bluetooth pairing of the sensor](images/1.%20Bluetooth%20Pairing.png)

![Environment page on the Cerbo showing sensor data](images/2.%20Environment.png)

![Sensor data in VRM online with a historical graph](images/3.%20VRM.png)

## NMEA2000 Wiring

To set up NMEA2000, firstly, you'll need your device to be connected via NMEA2K cable to VE Can. These cables can be made using an Ethernet cable with a NMEA field connector on one end for around £15 and you can find instructions online. The official Victron cable is more expensive, but simpler and potentially more reliable for those unused to making cables.

## Cerbo Additional Software

Next, you need to go to Settings, General, Firmware, Online Updates and select the "Large" image for Cerbo which includes Node-Red and SignalK. Once selected, check for updates and install. This does not remove your settings and is seemingly quite safe to do, but maybe take a backup of your settings to be sure. The device will reboot after a few minutes and has a couple of new menu options.

## Signal K and Node-Red

### Setup Signal K

Go to Settings, Integrations and enable Signal K. DO NOT enable Node-Red, we won't be using that from here and neither do we want two copies running. It's not an issue to have both versions, but it will take resources so unless you actually know what you're doing don't turn it on.

Click Open Link to access Signal K and you'll find yourself in a new portal with some fairly powerful capabilities. Click on the App Store link (don't worry, no charge for the apps).

We're going to use two plugins for this integration, signalk-to-nmea2000 which is preinstalled and @signalk/signalk-node-red which you need to search for and install. We're going to use the Node-Red app to convert some data and remap it for the NMEA plugin to use, and the NMEA plugin will push that data out to the NMEA network.

### Find your sensor data

Now click on Data Browser in the left hand menu. We need to find the paths to our Ruuvi Data. In the search box type "humidity" and you'll see several values, you're looking for ones that look like "environment.venus.20.humidity".
Because I have two sensors I have two of these, each showing the ruuvi source on the right hand side. Copy the paths you need, mine are:

environment.venus.20.humidity
environment.venus.20.temperature
environment.venus.20.pressure

environment.venus.21.humidity
environment.venus.21.temperature
environment.venus.21.pressure

Yours may be different as they are assigned by the system, but they will be similar and you'll have three per sensor.

![Data browser showing sensor data](images/4.%20Data%20Browser.png)

### Signal K to NMEA2000

Next, click Server, Plugin Config on the left side menu. You'll see various plugins here, scroll and enable "Signal K to NMEA 2000". Don't enable any logging as it just uses space on the disk and will eventually fill it up.

Scroll down slowly. We need to enable multiple PGNs for the NMEA2000 to ensure broad plotter support since there are many versions of these and not all plotters/instruments support all of them. The list I enabled for one internal and one external sensor is:

Atmospheric Pressure (130311)
Outside Humidity (PGN130313)
Inside Humidity (PGN130313)
Atmospheric Pressure (130314)
Outside Temperature (130312)
Outside Temperature (130316)
Inside Temperature (130312)
Inside Temperature (130316)

For each one, tick Enabled.
Each will have a box at the top for Resend - set this to 1 second for all.
Each will have a box at the bottom for Source such as "Source for environment.outside.pressure". It's the "environment.outside.pressure" part we need to fill with data later, so make a note of these as they are different for inside and outside and you may use different ones than I did.

![](images/9.%20PGN.png)

When you reach the bottom, click Submit to save your changes. We now have the NMEA plugin configured but need to connect data to it.

### Node-Red Plugin

Scroll up and ensure that the Node-Red plugin is enabled. If not, enable it and hit Submit.
Click on WebApps in the left hand menu then Node-Red. Note that this Node-Red is SignalK enabled while the stock Victron one is not, that's why we didn't use the one in Victron.

You'll now be in the Node-Red interface. Think of this like wiring things together. On the left you have functions and other stuff. For this guide we're only interested in three things.

Signal K Subscribe - this will connect to our data source i.e. our Ruuvi sensor data.
Signal K Send Pathvalue - this will connect to our data out i.e. the NMEA2K paths we found earlier like "environment.outside.pressure"
Function function - this will transform data where needed. My B&G doesn't properly format Relative Humidity so I had to multiply it by 100 and limit to 2 decimal places for it to show as a percentage (53.2%) rather than as a number (0.532). It's a small thing, but important to me. This may be a Navico plotter bug as I have B&G, I would not expect to have to do this.

![](images/5.%20Node%20Flows.png)

We will need one line per data point, so three per sensor (temp, humidity, baro pressure). For each, drag a subscribe and send pathvalue onto your flow workspace. Drag the grey square on the right of the subscribe box to the one on the left of the send pathvalue box (just like wiring!).

Double Click the subscribe node and fill in a name such as "outside barometer sensor". Fill in the path with your ruuvi data path from above, such as "environment.venus.20.pressure". 

![Subscribe Node](images/6.%20subscribe%20node.png)

On the corresponding send pathvalue node double click and again fill in a name such as "outside barometer N2K" and set the path to the matching one from the NMEA2000 plugin from above such as "environment.outside.pressure". 

![Send Pathvalue](images/7.%20Send%20Pathvalue.png)

For the Humidity line, I added a function between the subscribe and send pathvalue nodes. In the OnMessage tab of this, I added the following code. There are neater ways to do this (but they aren't more efficient) but I wanted it easy to understand to share here. Line 1 multiplies the incoming value by 100. Line two takes that value and rounds it to two decimal places. Line two also tells the system to return the value as a number rather than text. Line three sends the result to the next node (send pathvalue).

```
msg.payload = msg.payload * 100;
msg.payload = Number(msg.payload.toFixed(2));
return msg;
```

![Node-Red function code](images/8.%20Function.png)

Click Deploy at the top right of the screen. You may need to restart the Cerbo but it should now be sending temperature, barometer, and relative humidity to your NMEA network.

## Plotter

You will now need to follow your instruction manual for the plotter to show these data on your screen.