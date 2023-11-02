# Spotify To MP3 Converter

This Python program allows you to get all your liked songs from Spotify and tries to download them as an MP3 (320kbps). Follow the instructions below to set up and use the application.

## Setup

### 1. Spotify Developer Account

- Change the name of the dotenv file to `.env`.
- Go to [Spotify Developer](https://developer.spotify.com/) and log in with your Spotify account.
- Navigate to the [Dashboard](https://developer.spotify.com/dashboard).
- Create a new application.
- Copy the client ID and client secret and paste them into the corresponding fields (`SPOTIPY_CLIENT_ID` and `SPOTIPY_CLIENT_SECRET`) in the `.env` file.

### 2. Music Download Folder

- Copy the path to the folder where you want to download music.
- Paste the path into the `music_download_folder` field in the `.env` file.

### 3. Gmail Account for Notifications

- Generate an [application password](https://pythonaddict.com/how-to-generate-google-application-password/) for your Gmail account.
- Paste your email address into the `EMAIL_ADDRESS` field in the `.env` file.
- Paste the application password into the `EMAIL_PASSWORD` field in the `.env` file.
- Specify the email where you want to receive notifications by pasting it into the `TO_EMAIL` field in the `.env` file.

## Setting Up the Browser

- Set your browser's download folder to the one specified in the `music_download_folder` field in the `.env` file.

## Setting Up Assets

Assets are located in the `assets` folder. Replace the pre-loaded assets by following the instructions below:

- **download_1.png and download_1_alt_1.png:** These represent the download button when you search for a song.
- **captcha.png:** This indicates the box where the captcha must be clicked. Ensure the box is centered in the image.
- **captcha_complete.png:** This is the checkmark that appears when a captcha is complete.

## Usage

- Run the `Spotify-To-MP3.py` file.
- Press Enter to start, then switch to your browser.
- To quit the program, hold 'q' for a few seconds.
