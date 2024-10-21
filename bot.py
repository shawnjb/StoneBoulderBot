import discord
import os
from discord.ext import commands
from dotenv import load_dotenv
from transformers import pipeline

load_dotenv()
if not os.path.exists('.env'):
    with open('.env', 'w') as f:
        f.write('TOKEN=YOUR_TOKEN_HERE\n')
    print(".env file created with required entries. Please fill in your token.")
    exit()

TOKEN = os.getenv('TOKEN')

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)
tree = discord.app_commands.CommandTree(client)

generator = pipeline('text-generation', model='gpt2')

@tree.command(name='prompt', description='Generate a response from the AI with the given prompt.')
async def prompt(interaction: discord.Interaction, message: str):
    async with interaction.channel.typing():
        ai_response = generator(message, max_length=50, num_return_sequences=1)[0]['generated_text']
    await interaction.response.send_message(ai_response)

@client.event
async def on_ready():
    print(f'Logged in as {client.user.name}')
    await tree.sync()

client.run(TOKEN)
