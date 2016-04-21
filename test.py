import cv2
import time
import sys
import PIL
from images2gif import writeGif
from PIL import Image
from PIL import ImageOps

# "0" is the port of your built-in webcam, probably.
camera_port = 0
# Number of frames to ramp-up the camera. 
ramp_frames = 30

# Note that you will want to keep the row/column count in line with the width
# and height values to maintain a sensible strip. i.e. One column looks good
# with strip_width = 300, but odd with a wider width.
strip_rows = 4
strip_columns = 2
strip_width = 1200
strip_height = 1800
footer = Image.open('photobooth_footer.png')

# Animated gif settings.
gif_width = 300
gif_height = 900
gif_footer = Image.open('photobooth_gif_footer.png')
gif_row_gutter = 7

# Determines the space in pixels between columns and rows.
row_gutter = 15
column_gutter = 10

# How long the script should count down before taking a picture in seconds.
wait_time = 3

# A silly list determining what columns should have a grayscale effect applied.
# Ideally this would be a map of common filters - sepiatone, soft focus, etc.
column_grayscale = (0, 1)

# Takes a single picture from the current video capture device.
def get_image(camera):
  retval, image = camera.read()
  image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
  image = Image.fromarray(image)
  return image

def photobooth_sequence(camera):
  strip = Image.new('RGB', (strip_width, strip_height), (255,255,255))
  animated_strip = []

  # Warm up the camera to make sure the lightning/focus adjusts.
  print 'Warming up...'
  for i in xrange(ramp_frames):
    temp = get_image(camera)

  # Determine a desired width/height for our frames based on common variables.
  target_height = ((strip_height - footer.height) - ((strip_rows + 1) * row_gutter)) / strip_rows
  target_width = (strip_width - ((strip_columns - 1) * column_gutter)) / strip_columns
  
  # Handle animation.
  target_gif_height = ((gif_height - gif_footer.height) - ((strip_rows + 1) * gif_row_gutter)) / strip_rows
  target_gif_width = gif_width

  for row in xrange(strip_rows):
    # Wait a bit extra to give people time to adjust.
    time.sleep(2)

    frames = []

    # Wait for our users to pose. Wait time doesn't account for execution time 
    # because I'm lazy.
    for i in xrange(wait_time):
      print '%s...' % (wait_time - i)
      # Handle animation.
      for i in xrange(4):
        frame = ImageOps.fit(get_image(camera), (target_gif_width, target_gif_height), PIL.Image.LANCZOS)
        frames.append(frame)
        time.sleep(.25)
    print 'Smile!'
    time.sleep(.25)

    # Grab an image from the webcam.
    image = get_image(camera)

    # Scale/crop the image to fit our desired width/height.
    image = ImageOps.fit(image, (target_width, target_height), PIL.Image.LANCZOS)
    
    # Handle animation.
    frame = ImageOps.fit(image, (target_gif_width, target_gif_height), PIL.Image.LANCZOS)
    frames.append(frame)

    y = (row * target_height) + ((row+1) * row_gutter)

    for column in xrange(strip_columns):
      x = (column * target_width) + (column * column_gutter)
      # Check if this column should be grayscaled.
      if column_grayscale[column]:
        strip.paste(ImageOps.grayscale(image), (x, y))
      else:
        strip.paste(image, (x, y))

    # Handle animation.
    index = 0
    y = (row * target_gif_height) + ((row+1) * (gif_row_gutter))
    for frame in frames:
      try:
        animated_strip[index]
      except IndexError:
        animated_strip.insert(index, Image.new('RGB', (gif_width, gif_height), (255,255,255)))
      animated_strip[index].paste(frame, (0, y))
      index += 1

  # Add the footer.
  strip.paste(footer, (0, (strip_height - footer.height)))
  
  # Add the footer to animated frames.
  for current_strip in animated_strip:
    current_strip.paste(gif_footer, (0, (current_strip.height - gif_footer.height)))

  # Show the strip to the user, this is where you'd put print/save code as well.
  strip.show()

  # Write the animated gif to a file.
  writeGif('test.gif', animated_strip, duration=0.1)

while True:
  text = raw_input('Press ENTER to start photobooth sequence, or type "peace" to quit: ')
  if (text == 'peace'):
    break
  camera = cv2.VideoCapture(camera_port)
  photobooth_sequence(camera)
  del(camera)
