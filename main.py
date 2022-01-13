import os
import requests
from PIL import Image
import threading

SUBDIRECTORY = "downloads"
timeout_seconds = int(input("HTTP connection timeout in seconds (20 is recommended): "))
num_of_threads = int(input("Number of download threads to use (25 is recommended): "))
print()
header = {"User-Agent": "Mozilla/5.0 (X11; CrOS x86_64 12871.102.0) "
                        "AppleWebKit/537.36 (KHTML, like Gecko) "
                        "Chrome/81.0.4044.141 Safari/537.36"}

if not os.path.isdir(SUBDIRECTORY):
    os.mkdir(SUBDIRECTORY)

with open("imgs.txt") as f:
    links = f.readlines()
    links = [link.strip("\n") for link in links if link.startswith("https://")]

url_errors = 0
empty_images = 0
total_downloaded = 0
threads = []


def download_image(threadno):
    global total_downloaded
    global url_errors
    while total_downloaded <= len(links):
        try:
            url = links[total_downloaded]
        except IndexError:
            break
        file_name = url.split("/")[-1]
        progress_percent = round((total_downloaded) / len(links) * 100, 2)
        print(f"Downloading image #{total_downloaded + 1} ({progress_percent}%)    ", end="\r")
        try:
            f = open(f"{SUBDIRECTORY}/{file_name}", 'wb')
            response = requests.get(url, headers=header, timeout=(timeout_seconds, timeout_seconds))
            f.write(response.content)
            f.close()
        except:
            url_errors += 1
        total_downloaded += 1

for i in range(num_of_threads):
    t = threading.Thread(target=download_image, args=(i,))
    threads.append(t)

for t in threads:
    t.start()

for t in threads:
    t.join()

print("\nAll files downloaded.")
print(f"Success rate: {round(((len(links) - url_errors) / len(links)) * 100, 2)}% ({len(links) - url_errors} successful, {url_errors} failed)")
input("\nPress [Enter] to delete empty images. Press [Ctrl] + [C] to skip this check and exit the script.")
print("Deleting empty images...\n")

file_number = 0
for file in os.listdir(SUBDIRECTORY):
    f = os.path.join(SUBDIRECTORY, file)
    if os.path.isfile(f):
        try:
            im = Image.open(f)
            image_rgb = im.convert("RGB").getpixel((1, 1))
            if image_rgb == (0, 0, 0):
                os.remove(f)
                print(f"({round(file_number / (len(links) - url_errors) * 100, 2)}%) Removed {file}: Reddit image not found    ", end="\r")
                empty_images += 1
            elif image_rgb == (34, 34, 34):
                os.remove(f)
                print(f"({round(file_number / (len(links) - url_errors) * 100, 2)}%) Removed {file}: Imgur image not found    ", end="\r")
                empty_images += 1
            else:
                pass
        except:
            pass
    file_number += 1

print(f"\nAll empty images deleted: {len(links) - url_errors - empty_images} downloaded, {empty_images} empty images")
