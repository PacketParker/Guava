import requests
import re

from utils.config import LOG

"""
Search through the JS files on the Apple Music website to pull
a media API key
"""


def get_media_api_key():
    url = "https://music.apple.com"
    response = requests.get(url)

    js_files = re.findall(r"assets/(.*?\.js)", response.text)

    # Look for `const Ga="TOKEN HERE"`
    for js_file in js_files:
        response = requests.get(f"{url}/assets/{js_file}")
        # "(?<token>(ey[\w-]+)\.([\w-]+)\.([\w-]+))" - Credit to https://github.com/topi314/LavaSrc
        match = re.search(r'"(?P<token>ey[\w-]+\.[\w-]+\.[\w-]+)"', response.text)
        if match:
            return match.group(1)

    LOG.error(
        "Failed to find media API key. Apple Music support will not work until a key is found or manually set."
    )
    return None
