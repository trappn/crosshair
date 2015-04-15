# crosshair
A customizable crosshair overlay generator for Raspberry Pi with Picamera, written in Python

Uses Python 2.7 & the following:
- pillow
- numpy
- OpenCV
- RPi.GPIO
- picamera

Installation instructions for OpenCV: http://www.pyimagesearch.com/2015/02/23/install-opencv-and-python-on-your-raspberry-pi-2-and-b/

Installation instructions for picamera:
http://www.raspberrypi.org/documentation/usage/camera/python/README.md

Installation instructions for RPi.GPIO:
http://sourceforge.net/p/raspberry-gpio-python/wiki/install/

You can connect three pushbuttons to the Pi's GPIOs 24,23,18 (and each to GND). These will then toggle the overlay on/off (24) or cycle through crosshair patterns (23) and colors (18).

/boot/crosshair.cfg stores the settings (so it can be adjusted on the SD card from a Windows machine).
The file will be created on first start of the program using sensible defaults if it cannot be found.
The script needs superuser privileges. This is handled by the "run_crosshair" scriptlet.

Planned features:
- connect a keyboard to change the default settings (and also the crosshair's center and radius)
- stream to a web server
