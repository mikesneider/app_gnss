import random
import numpy as np
import math
from PIL import Image, ImageDraw, ImageFont


def transform_polar_to_input(r, theta, w, h, theta_offset):
  # Set X from 0 to 500
  r = 90 - r
  theta = (-1.0*theta) -180 -theta_offset

  x = r*math.cos(math.radians(theta))
  y = r*math.sin(math.radians(theta))

  xs = ((x/90.0)*500)
  ys = ((y/90.0)*500)
  xs = 540 + xs
  ys = abs(ys - 540)

  return xs, ys


def generate_random_data(img_path, north_w_point=0):
  """
  Gets an image path, and randomly generate coordinate points
  for the satellites.
  """
  img = Image.open(img_path)
  w,h = img.size

  # Azimuth
  az = range(0,360)
  # Elevation
  el = range(0,90)
  theta_offset = (north_w_point/(w*1.0))*360

  # Return 5 pairs of el,az
  az_el_pairs = [ (random.choice(az), random.choice(el)) for i in range(5) ]

  print az_el_pairs

  data = []

  for (az, el) in az_el_pairs:
    x,y = transform_polar_to_input(el, az, w ,h, theta_offset)
    data.append((x,y))
  return data


def set_points(img_path, data):
  """
  Gets an image path and sets data points

    Attributes:
      img_path: String
      data: list of pairs x,y
  """
  img = Image.open(img_path)
  draw = ImageDraw.Draw(img)
  for (x,y) in data:
    draw.ellipse((x-5, y-5, x+5, y+5), fill=(0,255,0))

  img.save(img_path)


def get_north_w_point_from_heading(img_path, north_heading):
  """
  Gets a heading pointing north,
  and returns a horizontal pixel where it should be

    Attributes:
      img_path: String
      north_heading: double
  """
  img = Image.open(img_path)
  w,h = img.size

  return ((((360-north_heading/360.0) * w) + w/2) % w)





def set_elevation_lines(img_path, north_w_point=0):
  """
  Gets an image path and sets elevation lines in it.
  Assuming the horizon is 2/3 down the image.

    Attributes:
      img_path: String
  """
  img = Image.open(img_path)
  w,h = img.size

  bot = 2*h/3

  # Draw horizontal lines
  step = 0
  for i in range(10):
    draw = ImageDraw.Draw(img)
    draw.line((0, step, w, step), fill=128)
    step += bot/9

  # Draw vertical lines for NWSE
  w0 = north_w_point
  for i in range(4):
    draw.line(( w0, 0, w0, h ), fill=128)
    w0 = (w0 + w/4)%w

  img.save(img_path)


def rotate_and_set_directions(img_path, north_w_point=0):
  """
  Gets an image path, and sets directions NWSE,
  using arbitrary positions assuming north is always in the center.

  Attributes:
    img_path: String

  """
  img = Image.open(img_path)
  w, h = (960,360)

  theta_offset = (north_w_point/(w*1.0))*360

  img2 = img.rotate(theta_offset - 90)

  draw = ImageDraw.Draw(img2)
  font = ImageFont.truetype("utils/font.ttf", 30)
  w,h = img2.size

  # north (el: 0, az:0)
  x,y = w/2, 0
  draw.text((x+5,y+5), "N", (0,255,0), font=font)
  # east (el:0, az:90)
  x,y = w, h/2
  draw.text((x-25,y+5), "E", (0,255,0), font=font)
  # south (el:0, az: 180)
  x,y = w/2, h
  draw.text((x+5,y-30), "S", (0,255,0), font=font)
  # west (el:0, az: 270)
  x,y = 0, h/2
  draw.text((x+5,y+5), "W", (0,255,0), font=font)


  img2.save(img_path)

