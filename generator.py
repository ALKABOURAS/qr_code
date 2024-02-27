import qrcode
from PIL import Image, ImageDraw


Logo_link = 'A-logo-white.png'
def add_corners(im, rad):
    circle = Image.new('L', (rad * 2, rad * 2), 0)
    draw = ImageDraw.Draw(circle)
    draw.ellipse((0, 0, rad * 2 - 1, rad * 2 - 1), fill=255)
    alpha = Image.new('L', im.size, 255)
    w, h = im.size
    alpha.paste(circle.crop((0, 0, rad, rad)), (0, 0))
    alpha.paste(circle.crop((0, rad, rad, rad * 2)), (0, h - rad))
    alpha.paste(circle.crop((rad, 0, rad * 2, rad)), (w - rad, 0))
    alpha.paste(circle.crop((rad, rad, rad * 2, rad * 2)), (w - rad, h - rad))
    im.putalpha(alpha)
    return im

logo = Image.open(Logo_link)
# for smooth corners add 300 to the radius. After solving the
# problem of the corners in the final qr
logo = add_corners(logo, 1)
# set logo background color
logo = logo.convert("RGBA")


# taking base width
basewidth = 100

# adjust image size
wpercent = (basewidth/float(logo.size[0]))
hsize = int((float(logo.size[1])*float(wpercent)))
logo = logo.resize((basewidth, hsize), Image.LANCZOS)



QRcode = qrcode.QRCode(
    error_correction=qrcode.constants.ERROR_CORRECT_H
)

# taking url or text
url = 'http://ieee.upatras.gr/links/'

# adding URL or text to QRcode
QRcode.add_data(url)

# generating QR code
QRcode.make()

# adding color to **QR** code not logo
QRimg = QRcode.make_image(
    fill_color="black", back_color="white").convert('RGBA')
# set size of QR code
pos = ((QRimg.size[0] - logo.size[0]) // 2,
       (QRimg.size[1] - logo.size[1]) // 2)
QRimg.paste(logo, pos)

# save the QR code generated
QRimg.save('ieee.png')

print('QR code generated!')
