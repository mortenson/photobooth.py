
# "0" is the port of your built-in webcam, probably.
camera_port = 0
# The amount of frames to "warm up" (calibrate/focus) the camera.
ramp_frames = 30
wait_time = 3

# Number of rows in the strip.
strip_rows = 4
# Number of columns in the strip.
strip_columns = 2
# The width of the photostrip in pixels.
strip_width = 1200
# The height of the photostrip in pixels.
strip_height = 1800
row_gutter = 15
column_gutter = 10

column_grayscale = (0, 1)

# The optional image files to use in the footer.
footer = 'photobooth_footer.png'
gif_footer = 'photobooth_gif_footer.png'

# The width/height of the animated gif, in pixels.
# Should be relative to the size of one column to maintain aspect ratio.
gif_width = 300
gif_height = 900
# The gutter between rows of images in the animated gif strip, in pixels.
gif_row_gutter = 7

# Optional Imgur integration settings. See https://api.imgur.com/ for details.
use_imgur = False
imgur_client_id = ''
imgur_client_secret = ''
# This configuration gets passed to the ImgurClient.upload.
# A common use case is uploading to a specific album, i.e. {'album': 'a1buM1D'}
imgur_config = {}
