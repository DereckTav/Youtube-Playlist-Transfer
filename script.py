import math
from p2pd import *
import asyncio
import random
import sys
import authorization
import youtubeAPI

 #TODO for watch later parse youtube website watchlater
            #How IN THE WORLD DO I ACCESS SOMEONE ELSE WATCH LATER
            #selenium

#TODO WHY IS IT NOT SENDING ??? !!!! : <<< (((
#TODO can you edit a constant stat DONE in main from other classes that
    # import it 

async def send_playlist_information(msg, client_tup, pipe):
    print()
    print("HI IM 2 : I recived something from the server")
    print(msg)

async def create_foreign_playlist(msg, client_tup, pipe):
    
    # if not os.path.exists('Playlist Hashes.txt'):

    # playlist_json = msg.decode('utf-8')
    # print(playlist_json)
    # if decoded an not json string know to do nothing
    try:
        playlist_json = msg.decode('utf-8')
        print(playlist_json)
        json.loads(playlist_json)  # Try to parse the string as JSON
        print("HI IM 1 : I recived something from the client")
        print(playlist_json)
        reply = "PlayList sent succesfully, shutting down now ".join(client_tup)
        # youtubeAPI.createPlaylist(playlist_json)
        # await pipe.send(reply.encode('utf-8'))
    except json.JSONDecodeError:
        reply = b"False"
        # await pipe.send(reply)  # Not a valid JSON string

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

                    # waiting need to implement
                    # set variable as turn off signal
                    # Exit
                    print("Waiting")
                    while not youtubeAPI.isDone():
                        await asyncio.sleep(1)

                    choice = "3"
                except KeyboardInterrupt:
                    await node.close()
                    sys.exit()

            if choice == "2":
                node.add_msg_cb(send_playlist_information)
                await node.start(out=True) # this prints the process of node starting
                await node.nickname(node.node_id)

            while choice == "2":
                option = ""
            
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

                                #TODO fix binary data
                                # says Trying to write to closed socket

                                '''
                                Split the files into blocks let's say of 100KB each. 
                                Then calculate a SHA hash (or some other hashing algorithm) on each of the blocks. 
                                so if the file is 905KB, you would have 10 such hashes calculated.

                                The server would contain a hash definition file for each file that it serves. 
                                This hash definition file would contain a list of all of the blocks of the file, along with the hash. 
                                So if the server is serving our 905KB file called test.exe. 
                                Then we would have another file called test.exe.hashes which contains a listing of the 10 hashes of the file.

                                The client would download the hash definition file, and ensure that it has all of the blocks. 
                                The client can request each block individually and after it's downloaded, it can calculate the hash on its end again to ensure there is no corruption.

                                You don't need to physically split the file, splitting a file is just reading the part of it that you are interested in.   
                                The first block of the file is from byte range 0 to 102399, the next block is from 102400 to 204800, and so on. 
                                So just open the file, seek to that position, read the data, and close the file.
                                '''

                                playlist_json = youtubeAPI.getPlaylistItems(id)
                                # size_kb = len(playlist_json) / 1024

                                # if size_kb <= 100:
                                    # Add hashing (example, you can customize this part)
                                binary_data = playlist_json.encode('utf-8')
                                # h = "Hello"
                                # await pipe.send(h.encode('utf-8'))
                                await pipe.send(binary_data)
                                
                                # Receive response and check if it's successful
                                buf = await pipe.recv(timeout=3)
                                print(buf)
                                        
                                # else:
                                #     playlist_Hashchunks = []
                                #     chunk_size = 100 * 1024  # 100KB in bytes
                                #     iterations = math.ceil(size_kb / 100)

                                #     # Generate chunk slices and send them
                                #     for i in range(iterations):
                                #         start_idx = i * chunk_size
                                #         end_idx = min((i + 1) * chunk_size, len(playlist_json))

                                #         chunk = playlist_json[start_idx:end_idx]
                                #         received_hash = hashlib.sha256(chunk).hexdigest()
                                #         playlist_Hashchunks.append(received_hash)

                                #     byte_data = joined_hashes.encode('utf-8')  # Encode the string into bytes (UTF-8 encoding)
                                #     print("Byte Data:", byte_data)

                                #     # Example of sending this byte data over a pipe (simulated with await statements)
                                #     # Assuming you have a `pipe` object available for communication

                                #     await pipe.send(b"ECHO " + byte_data + b"\n")
                                #     # return number of item hashes
                                #     # get those

                                #     playlist_Hashchunks_string = ''.join(playlist_Hashchunks)
                                #     binary_string = ''.join(format(ord(char), '08b') for char in playlist_Hashchunks_string)
                                print(option)
                                print("here")
                                option = "exit"
                                break
                            except KeyboardInterrupt:
                                await pipe.close()
                                await node.close()
                                sys.exit()
    
        if choice == "3":
            print("Stopping program...")
            if node:
                print(".")
                print("..")
                await node.close()
            print("Successfully exiting program. Please Wait.")
            sys.exit()

        if choice == "4":
            print("deleting token...")
            authorization.delete_token()
            print("token deleted...")
            sys.exit()
            

if __name__ == "__main__":
    asyncio.run(main())