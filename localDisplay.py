# Local Display Utilities

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

import ILI9341local as TFT
#import Adafruit_GPIO as GPIO
#import Adafruit_GPIO.SPI as SPI
import gpiozero
import spidev


def initDisp():
    global nextline
    global DisplayLog
    global disp
    # Raspberry Pi configuration.
    DC = 25
    SPI_PORT = 0
    SPI_DEVICE = 0


    tftspi = spidev.SpiDev()
    tftspi.open(SPI_PORT, SPI_DEVICE)
    tftspi.mode = 0b00
    tftspi.max_speed_hz = 100000000

    print("tftspi instantiated")


    # Create TFT LCD display class.
    disp = TFT.ILI9341(DC, spi=tftspi)

    # Initialize display.
    disp.begin()

    disp.clear((0, 0, 127))
    disp.display()

    nextline = 0

    DisplayLog = [""] * 20
    for i in range(0,20):
        DisplayLog[i] = ""
    # Load default font.
    

# Define a function to create rotated text.  Unfortunately PIL doesn't have good
# native support for rotated fonts, but this function can be used to make a
# text image and rotate it so it's easy to paste in the buffer.


def draw_rotated_text(image, text, position, angle, font, fill=(255,255,255)):
    # Get rendered font width and height.
    draw = ImageDraw.Draw(image)
    width, height = draw.textsize(text, font=font)
    # Create a new image with transparent background to store the text.
    textimage = Image.new('RGBA', (width, height), (0,0,0,0))
    # Render the text.
    textdraw = ImageDraw.Draw(textimage)
    textdraw.text((0,0), text, font=font, fill=fill)
    # Rotate the text image.
    rotated = textimage.rotate(angle, expand=1)
    # Paste the text into the image, using it as a mask for transparency.
    image.paste(rotated, position, rotated)
    gridcolour = (191, 191, 0)
    draw.line((60, 0, 60, 319), width=1, fill=gridcolour)
    draw.line((120, 0, 120, 319), width=1, fill=gridcolour)
    draw.line((180, 0, 180, 319), width=1, fill=gridcolour)
    draw.line((0, 64, 239, 64), width=1, fill=gridcolour)
    draw.line((0, 128, 239, 128), width=1, fill=gridcolour)
    draw.line((0, 192, 239, 192), width=1, fill=gridcolour)
    draw.line((0, 256, 239, 256), width=1, fill=gridcolour)
    draw.ellipse((10, 275, 40, 305), fill=gridcolour, outline=gridcolour)
    disp.display()


def send2screen(displine):
    global nextline
    global DisplayLog
    global disp
    font = ImageFont.load_default()
    DisplayLog[nextline] = str(displine)
    nextline += 1
    disp.clear((0, 0, 127))
    if nextline > 14:
        nextline -= 15
    for i in range(0, 15):
        showline = (i + nextline) % 15
        draw_rotated_text(disp.buffer, DisplayLog[showline], (i * 15, 0), 90, font, fill=(191,191,0))
        
    disp.display()

def drawgrid(draw):
    #draw = ImageDraw.Draw(disp.buffer)
    gridcolour = (191,191,0)
    draw.line((60,0,60,319), width=1, fill=gridcolour)
    draw.line((120, 0, 120, 319), width=1, fill=gridcolour)
    draw.line((180, 0, 180, 319), width=1, fill=gridcolour)
    draw.line((0, 64, 239, 64), width=1, fill=gridcolour)
    draw.line((0, 128, 239, 128), width=1, fill=gridcolour)
    draw.line((0, 192, 239, 192), width=1, fill=gridcolour)
    draw.line((0, 256, 239, 256), width=1, fill=gridcolour)
    draw.ellipse((5, 260, 45, 300), fill=gridcolour,outline=gridcolour,width=1)
    disp.display()

def labelgrid(text, place, rotation, colour):
    font = ImageFont.load_default()
    draw_rotated_text(disp.buffer, text, place, rotation, font, fill=colour)


def placeonscreen(displine, place ):
    global nextline
    global DisplayLog
    global disp
    font = ImageFont.load_default()
    draw_rotated_text(disp.buffer, displine, place, 90, font, fill=(191, 191, 0))
    disp.display()