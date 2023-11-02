###########################
#                         #
#         Imports         #
#                         #
###########################

import time
import pyautogui
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
from dotenv import load_dotenv
import re
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from datetime import datetime
import keyboard

###########################
#                         #
#        Variables        #
#                         #
###########################

# Load environment variables from .env
load_dotenv()

music_download_folder = os.getenv("music_download_folder")
download_link = "https://free-mp3-download.net"

# Set up Spotify API credentials
SPOTIPY_CLIENT_ID = os.getenv("SPOTIPY_CLIENT_ID")
SPOTIPY_CLIENT_SECRET = os.getenv("SPOTIPY_CLIENT_SECRET")
SPOTIPY_REDIRECT_URI = os.getenv("SPOTIPY_REDIRECT_URI")

# Set the delay to give you time to switch to the browser window
delay = 5
first = True
# Initialize a set to store the list of downloaded filenames
song_filename_dict = {}
text_file_path = 'liked_songs.txt'



###########################
#                         #
#        Functions        #
#                         #
###########################

# Allow the use of relative paths
os.chdir(os.path.dirname(__file__))
script_folder = os.path.dirname(__file__)
# Change the permissions of all files in the script's folder to allow all users to read and write to them
for file in os.listdir(script_folder):
    file_path = os.path.join(script_folder, file)
    os.chmod(file_path, 0o666)

def get_most_recently_downloaded_filename(directory):
    files = [f for f in os.listdir(directory) if f.endswith('.mp3')]  # Adjust the extension as needed
    if not files:
        return None

    files_with_paths = [os.path.join(directory, f) for f in files]
    latest_file = max(files_with_paths, key=os.path.getmtime)
    
    return latest_file

def load_song_filename_dict(file_path):
    song_filename_dict = {}
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            for line in file:
                liked_song, filename = line.strip().split(' : ')
                song_filename_dict[liked_song] = filename
    return song_filename_dict

# Function to send an email
def send_email(subject, message):
    # Load email credentials from .env file
    email_address = os.getenv("EMAIL_ADDRESS")
    email_password = os.getenv("EMAIL_PASSWORD")

    # Recipient email address
    to_email = os.getenv("TO_EMAIL")

    # Email server setup (for Gmail in this example)
    smtp_server = "smtp.gmail.com"
    smtp_port = 587

    # Create the email message
    msg = MIMEMultipart()
    msg['From'] = email_address
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(message, 'plain'))

    try:
        # Login to the email server
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(email_address, email_password)

        # Send the email
        server.sendmail(email_address, to_email, msg.as_string())
        print("Email sent successfully!")
    except Exception as e:
        print(f"Error sending email: {e}")
    finally:
        # Close the server connection
        server.quit()

def delete_files_with_pattern(folder_path):
    # List all files in the specified folder
    files = os.listdir(folder_path)

    # Define the regular expression pattern
    pattern = re.compile(r'\(\d+\)\.mp3$')

    i = 0
    # Iterate through each file in the folder
    for file_name in files:
        file_path = os.path.join(folder_path, file_name)

        # Check if the file matches the pattern
        if pattern.search(file_name):
            try:
                # Delete the file
                os.remove(file_path)
                print(f"Deleted: {file_name}")
                i += 1
            except Exception as e:
                print(f"Error deleting {file_name}: {e}")

    print(f"Deleted {i} Duplicate Files")

def is_song_in_directory(song_name):
    directory = music_download_folder
    for filename in os.listdir(directory):
        index = filename.find("- ") + 2
        name = filename[index:]
        name = name.split(".mp3")[0]
        if name.lower() in song_name.lower():
            return True
    return False


def get_liked_songs():
    offset = 0
    limit = 50
    songs = []

    while True:
        results = sp.current_user_saved_tracks(limit=limit, offset=offset)
        items = results['items']

        if not items:
            break

        songs.extend(items)
        offset += limit
        
    return songs



###########################
#                         #
#          Code           #
#                         #
###########################

song_filename_dict = load_song_filename_dict(text_file_path)

scope = "user-library-read"
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID,
                                               client_secret=SPOTIPY_CLIENT_SECRET,
                                               redirect_uri=SPOTIPY_REDIRECT_URI,
                                               scope=scope))

print("CONSOLE: Initializing Liked Songs...")
liked_songs = get_liked_songs()

song_list = []
for song in liked_songs:
    track = song['track']
    title_artist = f"{track['name']} {', '.join([artist['name'] for artist in track['artists']])}"
    title_artist = title_artist.replace(',', '')
    song_list.append(title_artist)


input("\nPlease set the Download Location in the browser to the same as in .env\nSongs Initialized: Press Enter to Start: ")
print("\nCONSOLE: Please switch to the browser window")
i = 5
while i > -1:
    print(f"CONSOLE: Starting downloader in {i} seconds...")
    time.sleep(1)
    i -= 1

# Call the function to delete files with the specified pattern
print("CONSOLE: Deleting duplicate MP3 Files...")
delete_files_with_pattern(music_download_folder)

