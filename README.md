# hentai_downloader
An automatic image downloader from a predefined list of sources. Optional check at the end to remove empty images sourced from Reddit and Imgur.

# TODOs
- ~~Make progress bar instead of cascading download results.~~
  - Dropped progress bar in favor of constantly updating stdouts
- ~~Implement proper optional check instead of making the user raise a `KeyboardInterrupt`.~~
  - Done. See if there is a better way to exit the program without using `exit()`
- Make it run 2nd and 3rd passes to download failed images.
- Scan for duplicate files and empty images that have been downloaded from sources other than Reddit or Imgur.

# Screenshot:
![image](https://user-images.githubusercontent.com/61984863/149300333-8b384527-6c4a-4057-8dd4-318f0c9cd839.png)
