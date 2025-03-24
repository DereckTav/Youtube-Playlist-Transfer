from p2pd import *
import asyncio
import random
import sys
import authorization
import youtubeAPI

 #TODO for watch later parse youtube website watchlater
            #How IN THE WORLD DO I ACCESS SOMEONE ELSE WATCH LATER
            #selenium

async def send_playlist_information(msg, client_tup, pipe):
    print(to_s(msg))

async def create_foreign_playlist(msg, client_tup, pipe):
    json = msg.decode('utf-8')
    print(json)
    #TODO YOUTUBE API
    # createPlaylist(playlist_json)


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
                print("Staring...")
                # maybe can replace fstr with f string
                # may or maynot need this;
                if_names = await list_interfaces()
                print(".")
                print("..")
                ifs = await load_interfaces(if_names)
                print("...")
                node = P2PNode(ifs=ifs)
        
            if choice == "1":
                node.add_msg_cb(create_foreign_playlist)
                await node.start(out=True) # this prints the process of node starting

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

                # waiting need to implement
                # set variable as turn off signal
                # transfer to menu
                while True:
                    await asyncio.sleep(1)
                    #TODO YOUTUBE API

            while choice == "2":
                node.add_msg_cb(send_playlist_information)
                await node.start(out=True) # this prints the process of node starting

                option = ""

                if option == "":
                    print()
                    print("Enter Connection Key or type menu to return to menu or exit to quit")
                    option = input("> ")

                if not re.match(r'[1-9]{3}-[1-9]{3}-[1-9]{3}', option) and option not in ("menu", "exit"):
                    continue

                if option == "exit":
                    choice = "3"
                    break

                if option == "menu":
                    choice = ""
                    break

                connection_key = option
                pipe = await node.connect(connection_key)
                print()
                print("If you entered the wrong connection key, spam crtl + c, and start over. (Or wait)")
                
                if pipe is None:
                    print()
                    print("Connection failed.")
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
                        if option in ("exit"):
                            option = "3"
                            pipe.close()
                            break
                        if option in ("N"):
                            option = "menu"
                            await pipe.close()
                            break
                        if option in ("Y"):
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

                            id = playlist_ids(playlist)

                            # add if statments, for youtube playlist watchlater
                            playlist_json = youtubeAPI.getPlaylistItems(id)
                            binary_data = playlist_json.encode('utf-8')
                
                            await pipe.send(binary_data + b"\n")
                            buf = await pipe.recv(timeout=3)
                            if buf:
                                print("SENT: ", True)
                            else:
                                print("SENT: ", False)
    
        if choice == "3":
            print("Stopping program...")
            if node:
                print(".")
                print("..")
                await node.close()
            print("Successfully exited program.")
            sys.exit()

        if choice == "4":
            print("deleting token...")
            authorization.delete_token()
            print("token deleted...")
            sys.exit()
            

if __name__ == "__main__":
    asyncio.run(main())