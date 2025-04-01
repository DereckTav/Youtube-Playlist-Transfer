import json

RECIEVED = False
json_object = ""

def processJsonChunk(chunk):
    json_object.join(chunk)

    try:
        json.loads(json_object)
        global RECIEVED
        RECIEVED = True
        # youtubeAPI.createPlaylist(playlist_json)

    except json.JSONDecodeError:
        pass


# if making a loop to send playlist add function to clear json_object