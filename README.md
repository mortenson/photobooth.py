# photobooth.py

Given the complexity of existing photobooth software, and how much I enjoy
classic photobooths, I decided to script up something that simple takes four
pictures on a timer and adds them to a strip.

Not satisfied with the simplicity of outputting a normal strip, I also added
animated GIF support. Every quarter second during the given wait_time, an image
is taken and compiled into an animated photobooth strip.

# Requirements

- Python 2.7+
- numpy 1.11.0+ (Python package)
- Pillow 3.2.0+ (Python package)
- OpenCV 3.0.0+ (Python package)

# Use

Simply run "python photobooth.py" to start the photobooth.

# Configuration

There are a number of configuration settings that can be changed in the script,
which can be found/changed near the top of the file. Here's descriptions of
each:

- camera_port
 - The port of the webcam. Defaults to 0.
- ramp_frames
 - The amount of frames to "warm up" (calibrate/focus) the camera.
- strip_rows
 - Number of rows in the strip. Defaults to 4.
- strip_columns
 - Number of columns in the strip. Defaults to 2.
- strip_width
 - The width of the photostrip in pixels. Defaults to 1200.
- strip_height
 - The height of the photostrip in pixels. Defaults to 1800.
- footer
 - The image file to use in the footer, if present.
- gif_width
 - The width of the animated gif, in pixels. Should be relative to the width of
 one column to maintain aspect ratio. Defaults to 300.
- gif_height
 - The height of the animated gif, in pixels. Defaults to 900.
- gif_row_gutter
 - The gutter between rows of images in the animated gif strip, in pixels.
 Defaults to 7.
- gif_footer
 - The image file to use in the animated gif's footer, if present.
- row_gutter
 - The gutter between rows of images in the animated gif strip, in pixels.
 Defaults to 7.
- column_gutter
 - The gutter between columns in the strip, in pixels. Defaults to 10.
- wait_time
 - The amount of time to wait between shots, in seconds. Defaults to 3.
- column_grayscale
 - A list defining what columns should have a grayscale effect applied to them.
 Defaults to (0, 1), which will make the second column grayscaled. Ideally this
 would map common image filters to columns.
