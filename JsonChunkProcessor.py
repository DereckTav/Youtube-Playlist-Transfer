import json

RECIEVED = False
json_object = ""

def processJsonChunk(chunk):
    json_object.join(chunk)

    try:
        print(chunk)
        json.loads(json_object)
        global RECIEVED
        RECIEVED = True
        # youtubeAPI.createPlaylist(playlist_json)

    except json.JSONDecodeError:
        pass

def getJson():
    return json_object
# if making a loop to send playlist add function to clear json_object