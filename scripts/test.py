from moviepy.editor import TextClip
import moviepy.config as mpy_conf

mpy_conf.change_settings({"IMAGEMAGICK_BINARY": "C:/Program Files/ImageMagick-7.1.1-Q16-HDRI/magick.exe"})

clip = TextClip("Hello world!", fontsize=70, color="white", font="Arial-Bold", method='caption')
clip.save_frame("test_text.png")
