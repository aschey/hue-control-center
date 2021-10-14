import re
import requests
import yaml
import time
import os
from qhue import Bridge
from colormath.color_objects import sRGBColor, xyYColor
from colormath.color_conversions import convert_color
from dotenv import load_dotenv

load_dotenv()


def correct_xyz2rgb_gamma(channel):
    """
    Correct the gamma of a channel during an XYZ to sRGB conversion.
    Args:
        channel: the channel to correct the gamma of
    Returns:
        the channel after correcting the gamma
    """
    # apply the correction
    if channel <= 0.0031308:
        channel = channel * 12.92
    else:
        channel = 1.055 * pow(channel, (1.0 / 2.4)) - 0.055
    # normalize channel as int in [0, 255]
    return min(255, max(0, int(channel * 255)))


def xy_bri_to_rgb(x, y, brightness):
    """
    Convert an XY-Brightness color to RGB.
    Args:
        x: the x value of the color [0.0, 1.0]
        y: the y value of the color [0.0, 1.0]
        brightness: the brightness value of the color [0, 254]
    Returns:
        an RGB tuple
    """
    z = 1.0 - x - y
    # calculate the XYZ values
    Y = brightness / 255.0
    X = (Y / y) * x
    Z = (Y / y) * z
    # Wide gamut conversion D65 and correct gamma
    r = correct_xyz2rgb_gamma(X * 1.656492 - Y * 0.354851 - Z * 0.255038)
    g = correct_xyz2rgb_gamma(-X * 0.707196 + Y * 1.655397 + Z * 0.036152)
    b = correct_xyz2rgb_gamma(X * 0.051713 - Y * 0.121364 + Z * 1.011530)
    return r, g, b


def correct_rgb2xyz_gamma(channel):
    """
    Correct the gamma of a channel during an XYZ to sRGB conversion.
    Args:
        channel: the channel to correct the gamma of
    Returns:
        the channel after correcting the gamma
    """
    # normalize channel in [0, 1]
    channel /= 255
    # apply the correction
    if channel > 0.04045:
        channel = pow((channel + 0.055) / 1.055, 2.4)
    else:
        channel = channel / 12.92
    return channel


def rgb_to_xy_bri(r, g, b):
    """
    Convert a color from RGB color space to x,y Brightness for Philips hue.
    Args:
        rgb: an RGB tuple
    Returns:
        a tuple of
        - the x,y values
        - the brightness
    """
    # correct the gamma
    r = correct_rgb2xyz_gamma(r)
    g = correct_rgb2xyz_gamma(g)
    b = correct_rgb2xyz_gamma(b)
    # Wide gamut conversion D65
    X = r * 0.664511 + g * 0.154324 + b * 0.162028
    Y = r * 0.283881 + g * 0.668433 + b * 0.047685
    Z = r * 0.000088 + g * 0.072310 + b * 0.986039
    # calculate the denominator to prevent any divide by zero errors
    denominator = X + Y + Z
    x = X / denominator if denominator > 0 else 0
    y = Y / denominator if denominator > 0 else 0
    # return the x, y tuple and shift and bound the brightness
    return (x, y), min(255, max(0, int(Y * 255.0)))


def hex_to_rgb(hx, hsl=False):
    """Converts a HEX code into RGB or HSL.
    Args:
        hx (str): Takes both short as well as long HEX codes.
        hsl (bool): Converts the given HEX code into HSL value if True.
    Return:
        Tuple of length 3 consisting of either int or float values.
    Raise:
        ValueError: If given value is not a valid HEX code."""
    if re.compile(r"#[a-fA-F0-9]{3}(?:[a-fA-F0-9]{3})?$").match(hx):
        div = 255.0 if hsl else 0
        if len(hx) <= 4:
            return tuple(
                int(hx[i] * 2, 16) / div if div else int(hx[i] * 2, 16)
                for i in (1, 2, 3)
            )
        return tuple(
            int(hx[i : i + 2], 16) / div if div else int(hx[i : i + 2], 16)
            for i in (1, 3, 5)
        )
    raise ValueError(f'"{hx}" is not a valid HEX code.')


res = requests.get("https://discovery.meethue.com")
bridge_ip = res.json()[0]["internalipaddress"]
username = os.environ["HUE_USERNAME"]
bridge = Bridge(bridge_ip, username)

colors = [
    "#8FBCBB",
    "#D08770",
    "#88C0D0",
    "#81A1C1",
    "#A3BE8C",
    "#B48EAD",
]
index1 = 0
index2 = 1
while True:
    r1, g1, b1 = hex_to_rgb(colors[index1])
    r2, g2, b2 = hex_to_rgb(colors[index2])
    index1 = (index1 + 1) % len(colors)
    index2 = (index2 + 1) % len(colors)
    res1 = rgb_to_xy_bri(r1, g1, b1)
    res2 = rgb_to_xy_bri(r2, g2, b2)
    bridge.lights[1].state(xy=[res1[0][0], res1[0][1]], bri=res1[1], transitiontime=600)
    bridge.lights[2].state(xy=[res2[0][0], res2[0][1]], bri=res2[1], transitiontime=600)
    time.sleep(60)
