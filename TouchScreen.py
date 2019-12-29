from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

import ILI9341local as TFT
#import Adafruit_GPIO as GPIO
#import Adafruit_GPIO.SPI as SPI
import gpiozero
import spidev


class Displaymgr():
    """Class to manage touch LCD Display on Raspberry Pi ZeroW

    Attributes:
        

    Methods:
        pane (str): Name of Display Pane
        clearscreen(colour): Clear Screen to specified.
        refreshscreen(): Write buffer to screen
        
    """
    
    def __init__(self, pane):
        self.pane = pane
        # Raspberry Pi configuration.
        DC = 25
        SPI_PORT = 0
        SPI_DEVICE = 0
        displaysize = (320, 240)

        tftspi = spidev.SpiDev()
        tftspi.open(SPI_PORT, SPI_DEVICE)
        tftspi.mode = 0b00
        tftspi.max_speed_hz = 100000000
        

        print("tftspi instantiated")

        # Create TFT LCD display class.
        self.pane = TFT.ILI9341(DC, spi=tftspi,width=240,height=320)

        # Initialize display.
        self.pane.begin()

        self.image = Image.new('RGB', displaysize, 'white')
        self.draw = ImageDraw.ImageDraw(self.pane.buffer)

    def clearscreen(self,background=(0,0,0)):
        self.pane.clear(background)
        
        
    def refreshscreen(self):
        self.pane.display()


    def drawgrid(self,gridcolour):
        print('Drawing Grid')
        self.draw.line((60, 0, 60, 319), width=1, fill=gridcolour)
        self.draw.line((120, 0, 120, 319), width=1, fill=gridcolour)
        self.draw.line((180, 0, 180, 319), width=1, fill=gridcolour)
        self.draw.line((0, 64, 239, 64), width=1, fill=gridcolour)
        self.draw.line((0, 128, 239, 128), width=1, fill=gridcolour)
        self.draw.line((0, 192, 239, 192), width=1, fill=gridcolour)
        self.draw.line((0, 256, 239, 256), width=1, fill=gridcolour)
        
        
    def drawlamp(self,gridcolour,light,x,y):
        if light == 'On':
            lampstate = gridcolour
        else:
            lampstate = (0,0,127)
        self.draw.ellipse((x, y, x+30, y+30), fill=lampstate, outline=gridcolour)
        

    def draw_rotated_text(self,  text, position, angle, fill=(255,255,255)):
        # Get rendered font width and height.
        # print('Start Rotated Text')
        draw = ImageDraw.Draw(self.pane.buffer)
        self.font = ImageFont.load_default()
        width, height = draw.textsize(text, font=self.font)
        # print('Width {} Height {}'.format(width,height))
        # Create a new image with transparent background to store the text.
        textimage = Image.new('RGBA', (width, height), (0,0,0,0))
        # Render the text.
        #textdraw = ImageDraw.Draw(textimage)
        textdraw = ImageDraw.Draw(textimage)
        textdraw.text((0,0), text, font=self.font, fill=fill)
        # Rotate the text image.
        rotated = textimage.rotate(angle, expand=1)
        # Paste the text into the image, using it as a mask for transparency.
        self.pane.buffer.paste(rotated, position, rotated)