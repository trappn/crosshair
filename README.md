# crosshair
A customizable crosshair overlay generator for Raspberry Pi with Picamera, written in Python

Uses Python 2.7 & the following:
- pillow
- numpy
- OpenCV
- RPi.GPIO
- picamera
- configparser
- pyscreenshot
- scrot (backend for pyscreenshot)

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
- web server (minimal http server provides png screenshot with or without overlay, port and interval can be configured)

Planned features:
- live video stream
- sftp file upload
