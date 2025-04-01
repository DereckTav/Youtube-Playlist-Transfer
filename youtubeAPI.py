from googleapiclient.discovery import build
import json
from authorization import getCredentials

def getListOfPlaylist():
    credential = getCredentials()

    with build('youtube', 'v3', credentials=credential) as youtube:
        playlist = youtube.playlists()
        request = playlist.list(part='snippet', mine=True)

                 #TODO for watch later parse youtube website watchlater
                        #How IN THE WORLD DO I ACCESS SOMEONE ELSE WATCH LATER
                        #selenium

        playlist_titles = []
        playlist_ids = []

        while request:
            playlists_response = request.execute()

            playlist_titles.extend([item["snippet"]["title"] for item in playlists_response.get("items", [])])
            playlist_ids.extend([item["id"] for item in playlists_response.get("items", [])])

            token = playlists_response.get('nextPageToken', None)

            if token:
                request = playlist.list(part='snippet', mine=True, pageToken=token)
            else:
                request = None

        playlist_ids.append('LL')
        playlist_titles.append('Liked Videos')

    return playlist_titles, playlist_ids
        
        
def getPlaylistItems(id):      
    credential = getCredentials()

    with build('youtube', 'v3', credentials=credential) as youtube:
        playlist = youtube.playlistItems()
        request = playlist.list(part='snippet', playlistId=id)

        playlists_response = request.execute()

    return json.dumps(playlists_response, indent=4)


def createPlaylist(playlist_json):
    credential = getCredentials()

    with build('youtube', 'v3', credentials=credential) as youtube:
        youtube_playlist = youtube.playlists()

        user = f"({playlist_json["items"]['snippet']['channelTitle']})"

        playlist_json["items"]['snippet']['title'] = f"{playlist_json["items"][0]['snippet']['channelTitle']} {user}"

        # response = youtube_playlist.insert(part="snippet", body=)
        # response.execute()

def makePlaylistJsonWithTitle(title):
    pass

if __name__ == "__main__":
    print(getPlaylistItems('PLFdBzy0C-WaXjLb4TqsNN1Ssv-EIoUNII'))