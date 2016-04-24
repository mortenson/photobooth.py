import cv2
import sys
import time
import PIL
from photobooth_config import *
from images2gif import writeGif
from imgurpython import ImgurClient
from imgurpython.helpers.error import ImgurClientError
from PIL import Image
from PIL import ImageOps

# Attempt to load the footer images, which may not exist.
try:
  footer = Image.open(footer)
except IOError:
  footer = Image.new('RGB', (1, 1), (255,255,255))

try:
  gif_footer = Image.open(gif_footer)
except IOError:
  gif_footer = Image.new('RGB', (1, 1), (255,255,255))

def get_imgur_client(client_id, client_secret):
  try:
    client = ImgurClient(client_id, client_secret)
    authorization_url = client.get_auth_url('pin')
    imgur_pin = raw_input('Please visit %s and enter the pin given to you there: ' % authorization_url)
    credentials = client.authorize(imgur_pin, 'pin')
    client.set_user_auth(credentials['access_token'], credentials['refresh_token'])
  except ImgurClientError as e:
    print('Imgur error #%d: "%s"' % (e.status_code, e.error_message))
    print('Proceeding without enabling Imgur integration.')
    client = False

  return client

# Takes a single picture from the current video capture device.
def get_image(camera):
  retval, image = camera.read()
  image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
  image = Image.fromarray(image)
  return image

def photobooth_sequence(camera):
  # Unique key to append to filenames.
  timestamp = time.strftime('%Y%m%d-%H%M%S')

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
  strip.save('photobooth_' + timestamp + '.png')

  # Write the animated gif to a file.
  writeGif('photobooth_gif_' + timestamp + '.gif', animated_strip, duration=0.1)

  # Upload both files to Imgur.
  if use_imgur and imgur_client:
    try:
      imgur_client.upload_from_path('photobooth_' + timestamp + '.png', imgur_config, False);
      imgur_client.upload_from_path('photobooth_gif_' + timestamp + '.gif', imgur_config, False);
    except ImgurClientError as e:
      print('Imgur error #%d: "%s"' % (e.status_code, e.error_message))

if use_imgur:
  imgur_client = get_imgur_client(imgur_client_id, imgur_client_secret)

while True:
  text = raw_input('Press ENTER to start photobooth sequence, or type "peace" to quit: ')
  if (text == 'peace'):
    break
  camera = cv2.VideoCapture(camera_port)
  photobooth_sequence(camera)
  del(camera)
