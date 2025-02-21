import requests
from datetime import datetime
from bs4 import BeautifulSoup
import spotipy

# https://www.billboard.com/charts/hot-100/2000-08-12
# https://web.archive.org/web/20250202080938/https://www.billboard.com/

print("WELCOME TO THE MUSICAL TIME MACHINE\n"
      "Enter the month in this format [1 for january, 2 for February and so on...]")
wrong = True
while wrong:
    try :
        year = int(input("Enter the year you will like to go to\n"))
        month = int(input("The month\n"))
        date_guy = datetime(year=year, month=month, day=12)
        date = date_guy.strftime("%Y-%m-%d")
    except ValueError or NameError:
        print("❌❌❌\npls enter the values in the correct format\nHere we go again")
        continue
    wrong = False

    # Using an old version of website from web archive, The new one is rendered with js.
    try :
        headers = {
            'User-Agent': '*******************',
            "Accept-Language": "**************",
        }
        response = requests.get(url=f"https://web.archive.org/web/20240304020915/https://www.billboard.com/charts/hot-100/{date}/", headers=headers)
        web_data = response.text
    except requests.exceptions.ConnectionError :
        print("Pls check your internet connection⚠️⚠️⚠️")
        continue
    souppy = BeautifulSoup(web_data, "html.parser")

    raw_titles = souppy.select("li #title-of-a-story")

    # Striping the titles of all white spaces
    titles = [c.getText(strip=True) for c in raw_titles]   #Part 1 of day 46 finished
    print(titles)


    # Authenticating spotify
    from spotipy.oauth2 import SpotifyOAuth

    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id="***************",
                                                   client_secret="************",
                                                   redirect_uri="************",
                                                   scope="****************"))

    # results = sp.current_user_saved_tracks()
    # for idx, item in enumerate(results['items'], start=1) :
    #     track = item['track']
    #     print(idx, track['artists'][0]['name'], " – ", track['name'])

    # user = sp.current_user()  # Used to get user id
    user_id = "****************"


    # Creating the playlist
    my_playlist = sp.user_playlist_create(user=f"{user_id}", name=f"{year} Top Tracks with Python Time Machine", public=False,
                                          description="Top Tracks from back in the Days")
   

    ids = []
    for index, title in enumerate(titles, start=1) :
        try :
          bb = sp.search(q=title, type="track")
          track_id = bb["tracks"]["items"][0]["id"]
          ids.append(track_id)
          print(track_id)
        except KeyError :
            continue #Skip if song not found

    # Adding the songs to the playlist
    add_playlist = sp.playlist_add_items(playlist_id=my_playlist["id"], items=ids)



