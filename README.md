# crosshair
A customizable crosshair overlay generator for Raspberry Pi with Picamera, written in Python

Uses Python 2.7 & the following:
- pillow
- numpy
- OpenCV
- RPi.GPIO
- picamera
- configparser
- some stuff from BaseHTTPServer & CGIHTTPServer
- paramiko (for SSH2 protocol)

Installation instructions for OpenCV: http://www.pyimagesearch.com/2015/02/23/install-opencv-and-python-on-your-raspberry-pi-2-and-b/

Installation instructions for picamera:
http://www.raspberrypi.org/documentation/usage/camera/python/README.md

Installation instructions for RPi.GPIO:
http://sourceforge.net/p/raspberry-gpio-python/wiki/install/

I also use a solution for adding comments using Python's configparser suggested by user jcollado:
http://stackoverflow.com/questions/8533797/adding-comment-with-configparser

The script needs superuser privileges. This is handled by the "run_crosshair" scriptlet.
If the camera is hooked to microscope optics, the LED should be switched off. The script doesn't do it, but you can just add `disable_camera_led=1` to /boot/config.txt. 

Done features:
- You can connect three pushbuttons to the Pi's GPIOs 24,23,18 (and each to GND). These will then toggle the overlay on/off (24) or cycle through crosshair patterns (23) and colors (18).
- /boot/crosshair.cfg stores the settings (so it can be adjusted on the SD card from a Windows machine).
The file will be created on first start of the program using sensible defaults if it cannot be found.
- several colors (white, red, green, blue, yellow)
- several crosshair patterns (10 total)
- keyboard interface:
      arrow keys move center around
      +/- increase/decrease scale
      p/c change pattern/color
      space toggles overlay on/off
      ESC reverts to original settings
      s saves current settings to config file
      q quits program
- program can log to a file (off by default to increase SD card lifetime)
- web server (minimal http server provides png screenshot and metadata, port and interval can be configured)
- provided default index.html uses a CGI to embed metadata, zoom and crosshair overlay on client can be toggled. Needs javascript on client.
- sftp file upload (configurable host, username, password, target directory and filenames, metadata text file can be included). Stable vs. network outage: if the server is not reachable within a timeout, the program will just skip&retry during the next cycle.

Planned features:
- live video stream (currently not possible due to limitations in picamera)
