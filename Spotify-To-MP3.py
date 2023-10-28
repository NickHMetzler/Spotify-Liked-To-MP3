import time
import pyautogui
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
from dotenv import load_dotenv
import re

music_doanload_folder = r'C:\Users\nickf\Downloads\hades-main\Music'

client_id = os.environ.get('SPOTIPY_CLIENT_ID')
client_secret = os.environ.get('SPOTIPY_CLIENT_SECRET')
redirect_uri = os.environ.get('SPOTIPY_REDIRECT_URI')


def delete_files_with_pattern(folder_path):
    # List all files in the specified folder
    files = os.listdir(folder_path)

    # Define the regular expression pattern
    pattern = re.compile(r'\(\d+\)\.mp3$')

    # Iterate through each file in the folder
    for file_name in files:
        file_path = os.path.join(folder_path, file_name)

        # Check if the file matches the pattern
        if pattern.search(file_name):
            try:
                # Delete the file
                os.remove(file_path)
                print(f"Deleted: {file_name}")
            except Exception as e:
                print(f"Error deleting {file_name}: {e}")

# Specify the folder path
folder_path = "/path/to/your/folder"

# Call the function to delete files with the specified pattern
delete_files_with_pattern(folder_path)

# Load environment variables from .env
load_dotenv()

# Set up Spotify API credentials
SPOTIPY_CLIENT_ID = os.getenv("SPOTIPY_CLIENT_ID")
SPOTIPY_CLIENT_SECRET = os.getenv("SPOTIPY_CLIENT_SECRET")
SPOTIPY_REDIRECT_URI = os.getenv("SPOTIPY_REDIRECT_URI")

scope = "user-library-read"
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID,
                                               client_secret=SPOTIPY_CLIENT_SECRET,
                                               redirect_uri=SPOTIPY_REDIRECT_URI,
                                               scope=scope))

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

liked_songs = get_liked_songs()

song_list = []
for song in liked_songs:
    track = song['track']
    title_artist = f"{track['name']} {', '.join([artist['name'] for artist in track['artists']])}"
    song_list.append(title_artist)

def is_song_in_directory(song_name):
    directory = r'C:\Users\nickf\Downloads\hades-main\Music'
    for filename in os.listdir(directory):
        index = filename.find("- ") + 2
        name = filename[index:]
        name = name.split(".mp3")[0]
        if name.lower() in song_name.lower():
            return True
    return False


# Set the delay to give you time to switch to the browser window
initial_delay = 5

print("Starting!")
# Loop through the search terms
for term in song_list:
    
    if is_song_in_directory(term):
        print(f"Skipping {term}, already in the directory.")
        continue

    i = 0
    found_flag = False
    while i < 2 and not found_flag:
        # Delay before starting to allow switching to the browser
        time.sleep(initial_delay)

        # Open your browser and go to the localhost address
        # (Make sure your browser window is active before running the script)
        pyautogui.hotkey("ctrl", "w")
        pyautogui.hotkey("ctrl", "t")
        pyautogui.write("https://free-mp3-download.net")
        pyautogui.press("enter")

        # Wait for the page to load
        time.sleep(2)

        # Locate and click the first button (replace coordinates with actual values)
        if pyautogui.locateOnScreen('assets/Search_Box.png') is not None:
            button_x, button_y = pyautogui.locateCenterOnScreen('assets/Search_Box.png')
            pyautogui.click(button_x, button_y)
        else:
            print("Search Box not found")
            
        pyautogui.write(term)

        # Press Enter
        pyautogui.press("enter")

        # Wait for search results to load
        time.sleep(3)
        print("Finding first DL")
        for file in ["download_1", "download_1_alt_1"]:
            if pyautogui.locateOnScreen(rf'C:\Users\nickf\OneDrive\Documents\Downloader\assets\{file}.png', grayscale=False, confidence=0.95) is not None:
                print("Found first DL")
                button_x, button_y = pyautogui.locateCenterOnScreen(rf'C:\Users\nickf\OneDrive\Documents\Downloader\assets\{file}.png', grayscale=False, confidence=0.95)
                pyautogui.click(button_x, button_y)
                found_flag = True
                break
            else:
                print("Results Download Button not found, moving to the next search term.")
        i += 1
        
        

    time.sleep(2)
    # Scroll down a bit
    pyautogui.press("pagedown")

    # Click another button (replace coordinates with actual values)
    if pyautogui.locateOnScreen(r'C:\Users\nickf\OneDrive\Documents\Downloader\assets\captcha.png') is not None:
        another_button_x, another_button_y = pyautogui.locateCenterOnScreen(r'C:\Users\nickf\OneDrive\Documents\Downloader\assets\captcha.png')
        pyautogui.click(another_button_x, another_button_y)
    else:
        print("Captcha not found, moving to the next search term.")
    
    # Locate and click the first button (replace coordinates with actual values)
    if pyautogui.locateOnScreen(r'C:\Users\nickf\OneDrive\Documents\Downloader\assets\download_2.png') is not None:
        button_x, button_y = pyautogui.locateCenterOnScreen(r'C:\Users\nickf\OneDrive\Documents\Downloader\assets\download_2.png')
        pyautogui.click(button_x, button_y)
    else:
        print("Results Download Button not found, moving to the next search term.")
        
    # Add a delay before moving to the next iteration
    time.sleep(10)

# End of the script
