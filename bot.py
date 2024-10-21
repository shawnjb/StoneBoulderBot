import discord
import os
from discord.ext import commands
from dotenv import load_dotenv
from transformers import pipeline

load_dotenv()
TOKEN = os.getenv('TOKEN')

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

generator = pipeline('text-generation', model='gpt2')
message_counter = 0

def generate_ai_response(prompt):
    result = generator(prompt, max_length=50, num_return_sequences=1)
    return result[0]['generated_text']

@bot.event
async def on_message(message):
    global message_counter
    if message.author == bot.user:
        return
    
    message_counter += 1

    if message_counter % 5 == 0:
        user_input = message.content
        ai_response = generate_ai_response(user_input)
        await message.channel.send(ai_response)
    
    await bot.process_commands(message)

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game(name=f'In {len(bot.guilds)} servers'))
    print(f'Logged in as {bot.user.name}')

bot.run(TOKEN)
