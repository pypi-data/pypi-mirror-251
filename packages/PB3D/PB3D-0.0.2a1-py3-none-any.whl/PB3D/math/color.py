import colorsys

class RGB:
    def __init__(self, red, green, blue):
        self.red = red
        self.green = green
        self.blue = blue

    def hsv(self):
        rgb = colorsys.rgb_to_hsv(self.red, self.green, self.blue)
        return RGB(rgb[0], rgb[1], rgb[2])

class HSV:
    def __init__(self, hue, saturation, value):
        self.hue = hue
        self.saturation = saturation
        self.value = value

    def rgb(self):
        rgb = colorsys.hsv_to_rgb((self.hue / 360), self.saturation, self.value)
        return RGB(rgb[0], rgb[1], rgb[2])