last_song = get_most_recently_downloaded_filename(music_download_folder)

# Loop through the search terms
for liked_song in song_list:
    if keyboard.is_pressed('q'):
        break
    if liked_song in song_filename_dict:
        print(f"\nCONSOLE: Skipping {liked_song}, already in the directory.")
        continue
    
    print(f"\nCONSOLE: Trying to Download {liked_song}")

    i = 0
    found_flag = False
    while i < 2 and not found_flag and not keyboard.is_pressed('q'):
        
        # Add a delay to the start
        time.sleep(delay)

        # Close the old tab and open a new tab to search
        if first != True:
            pyautogui.hotkey("ctrl", "w")
        else:
            first = False
        time.sleep(int(delay/5))
        pyautogui.hotkey("ctrl", "t")
        time.sleep(int(delay/5))
        pyautogui.write(download_link)
        time.sleep(int(delay/5))
        pyautogui.press("enter")

        # Wait for the page to load
        time.sleep(int(delay/5))

        # Locate and click the first button (replace coordinates with actual values)
        if pyautogui.locateOnScreen('assets/Search_Box.png') is not None:
            button_x, button_y = pyautogui.locateCenterOnScreen('assets/Search_Box.png')
            print("CONSOLE: Search Box found")
            pyautogui.click(button_x, button_y)
        else:
            print("CONSOLE: Search Box not found")
            continue
            
        time.sleep(int(delay/3))

        pyautogui.write(liked_song)

        # Press Enter to search for the song
        pyautogui.press("enter")

        # Wait for search results to load
        time.sleep(int(delay/3))
        print("CONSOLE: Finding first Download Button")
        for file in ["download_1", "download_1_alt_1"]:
            if pyautogui.locateOnScreen(f'assets\{file}.png', grayscale=False, confidence=0.95) is not None:
                print(f"CONSOLE: Found first Download Button as {file}.png")
                button_x, button_y = pyautogui.locateCenterOnScreen(f'assets\{file}.png', grayscale=False, confidence=0.95)
                pyautogui.click(button_x, button_y)
                found_flag = True
                break
            else:
                print(f"CONSOLE: Did not find first Download Button as {file}.png")
        i += 1

    # If the song is not found, move onto the next song
    if found_flag == False:
        print("CONSOLE: Song not found, moving to the next song.")
        with open('liked_songs.txt', 'a') as file:
            file.write(f"{liked_song} : None\n")
        continue
    elif keyboard.is_pressed('q'):
        break
        
    time.sleep(int(delay/5))
    # Scroll down a bit
    pyautogui.press("pagedown")

    # Click the captcha
    if pyautogui.locateOnScreen('assets\captcha.png') is not None and not keyboard.is_pressed('q'):
        print("CONSOLE: Captcha found, clicking...")
        another_button_x, another_button_y = pyautogui.locateCenterOnScreen('assets\captcha.png')
        pyautogui.click(another_button_x, another_button_y)
        pyautogui.moveTo(100, 200)
        time.sleep(int(delay/5))
        # Add code for captcha text/email
        # Check if the image is found on the screen
        if not pyautogui.locateOnScreen('assets\captcha_complete.png'):
            print("CONSOLE: Captcha needs to be completed, waiting for human intervention")

            # Send an email
            subject = "CHECK PROGRAM"
            message = "Found Captcha on Downloader, human intervention required."
            send_email(subject, message)

            input("CONSOLE: Please Solve the Captcha\nCONSOLE: Press Enter to continue: ")
            print("\nCONSOLE: Please switch to the browser window")
            i = 5
            while i > -1:
                print(f"CONSOLE: Restarting downloader in {i} seconds...")
                time.sleep(1)
                i -= 1
    
        else:
            print("CONSOLE: Captcha is valid")
    elif keyboard.is_pressed('q'):
        break
    else:
        print("CONSOLE: Captcha not found.")
    
    # Locate and click the download button
    if pyautogui.locateOnScreen('assets\download_2.png') is not None and not keyboard.is_pressed('q'):
        print(f"CONSOLE: {liked_song} is being downloaded...")
        button_x, button_y = pyautogui.locateCenterOnScreen('assets\download_2.png')
        pyautogui.click(button_x, button_y)

        # Add a delay before moving to the next iteration
        time.sleep(delay * 3)
        
        # Update the dictionary and save to text file
        if last_song != get_most_recently_downloaded_filename(music_download_folder):
            song_filename_dict[liked_song] = get_most_recently_downloaded_filename(music_download_folder)
            last_song = song_filename_dict[liked_song]
            with open('liked_songs.txt', 'a') as file:
                file.write(f"{liked_song} : {song_filename_dict[liked_song]}\n")
        else:
            print("CONSOLE: Error with download, moving to the next song.")
    elif keyboard.is_pressed('q'):
        break
    else:
        print("CONSOLE: Download Button not found, moving to the next song.")
        
    

delete_files_with_pattern(music_download_folder)
# End of the script
