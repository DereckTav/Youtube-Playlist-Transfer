import json

RECIEVED = False
json_object = ""

def processJsonChunk(chunk):
    global json_object
    json_object.join(chunk)

    try:
        if "}" == chunk:
            print(json_object)
            try:
                json.loads(json_object)
            except Exception as e:
                print(e)

        json.loads(json_object)
        global RECIEVED
        RECIEVED = True
        # youtubeAPI.createPlaylist(playlist_json)

    except json.JSONDecodeError:
        pass

def getJson():
    return json_object
# if making a loop to send playlist add function to clear json_object