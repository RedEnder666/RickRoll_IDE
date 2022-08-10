import time, sys
from pypresence import Presence


def get_discord_rpc_filename():
    with open(f"current_file.txt") as f:
        text = f.read()
    
    return text


def set_discord_rpc_filename(text):
    with open(f"current_file.txt", 'w') as f:
        f.write(text)


def update_presence():
    try:
        start_time = time.time()
        client_id = "960035622272262184"
        rpc = Presence(client_id)
        rpc.connect()

        while True:
            global discord_rpc_filename
            rpc.update(
                state=f"Editing: {get_discord_rpc_filename()}", 
                details="Coding using the Rickroll IDE",
                large_image="rickroll_ide", 
                large_text="Rick Roll Lang", 
                buttons=[
                    {
                        "label":"Totally not a rick roll", 
                        "url":"https://www.youtube.com/watch?v=dQw4w9WgXcQ"
                    }, 
                    {
                        "label":"Download IDE", 
                        "url":"https://github.com/RedEnder666/RickRoll_IDE/archive/refs/heads/main.zip"
                    }
                ], 
                start=start_time)
                
            time.sleep(15)
    except:
        pass
