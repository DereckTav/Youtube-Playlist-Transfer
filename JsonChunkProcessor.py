import json

RECIEVED = False
json_chunks = []

def processJsonChunk(chunk):
    global json_chunks
    json_chunks.append(chunk)

    try:
        json_object = "".join(json_chunks)
        json.loads(json_object)
        global RECIEVED
        RECIEVED = True
        # youtubeAPI.createPlaylist(playlist_json)

    except json.JSONDecodeError:
        pass

def getJson():
    return "".join(json_chunks)
# if making a loop to send playlist add function to clear json_object