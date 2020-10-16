import discord
from random import randint

from dotenv import load_dotenv
load_dotenv()

import os
TOKEN = os.getenv("PING_TOKEN")

client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

async def handle_bot_game(message):
    computerMove = randint(0,2)

    userMove = message.content[5:]

    if (userMove =='rock' or userMove == 'paper' or userMove == 'scissors'):
        if computerMove == 0: 
            if userMove == 'rock':
                await message.channel.send("you both played rock! Tie")
            elif userMove == 'paper':
                await message.channel.send("user used paper computer used rock. Player wins!")
            else:
                await message.channel.send("user used scissors, computer used rock. Computer wins!")    

        elif computerMove == 1: 
            if userMove == 'paper':
                await message.channel.send("you both played paper! Tie")
            elif userMove == 'scissors':
                await message.channel.send("user used scissors, computer used paper. Player wins!")
            else:
                await message.channel.send("user used rock, computer used paper. Computer wins!") 

        elif computerMove == 2:
            if userMove == 'scisscors':
                await message.channel.send("you both played scissors! Tie")
            elif userMove == 'rock':
                await message.channel.send("user used rock computer used scissors. Player wins!")
            else:
                await message.channel.send("user used paper, computer used scissors. Computer wins!")

    else:
        await message.channel.send("Please use rock, paper or scissors")

messages = {}

class Game():
    def __init__(self, user_a, user_b, output_channel):
        self.user_a = user_a
        self.user_b = user_b
        self.output_channel = output_channel

        self.user_a_choice = None
        self.user_b_choice = None
    
    async def start(self):
        await self.send_user_rps_direct_message(self.user_a, self.user_b)
        await self.send_user_rps_direct_message(self.user_b, self.user_a)
    
    async def send_user_rps_direct_message(self, user, other_user):
        message = await user.send(f"You VS {other_user.name}: Rock, paper, scissors? (game #{id(self)})")
        await message.add_reaction("🗿")
        await message.add_reaction("🧻")
        await message.add_reaction("✂️")

        messages[message.id] = (self, user)
    
    async def handle_reaction(self, message, user, reaction):
        if reaction.emoji == "🗿":
            choice = "rock"
        elif reaction.emoji == "🧻":
            choice = "paper"
        elif reaction.emoji == "✂️":
            choice = "scissors"
        else:
            print("TODO handle invalid emoji")
        
        if user == self.user_a:
            self.user_a_choice = choice
        else:
            self.user_b_choice = choice
        
        if choice is not None:
            del messages[message.id]

        await self.check_if_game_is_done()

    async def check_if_game_is_done(self):
        if self.user_a_choice is not None and self.user_b_choice is not None:
            await self.end_game()

    async def end_game(self):
        winner = None
    
        if self.user_a_choice == "rock": 
            if self.user_b_choice == 'paper':
                winner = self.user_b
            elif self.user_b_choice== "scissors":
                winner = self.user_a 

        elif self.user_a_choice == "paper": 
            if self.user_b_choice == "scisssors":
                winner = self.user_b
            elif self.user_b_choice == "rock":
                winner = self.user_a

        else:
            if self.user_b_choice == 'rock':
                winner = self.user_b
            elif self.user_b_choice=='paper':
                winner = self.user_a

        if winner:
            postfix = f"{winner} wins!"
        else:
            postfix = "tie!"

        await self.output_channel.send(f"Game #{id(self)} results: {self.user_a.name} {self.user_a_choice} VS {self.user_b.name} {self.user_b_choice}, {postfix}")

async def handle_user_game(message):
    new_game = Game(message.author, message.mentions[0], message.channel)
    await new_game.start()
    await message.channel.send(f"New game #{id(new_game)} created, check your direct messages!")

@client.event
async def on_reaction_add(reaction, user):
    if user == client.user:
        return

    if reaction.message.id in messages:
        game, user = messages[reaction.message.id]
        await game.handle_reaction(reaction.message, user, reaction)

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$rps '):
        amount_of_mentions = len(message.mentions)

        if amount_of_mentions == 0:
            await handle_bot_game(message)
        elif amount_of_mentions == 1:
            await handle_user_game(message)
        else:
            await message.channel.send("Too many mentions in message, expected either one or none")

client.run(TOKEN)