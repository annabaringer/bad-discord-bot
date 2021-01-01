import discord
import pandas as pd
import sys
import configparser

# define variabls to refer to bot and servers (guilds)
client = discord.Client()
guild = discord.Guild

# parse requirements cfg
settings = configparser.ConfigParser()
settings.read('replacements.cfg')
BOT_TOKEN = settings.get('inputs','BOT_TOKEN')

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

# called when bot recieves a message
@client.event
async def on_message(message):
    if message.author == client.user: # do not include bot messages
        return

    elif message.content.startswith('~'): # if it starts with ~, it's a command for bot
        cmd = message.content.split()[0].replace("~","")

        if len(message.content.split()) > 1:
            parameters = message.content.split()[1:]
            
        # commands for bot below this

        # make dataframe to steal
        if cmd == 'steal':
            data = pd.DataFrame(columns=['content', 'time', 'author'])

            # ask for the number of messages to be scraped by the bot command
            if (len(message.content.split()) > 1 and len(message.channel_mentions) == 0) or len(message.content.split()) > 2:
                for parameter in parameters:
                    if parameter == "help":
                        answer = discord.Embed(title="command help",
                                               description="""`~steal <number_of_messages>`\n\n`<number_of_messages>` : ** number of messages you wish to steal**""",
                                               colour=0x1a7794) 
                        await message.channel.send(embed=answer)
                        return
                    elif parameter[0] != "<": # channels are enveloped by "<>" as strings
                        limit = int(parameter)
            else:
                limit = 100
            
            answer = discord.Embed(title="creating dataframe",
                                   description="waiting?",
                                   colour=0x1a7794) 

            await message.channel.send(embed=answer)

            def is_command (msg): # checking if the message is a command call
                if len(msg.content) == 0:
                    return False
                elif msg.content.split()[0] == '~steal':
                    return True
                else:
                    return False

            async for msg in message.channel.history(limit=limit): # look at last x messages 
                if msg.author != client.user:
                    if not is_command(msg):
                        data = data.append({'content': msg.content,
                                    'time': msg.created_at,
                                    'author': msg.author.name}, ignore_index=True)
                if len(data) == limit:
                    break
            print(data)
            data.to_csv("data.csv", index=False)

            await message.channel.send('done!')

        # stop the program
        if cmd == 'killBot':
            sys.exit()

client.run(BOT_TOKEN)