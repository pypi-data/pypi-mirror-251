

import sys
import os

data_frame_size = 4000

cmd = f'ffmpeg -y -r 1/5 -s 1080x1620 -i output/%03d.png -vcodec libx264 -crf 25 ~/html/rs/video/video{data_frame_size}.mp4'
os.system(cmd)

#----delete images
cmd = 'rm /home/vixen/rs/dev/src/output/*'
os.system(cmd)