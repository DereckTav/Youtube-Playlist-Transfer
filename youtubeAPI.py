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

        playlists_response = request.execute()

        # Extract playlist IDs
        # give this to other class
        playlist_title = [item["snippet"]["title"] for item in playlists_response.get("items", [])]
        playlist_title.append('Liked Videos')

        playlist_ids = [item["id"] for item in playlists_response.get("items", [])]
        playlist_ids.append('LL')

    return playlist_title, playlist_ids
        
        
def getPlaylistItems(id):      
    credential = credential = getCredentials()

    with build('youtube', 'v3', credentials=credential) as youtube:
        playlist = youtube.playlistItems()
        request = playlist.list(part='snippet', playlistId=id)

        playlists_response = request.execute()

    return json.dumps(playlists_response, sort_keys=True, indent=4)


if __name__ == "__main__":
    getPlaylistItems('LL')