# Binocle Viewer Bulk Image Downloader

This program is a pet project created to solve a personal problem: efficiently downloading multiple images from websites using the Binocle Viewer. It's specifically designed for various archives and [historical document repositories](https://www.google.com/search?q=Binocle+2.10.14.alpha-1).

## Features

- Download multiple images from Binocle Viewer-based websites
- Customizable number of images to download

## How to Use

1. Enter the URL of the Binocle Viewer page you want to download images from.
2. Specify the number of images you want to download.
3. Set the timeout in seconds (default is 30 seconds).
4. Click the "Download" button to start the process.
5. Monitor the progress in the log area and progress bar.
6. Once complete, use the "Open Download Folder" button to access your images.

## Compatibility

This program is designed to work with websites using Binocle Viewer version 2.10.14.alpha-1 and similar versions. It has been tested with various archive websites, including:

- Archives départementales des Hautes-Alpes (https://archives.hautes-alpes.fr/)
- Archives de Nîmes (https://archives.nimes.fr/)
- Archives départementales des Bouches-du-Rhône (https://archives13.fr/)
- Archives Bordeaux Métropole (https://archives.bordeaux-metropole.fr/)
- Archives de Marseille (https://archives.marseille.fr/)
- Patrimoine et archives de Chelles (https://archives.chelles.fr/)
- Archives du Val-d'Oise (https://archives.valdoise.fr/)

For more examples of compatible websites, you can check this Google search:
https://www.google.com/search?q=Binocle+2.10.14.alpha-1

## Usage

Simply run the executable file provided in the release.


## Technical Details

The source code for this application is available in the `main.py` file. The program uses the following libraries:

- Playwright: For web automation and image downloading
- CustomTkinter: For creating the graphical user interface


## Note

This tool is intended for personal use and research purposes only. It is designed to facilitate easier and faster downloading of already publicly visible content on archiving websites. This program does not intend to steal or misuse any content. It is simply a tool that automates the process of downloading images that are already accessible to the public.

Please respect copyright laws and terms of service of the websites you're accessing. Always ensure you have the right to download and use the content for your intended purposes.