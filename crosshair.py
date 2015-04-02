import time
import picamera
import numpy as np
import cv2
import RPi.GPIO as GPIO

# settings from config file:
width = 1024
height = 768
colors = {
        'white': (255,255,255),
        'red': (255,0,0),
        'green': (0,255,0),
        'blue': (0,0,255),
        'yellow': (255,255,0),
        }
curcol = 'white'
curpat = 1
xcenter = 512
ycenter = 384
radius = 77

# number of available patterns:
maxpat = 10

# initialize toggle for on/off button and gui state:
togsw = 1
guivisible = 1

# initialize GPIO and assign buttons:
GPIO.setmode(GPIO.BCM)
# GPIO 24, 23 & 18 set up as inputs, pulled up to avoid false detection.
# Both ports are wired to connect to GND on button press.
GPIO.setup(24, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# threaded callbacks to run in new thread when button events are detected
# function to call when top button is pressed (GPIO 24):
def toggleonoff(channel):
    global togsw,o
    if togsw == 1:
        print "Toggle Crosshair OFF"
        camera.remove_overlay(o)
        togsw = 0
    else:
        print "Toggle Crosshair ON"
        if guivisible == 0:
            o = camera.add_overlay(np.getbuffer(ovl), layer=3, alpha=160)
        else:
            o = camera.add_overlay(np.getbuffer(gui), layer=3, alpha=160)
        togsw = 1
    return

# function to call when middle button is pressed (GPIO 23):
def togglepattern(channel):
    global togsw,o,curpat,maxpat,col,ovl,gui
    # if overlay is inactive, ignore button:
    if togsw == 0:
        print "Pattern button pressed, but ignored --- Crosshair not visible."
    # if overlay is active, drop it, change pattern, then show it again
    else:
        curpat += 1
        print "Set new pattern: " + str(curpat) 
        if curpat > maxpat:     # this number must be adjusted to number of available patterns!
            curpat = 1
        if guivisible == 0:
            # reinitialize array:
            ovl = np.zeros((height, width, 3), dtype=np.uint8)
            patternswitch(ovl,0)
            if 'o' in globals():
                camera.remove_overlay(o)
            o = camera.add_overlay(np.getbuffer(ovl), layer=3, alpha=160)
        else:
            # reinitialize array
            gui = np.zeros((height, width, 3), dtype=np.uint8)
            creategui(gui)
            patternswitch(gui,1)
            if 'o' in globals():
                camera.remove_overlay(o)
            o = camera.add_overlay(np.getbuffer(gui), layer=3, alpha=160)
    return

# function to call when low button is pressed (GPIO 18):
def togglecolor(channel):
    global togsw,o,curcol,col,ovl,gui
    # step up the color to next in list
    curcol = colorcycle(colors,curcol)
    # map colorname to RGB value for new color
    col = colormap(curcol)
    # if overlay is inactive, ignore button:
    if togsw == 0:
        print "Color button pressed, but ignored --- Crosshair not visible."
    # if overlay is active, drop it, change color, then show it again
    else:
        print "Set new color: " + str(curcol) + "  RGB: " + str(col) 
        if guivisible == 0:
            # reinitialize array:
            ovl = np.zeros((height, width, 3), dtype=np.uint8)
            patternswitch(ovl,0)
            if 'o' in globals():
                camera.remove_overlay(o)
            o = camera.add_overlay(np.getbuffer(ovl), layer=3, alpha=160)
        else:
            # reinitialize array
            gui = np.zeros((height, width, 3), dtype=np.uint8)
            creategui(gui)
            patternswitch(gui,1)
            if 'o' in globals():
                camera.remove_overlay(o)
            o = camera.add_overlay(np.getbuffer(gui), layer=3, alpha=160)
    return

GPIO.add_event_detect(24, GPIO.FALLING, callback=toggleonoff, bouncetime=300)
GPIO.add_event_detect(23, GPIO.FALLING, callback=togglepattern, bouncetime=300)
GPIO.add_event_detect(18, GPIO.FALLING, callback=togglecolor, bouncetime=300)


# map text color names to RGB:
def colormap(col):
    return colors.get(col, (255,255,255))    # white is default

# cycle through color list starting from current color:
def colorcycle(self, value, default='white'):
    # create an enumerator for the entries and step it up
    for i, item in enumerate(self):
        if item == value:
            i += 1
            # if end of color list is reached, jump to first in list
            if i >= len(self):
                i = 0
            return self.keys()[i]
    # if function fails for some reason, return white
    return default

# function to construct/draw the GUI
def creategui(target):
    cv2.putText(target, gui1, (10,630), font, 2, col, 2)
    cv2.putText(target, gui2, (10,660), font, 2, col, 2)
    cv2.putText(target, gui3, (10,690), font, 2, col, 2)
    cv2.putText(target, gui4, (10,720), font, 2, col, 2)
    cv2.putText(target, gui5, (10,750), font, 2, col, 2)
    cv2.putText(target, 'GUI will vanish after 10s', (10,30), font, 2, col, 2)
    return

# function to construct and draw the overlay, options are "gui" or "ovl" and 0 or 1
def patternswitch(target,guitoggle):
    global o
    # first remove existing overlay:
    if 'o' in globals():
        camera.remove_overlay(o)
    if guitoggle == 1:
        creategui(gui)
    # cycle through possible patterns:
    if curpat == 1:
        pattern1(target, xcenter, ycenter, radius, col)
    if curpat == 2:
        pattern2(target, xcenter, ycenter, radius, col)
    if curpat == 3:
        pattern3(target, xcenter, ycenter, radius, col)
    if curpat == 4:
        pattern4(target, xcenter, ycenter, radius, col)
    if curpat == 5:
        pattern5(target, xcenter, ycenter, radius, col)
    if curpat == 6:
        pattern6(target, xcenter, ycenter, radius, col)
    if curpat == 7:
        pattern7(target, xcenter, ycenter, radius, col)
    if curpat == 8:
        pattern8(target, xcenter, ycenter, radius, col)
    if curpat == 9:
        pattern9(target, xcenter, ycenter, radius, col)
    if curpat == 10:
        pattern10(target, xcenter, ycenter, radius, col)
    # Add the overlay directly into layer 3 with transparency;
    # we can omit the size parameter of add_overlay as the
    # size is the same as the camera's resolution
    o = camera.add_overlay(np.getbuffer(target), layer=3, alpha=160)
    return

# defining functions for all possible patterns follow, 
# activated by patternswitch function

# pattern1: Bruker style crosshair with circles and ticks
def pattern1( arr, x, y, rad, col ):
    cv2.line(arr,(0,y),(width,y),col,1)
    cv2.line(arr,(x,0),(x,height),col,1)
    i = 0
    for i in range(1, 8): 
        cv2.circle(arr,(x,y),i*rad,col,1)
        i += 1
    # ticks on the horizontal axis:
    intervalh = np.arange(0,width,float(rad)/10)
    j = 0
    for i in intervalh:
        # make every 5th tick longer, omit every 10th tick:
        diff = int(round(i))
        if j%5 == 0:    
            if not j%10 == 0:
                cv2.line(arr,(x+diff,y-4),(x+diff,y+4),col,1)
                cv2.line(arr,(x-diff,y-4),(x-diff,y+4),col,1)
        else:
            cv2.line(arr,(x+diff,y-2),(x+diff,y+3),col,1)
            cv2.line(arr,(x-diff,y-2),(x-diff,y+3),col,1)
        j += 1
    # ticks on the vertical axis:
    intervalv = np.arange(0,height,float(rad)/10)
    l = 0
    for k in intervalv:
        # make every 5th and 10th tick longer:
        diff = int(round(k))
        if l%5 == 0:    
            if l%10 == 0:
                cv2.line(arr,(x-6,y+diff),(x+6,y+diff),col,1)
                cv2.line(arr,(x-6,y-diff),(x+6,y-diff),col,1)
            else:
                cv2.line(arr,(x-4,y+diff),(x+4,y+diff),col,1)
                cv2.line(arr,(x-4,y-diff),(x+4,y-diff),col,1)
        else:
            cv2.line(arr,(x-2,y+diff),(x+2,y+diff),col,1)
            cv2.line(arr,(x-2,y-diff),(x+2,y-diff),col,1)
        l += 1
    return    

# pattern2: simple crosshair with ticks
def pattern2( arr, x, y, rad, col ):
    # cv2.circle(arr,(x,y),rad,col,1)
    cv2.line(arr,(0,y),(width,y),col,1)
    cv2.line(arr,(x,0),(x,height),col,1)
    # ticks on the horizontal axis:
    intervalh = np.arange(0,width,float(rad)/10)
    j = 0
    for i in intervalh:
        # make every 5th and 10th tick longer:
        diff = int(round(i))
        if j%5 == 0:    
            if j%10 == 0:
                cv2.line(arr,(x+diff,y-6),(x+diff,y+6),col,1)
                cv2.line(arr,(x-diff,y-6),(x-diff,y+6),col,1)
            else:
                cv2.line(arr,(x+diff,y-4),(x+diff,y+4),col,1)
                cv2.line(arr,(x-diff,y-4),(x-diff,y+4),col,1)
        else:
            cv2.line(arr,(x+diff,y-2),(x+diff,y+3),col,1)
            cv2.line(arr,(x-diff,y-2),(x-diff,y+3),col,1)
        j += 1
    # ticks on the vertical axis:
    intervalv = np.arange(0,height,float(rad)/10)
    l = 0
    for k in intervalv:
        # make every 5th and 10th tick longer:
        diff = int(round(k))
        if l%5 == 0:    
            if l%10 == 0:
                cv2.line(arr,(x-6,y+diff),(x+6,y+diff),col,1)
                cv2.line(arr,(x-6,y-diff),(x+6,y-diff),col,1)
            else:
                cv2.line(arr,(x-4,y+diff),(x+4,y+diff),col,1)
                cv2.line(arr,(x-4,y-diff),(x+4,y-diff),col,1)
        else:
            cv2.line(arr,(x-2,y+diff),(x+2,y+diff),col,1)
            cv2.line(arr,(x-2,y-diff),(x+2,y-diff),col,1)
        l += 1
    return    

# pattern3: simple crosshair without ticks
def pattern3( arr, x, y, rad, col ):
    cv2.line(arr,(0,y),(width,y),col,1)
    cv2.line(arr,(x,0),(x,height),col,1)
    return    

# pattern4: simple crosshair with circles (no ticks)
def pattern4( arr, x, y, rad, col ):
    cv2.line(arr,(0,y),(width,y),col,1)
    cv2.line(arr,(x,0),(x,height),col,1)
    i = 0
    for i in range(1, 8): 
        cv2.circle(arr,(x,y),i*rad,col,1)
        i += 1
    return    

# pattern5: simple crosshair with one circle (no ticks)
def pattern5( arr, x, y, rad, col ):
    cv2.line(arr,(0,y),(width,y),col,1)
    cv2.line(arr,(x,0),(x,height),col,1)
    cv2.circle(arr,(x,y),rad,col,1)
    return    

# pattern6: simple circle
def pattern6( arr, x, y, rad, col ):
    cv2.circle(arr,(x,y),rad,col,1)
    return

# pattern7: small center crosshair
def pattern7( arr, x, y, rad, col ):
    cv2.line(arr,(x-10,y),(x+10,y),col,1)
    cv2.line(arr,(x,y-10),(x,y+10),col,1)
    return

# pattern8: small center crosshair without center
def pattern8( arr, x, y, rad, col ):
    cv2.line(arr,(x-10,y),(x-3,y),col,1)
    cv2.line(arr,(x,y-10),(x,y-3),col,1)
    cv2.line(arr,(x+3,y),(x+10,y),col,1)
    cv2.line(arr,(x,y+3),(x,y+10),col,1)
    return

# pattern9: only a dot
def pattern9( arr, x, y, rad, col ):
    cv2.circle(arr,(x,y),2,col,-1)
    return

# pattern10: grid
def pattern10( arr, x, y, rad, col ):
    global width, height
    # center lines:
    cv2.line(arr,(0,y),(width,y),col,1)
    cv2.line(arr,(x,0),(x,height),col,1)
    i = rad
    j = rad
    # horizontal lines:
    while i < height:
        cv2.line(arr,(0,y+i),(width,y+i),col,1)
        cv2.line(arr,(0,y-i),(width,y-i),col,1)
        i += rad
    # vertical lines:
    while j < width:
        cv2.line(arr,(x+j,0),(x+j,height),col,1)
        cv2.line(arr,(x-j,0),(x-j,height),col,1)
        j += rad
    return

# create array for the overlay:
ovl = np.zeros((height, width, 3), dtype=np.uint8)
font = cv2.FONT_HERSHEY_PLAIN
col = colormap(curcol)
# create array for a bare metal gui and text:
gui = np.zeros((height, width, 3), dtype=np.uint8)
gui1 = 'arrows = move center'
gui2 = 'c       = cycle color'
gui3 = 'p       = cycle pattern'
gui4 = '+/-    = scale'
gui5 = 's       = save settings'

with picamera.PiCamera() as camera:
    camera.resolution = (width, height)
    camera.framerate = 24
    # set this to 1 when switching to fullscreen output
    camera.preview_fullscreen = 1
    camera.preview_window = (0,0,width,height)
    camera.start_preview()
    camera.annotate_background = 'black'
    try:
        # show gui fot 10 seconds:
        patternswitch(gui,1)
        time.sleep(10)
        guivisible = 0
        # cycle through possible patterns:
        patternswitch(ovl,0)
        while True:
            time.sleep(1)
    finally:
        camera.close()               # clean up camera
        GPIO.cleanup()               # clean up GPIO
