from p2pd import *
import asyncio
import random
import sys
import authorization
import youtubeAPI
import JsonChunkProcessor

#TODO for watch later parse youtube website watchlater
            #How IN THE WORLD DO I ACCESS SOMEONE ELSE WATCH LATER
            #selenium

recieved_valid_json_chunk = False

async def create_foreign_playlist(msg, client_tup, pipe):
    global recieved_valid_json_chunk
    chunk = msg.decode('utf-8')
    #prints the p2p message I want
    if "P2P_CON_ID_EQ" in chunk:
        print()
        print(chunk)
        print()

    if "{" in chunk and not recieved_valid_json_chunk:
        print("passed {")
        recieved_valid_json_chunk = True

    if recieved_valid_json_chunk:
        print("passed chunker")
        JsonChunkProcessor.processJsonChunk(chunk)

    if JsonChunkProcessor.RECIEVED:
        print("LETS GO")

async def main():
    node = None
    choice = None

    while True:
        if not os.path.exists('access_token.json') or os.stat('access_token.json').st_size == 0:
            print("No valid saved access token found. Starting OAuth...")
            print()

        # runs over here because I still want to refresh access token if it is expired
        authorization.authorize_user()
        print("(1) retrieve playlist from another user.\n(2) Send playlist to another user.")
        print("(3) Exit program.\n(4) delete api Key")
        
        choice = input("Select menu option: ")
        if choice not in ("1", "2", "3", "4", "exit"):
            print()
            continue
        
        if choice == "exit":
            choice = "3"

        if choice == "1" or choice == "2":
            if not node:
                print("Starting Program ...")
                node = P2PNode()
        
            if choice == "1":
                node.add_msg_cb(create_foreign_playlist)
                await node.start(out=True) # this prints the process of node starting
                try:

                    print("Setting up connection")
                    
                    try:
                        part1 = random.randint(100, 999)
                        part2 = random.randint(100, 999)
                        part3 = random.randint(100, 999)

                        connection_key = await node.nickname(f"{part1}-{part2}-{part3}")
                        print(fstr("Connection Key = \033[1;32m{0}\033[0m", (connection_key,)))
                        print()
                    except:
                        print("Server error")

                    print("Waiting For Playlist")
                    while not JsonChunkProcessor.RECIEVED:
                        await asyncio.sleep(1)
                    
                    #TODO allow accept and deny of playlist
                    print(JsonChunkProcessor.getJson())
                    # input("Would you like to accept playlist: " + JsonChunkProcessor.getJson())

                    choice = "3"
                except KeyboardInterrupt:
                    await node.close()
                    sys.exit()

            if choice == "2":
                await node.start(out=True) # this prints the process of node starting
                option = ""

                while True:
                    if option == "":
                        print()
                        print("Enter Connection Key or type menu to return to menu or exit to quit")
                        option = input("> ")

                    if not re.match(r'\d{3}-\d{3}-\d{3}\.peer', option) and option not in ("menu", "exit"):
                        continue

                    if option == "exit":
                        choice = "3"
                        break

                    if option == "menu":
                        await node.close()
                        node = None
                        choice = ""
                        break
                    
                    connection_key = option
                    pipe = await node.connect(connection_key)
                    
                    if pipe is None:
                        print()
                        print("Connection failed.")
                        option = ""
                        continue
                    
                    else:
                        print()
                        print("SUCCESSFLY CONNECTED")
                        print()
                        print("Y (to send)")
                        print("N (return to menu)")
                        print("exit (to quit).")
                        while 1: 
                            option = input("TRANSFER: ")
                            if option == "exit":
                                option = "exit"
                                await pipe.close()
                                break
                            if option == "N":
                                option = "menu"
                                await pipe.close()
                                break
                            if option == "Y":
                                try:
                                    playlist_titles, playlist_ids = youtubeAPI.getListOfPlaylist()

                                    print("Your PlayLists: ")
                                    for idx, title in enumerate(playlist_titles, start=1):
                                        print(f"({idx}) {title} ")
                                    
                                    playlist = input("choose a valid playlist number: ")
                                    while playlist:
                                        try:
                                            playlist = int(playlist)
                                            break
                                        except:
                                            print('Please choose a valid playlist number')
                                            playlist = input("Choose a playlist: ")

                                    #checks for canceling playlist can be added here

                                    id = playlist_ids[playlist]

                                    playlist_json = youtubeAPI.getPlaylistItems(id)

                                    binary_data = playlist_json.encode('utf-8')

                                    await pipe.send(binary_data)
                                    
                                    option = "exit"
                                    await pipe.close()
                                    break
                                except KeyboardInterrupt:
                                    await pipe.close()
                                    await node.close()
                                    sys.exit()
        
        if choice == "3":
            print("Stopping program...")
            if node:
                await node.close()
            print("Successfully exiting program. Please Wait.")
            sys.exit()

        if choice == "4":
            print("deleting token...")
            authorization.delete_token()
            print("token deleted")
            sys.exit()
            

if __name__ == "__main__":
    asyncio.run(main())