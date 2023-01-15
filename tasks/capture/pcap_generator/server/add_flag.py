import sys

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

flag = sys.argv[1] 

picture = Image.open('/root/pic.jpg')
height = picture.size[1]
flag_font = ImageFont.truetype("/root/jb-mono.ttf", height // 20)

draw = ImageDraw.Draw(picture)
draw.text((20,20), flag, fill=(0,0,0), font=flag_font)

picture.save('/root/output/hacker.jpg')
