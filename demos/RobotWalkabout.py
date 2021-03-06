#!/usr/bin/python
from __future__ import absolute_import, division, print_function, unicode_literals

""" Uses a Tkinter window with elevation map, and a robot character in the
foreground that swaps to a more objective view as the mouse moves back and forth
The landscape can be navigated with the w and s keys to move forward and back.
The robot demostrates the same texture as the buildings but with higher shiny
value
"""
import math

import demo

from pi3d import Display
from pi3d.Keyboard import Keyboard
from pi3d.Mouse import Mouse
from pi3d.Texture import Texture

from pi3d.Camera import Camera
from pi3d.Shader import Shader

from pi3d.shape.Cuboid import Cuboid
from pi3d.shape.Cylinder import Cylinder
from pi3d.shape.ElevationMap import ElevationMap
from pi3d.shape.EnvironmentCube import EnvironmentCube
from pi3d.shape.EnvironmentCube import loadECfiles
from pi3d.shape.MergeShape import MergeShape
from pi3d.shape.Sphere import Sphere

from pi3d.util.Screenshot import screenshot

# Setup display and initialise pi3d
DISPLAY = Display.create(x=50, y=50, w=-100, h=-100,
                         background=(0.4, 0.8, 0.8, 1))
shader = Shader("shaders/uv_reflect")
flatsh = Shader("shaders/uv_flat")
#############################

# Load textures
reflcn = Texture("textures/stars.jpg")

#load environment cube
ectex = loadECfiles("textures/ecubes","sbox_interstellar")
myecube = EnvironmentCube(size=900.0, maptype="FACES")
myecube.set_draw_details(flatsh, ectex)

# Create elevation map
mapwidth=1000.0
mapdepth=1000.0
mapheight=60.0
mountimg1 = Texture("textures/mars_colour.png")
bumpimg = Texture("textures/mudnormal.jpg")
mymap = ElevationMap(mapfile="textures/mars_height.png",
                     width=mapwidth, depth=mapdepth, height=mapheight,
                     divx=128, divy=128)
mymap.set_draw_details(shader,[mountimg1, bumpimg],128.0, 0.0)
mymap.set_fog((0.3,0.15,0.1,0.1), 300.0)


#create robot
metalimg = Texture("textures/metalhull.jpg")
robot_head= Sphere(radius=1.0)
robot_body = Cylinder(radius=1.0, height=2.0, sides=12)
robot_leg = Cuboid(w=0.35, h=2.0)

robot = MergeShape()
robot.add(robot_head.buf[0], 0.0, 1.6)
robot.add(robot_body.buf[0], 0.0, 0.5)
robot.add(robot_leg.buf[0], -1.04, 0, 0)
robot.add(robot_leg.buf[0], 1.05, 0, 0)
robot.set_draw_details(shader, [metalimg, metalimg, reflcn], 0.0, 0.5)

#create space station
ssphere = Sphere(radius=10, slices=16, sides=16)
scorrid = Cylinder(radius=4, height=22)

station = MergeShape(y=mymap.calcHeight(0, 0), rx=4, ry=4, rz=4)
station.add(ssphere.buf[0], -20, 0, 20)
station.add(ssphere.buf[0], 20, 0, 20)
station.add(ssphere.buf[0], 20, 0, -20)
station.add(ssphere.buf[0], -20, 0, -20)
station.add(scorrid.buf[0], -20, 0, 0, 90, 0, 0)
station.add(scorrid.buf[0], 0, 0, -20, 90, 90, 0)
station.add(scorrid.buf[0], 0, 0, 20, 90, 90, 0)
station.set_draw_details(shader, [metalimg, metalimg], 0.0)
station.set_fog((0.3,0.15,0.1,0.1), 300.0)

#avatar camera
rot = 0.0
tilt = -10.0
avhgt = 2.0
xm = 0.0
zm = 0.0
ym = (mymap.calcHeight(xm,zm)+avhgt)

# Fetch key presses
mykeys = Keyboard()
mymouse = Mouse(restrict=False)
mymouse.start()

omx, omy = mymouse.position()

# Display scene and rotate cuboid
CAMERA = Camera.instance()
while DISPLAY.loop_running():

  CAMERA.reset()
  #tilt can be used as a means to prevent the view from going under the landscape!
  if tilt < -1: sf = 15 - 12.5/abs(tilt)
  else: sf = 2.5
  xoff = sf*math.sin(math.radians(rot))
  yoff = abs(1.25*sf*math.sin(math.radians(tilt))) + 3.25
  zoff = -sf*math.cos(math.radians(rot))
  CAMERA.rotate(tilt, rot, 0)
  CAMERA.position((xm + xoff, ym + yoff, zm + zoff))   #zoom CAMERA out so we can see our robot

  #draw robot
  robot.position(xm, ym, zm)
  robot.rotateToY(-rot)
  robot.draw()

  station.draw()
  mymap.draw() #Draw the landscape
  myecube.draw() #Draw environment cube
  myecube.position(xm, ym, zm)

  mx, my = mymouse.position()

  #if mx>DISPLAY.left and mx<DISPLAY.right and my>DISPLAY.top and my<DISPLAY.bottom:
  rot -= (mx-omx) * 0.2
  tilt += (my-omy) * 0.1
  omx = mx
  omy = my

  #Press ESCAPE to terminate
  k = mykeys.read()
  if k >-1:
    if k==119:    #key W
      xm-=math.sin(math.radians(rot))
      zm+=math.cos(math.radians(rot))
      ym = (mymap.calcHeight(xm,zm)+avhgt)
    elif k==115:  #kry S
      xm+=math.sin(math.radians(rot))
      zm-=math.cos(math.radians(rot))
      ym = (mymap.calcHeight(xm,zm)+avhgt)
    elif k==39:   #key '
      tilt -= 2.0
      print(tilt)
    elif k==47:   #key /
      tilt += 2.0
    elif k==97:   #key A
        rot -= 2
    elif k==100:  #key D
        rot += 2
    elif k==112:  #key P
        screenshot("walkaboutRobot.jpg")
    elif k==27:    #Escape key
      mykeys.close()
      mymouse.stop()
      DISPLAY.destroy()
      break
    else:
        print(k)
