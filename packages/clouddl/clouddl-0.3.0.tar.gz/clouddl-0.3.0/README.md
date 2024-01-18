# clouddl

Downloader for Google Drive & DropBox

- Python 3 
- Works on all operating systems
- No API keys / credentials needed
- Auto extracts .zip files
- Auto extracts .rar files (requires 7zip)
- Auto deletes compressed files after extraction

## Installation 
```console
pip install clouddl
```

## Usage
```python3
from clouddl import grab

# grab(url, folder_path)
grab('https://drive.google.com/file/d/.../view?usp=sharing', './Downloads/')
```

## Verbose
```python3
from clouddl import grab
#grab(url, folder_path, quiet=False)
grab('https://drive.google.com/file/d/.../view?usp=sharing', './Downloads/', quiet=False)
```

## Bulk Usage
```python3
from clouddl import grab

download_list = ['URL1', 'URL2', 'URL3']

for url in download_list:
 grab(url, './')
```

## Variable Access
```python3
from clouddl import DROPBOX_URL, GDRIVE_URL
```
## Supported URLs
Google Drive
```txt
https://drive.google.com/drive/folders/...?usp=sharing
https://drive.google.com/file/d/.../view?usp=sharing
```
Dropbox
```txt
https://www.dropbox.com/s/.../...?dl=0
https://www.dropbox.com/s/.../...?dl=1
https://www.dropbox.com/sh/.../...?dl=0
https://www.dropbox.com/sh/.../...?dl=1
```
 
## Acknowledgements 
 
Thank you to the authors of the following repos:
- "gdrivedl" by matthuisman - https://github.com/matthuisman/gdrivedl
- "lootdl" by jesusyanez - https://github.com/jesusyanez/lootdl
