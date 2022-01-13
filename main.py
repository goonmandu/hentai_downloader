import os
import requests
from PIL import Image
import time
import random

SUBDIRECTORY = "downloads"

if not os.path.isdir(SUBDIRECTORY):
    os.mkdir(SUBDIRECTORY)

with open("imgs.txt") as f:
    links = f.readlines()
    links = [link.strip("\n") for link in links if link.startswith("https://")]

url_errors = 0
empty_images = 0

for index, url in enumerate(links):
    file_name = url.split("/")[-1]
    print(f"Retrieving item #{index+1} ({round((index + 1) / len(links) * 100, 2)}%)", end="")
    try:
        f = open(f"{SUBDIRECTORY}/{file_name}", 'wb')
        response = requests.get(url)
        f.write(response.content)
        f.close()
        print(" ... Done")
    except:
        print(" ... Error (Skipped)")
        url_errors += 1
    time.sleep(random.uniform(0.2, 0.25))

print("\nAll files downloaded.")
print(f"Success rate: {round(((len(links) - url_errors) / len(links)) * 100, 2)}% ({len(links) - url_errors} successful, {url_errors} failed)")
input("\nPress [Enter] to delete empty images. Press [Ctrl] + [C] to skip this check and exit the script.")
print("Deleting empty images...\n")

for file in os.listdir(SUBDIRECTORY):
    f = os.path.join(SUBDIRECTORY, file)
    if os.path.isfile(f):
        try:
            im = Image.open(f)
            image_rgb = im.convert("RGB").getpixel((1, 1))
            if image_rgb == (0, 0, 0):
                os.remove(f)
                print(f"Removed {file}: Reddit image not found")
                empty_images += 1
            elif image_rgb == (34, 34, 34):
                os.remove(f)
                print(f"Removed {file}: Imgur image not found")
                empty_images += 1
            else:
                pass
        except:
            pass

print(f"\nAll empty images deleted: {len(links) - url_errors - empty_images} downloaded, {empty_images} empty images")
