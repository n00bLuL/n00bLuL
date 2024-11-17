import nextcord
import asyncio
import tkinter as tk
from tkinter import simpledialog, scrolledtext

# Hardcoded bot credentials and user information
BOT_TOKEN = 'MTMwNzgwNzI4NTc3MDQ1MzA1Mw.G0SOJH.9xmhqflWq6CQ1n8rOxyLbLcTXXYA95PtRZCKV0'
GUILD_ID = 1307816121017044993  # Replace with your Guild ID
CHANNEL_ID = 1307816121537400832  # Replace with your Channel ID
USER_NAME = "Ham"  # Replace with your desired username to show up for the bot

# Initialize the client
client = nextcord.Client()

# Global variable to store the channel
channel = None

# Function to send messages to the channel
async def send_message(message):
    if channel:
        await channel.send(f"{USER_NAME} said - {message}")
    else:
        print("Channel is not defined.")

# Function to handle receiving messages from the Discord channel
async def receive_messages():
    global channel
    while True:
        # Wait for new messages from the Discord channel
        def check_message(msg):
            return msg.channel == channel and msg.author.name != USER_NAME
        
        # Wait for new message event asynchronously
        msg = await client.wait_for('message', check=check_message)
        add_message_to_gui(f"{msg.author.name} said - {msg.content}")

# Event handler for when the bot is ready
@client.event
async def on_ready():
    global channel
    print(f"Logged in as {client.user}")
    
    # Get the channel object from the guild
    guild = client.get_guild(GUILD_ID)
    if guild is None:
        print(f"Guild {GUILD_ID} not found. Exiting.")
        return

    channel = guild.get_channel(CHANNEL_ID)
    if channel is None:
        print(f"Channel {CHANNEL_ID} not found. Exiting.")
        return

    print(f"Successfully connected to channel: {channel.name}")
    
    # Start the receiving loop to listen for messages
    asyncio.create_task(receive_messages())

# GUI functions
def send_message_from_gui():
    message = message_entry.get()
    if message:
        message_entry.delete(0, tk.END)
        asyncio.run_coroutine_threadsafe(send_message(message), client.loop)
        add_message_to_gui(f"You said - {message}")

def add_message_to_gui(message):
    chat_log.config(state=tk.NORMAL)
    chat_log.insert(tk.END, message + '\n')
    chat_log.config(state=tk.DISABLED)
    chat_log.yview(tk.END)

# Set up the GUI
root = tk.Tk()
root.title("Discord Chat GUI")

chat_log = scrolledtext.ScrolledText(root, state=tk.DISABLED, wrap=tk.WORD, width=50, height=20)
chat_log.pack(padx=10, pady=10)

message_entry = tk.Entry(root, width=40)
message_entry.pack(side=tk.LEFT, padx=(10, 0), pady=(0, 10))

send_button = tk.Button(root, text="Send", command=send_message_from_gui)
send_button.pack(side=tk.LEFT, padx=(5, 10), pady=(0, 10))

# Start the bot and GUI
def start_bot():
    loop = asyncio.get_event_loop()
    loop.create_task(client.start(BOT_TOKEN))
    loop.run_forever()

# Run the bot in a separate thread
import threading
threading.Thread(target=start_bot, daemon=True).start()

# Start the Tkinter main loop
root.mainloop()
