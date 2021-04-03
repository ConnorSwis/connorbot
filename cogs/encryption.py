import os

import discord
from connor_bot import PREFIX, COG_FOLDER
from cryptography.fernet import Fernet
from discord.ext import commands


KEY_FOLDER = f'{COG_FOLDER}/keys/'

class Encryption(commands.Cog):
    def __init__(self, client):
        self.client = client

    def find(self, name, path):
        for root, dirs, files in os.walk(path):
            if name in files:
                return True


    def new_key(self, name):
        key = Fernet.generate_key()
        with open(f'{KEY_FOLDER}{name}.key', 'wb') as f:
            f.write(key)


    def read_key(self, name):
        with open(f'{KEY_FOLDER}{name}.key', 'rb') as f:
            key = f.read()
        return key


    def encrypt_string(self, name, *string):
        if not self.find(f'{name}.key', KEY_FOLDER):
            self.new_key(name)
        key = self.read_key(name)
        strings = []
        for i in range(len(string)):
            try:
                strings.append(string[i].decode())
            except:
                strings.append(string[i])
        message = ' '.join(strings)
        encoded = message.encode()

        f = Fernet(key)
        encrypted = f.encrypt(encoded)
        return encrypted


    def decrypt_string(self, name, string):
        if not self.find(f'{name}.key', KEY_FOLDER):
            return
        key = self.read_key(name)
        f = Fernet(key)
        decrypted_bytes = f.decrypt(string)
        decrypted = decrypted_bytes.decode()
        return decrypted


    @commands.command(brief="Encrypts a message with your personal key.", usage=f"{PREFIX}encrypt message")
    async def encrypt(self, ctx, *, message):
        encrypted = self.encrypt_string(str(ctx.author.id), message)
        embed = discord.Embed(title="Encryption")
        embed.add_field(name="Before:", value='```'+message+'```')
        embed.add_field(name="After:", value='```'+encrypted.decode()+'```')
        if type(ctx.channel) is not discord.channel.DMChannel:
            await ctx.channel.purge(limit=1)
        await ctx.author.send(embed=embed)


    @commands.command(brief="Decrypts message encoded with personal key.", usage=f"{PREFIX}decrypt message")
    async def decrypt(self, ctx, *, message):
        decrypted = self.decrypt_string(str(ctx.author.id), message.encode())
        if not decrypted:
            await ctx.send("Couldn't decrypt message.")
        embed = discord.Embed(title="Decryption")
        embed.add_field(name="Before:", value='```'+message+'```')
        embed.add_field(name="After:", value='```'+decrypted+'```')
        if type(ctx.channel) is not discord.channel.DMChannel:
            await ctx.channel.purge(limit=1)
        await ctx.author.send(embed=embed)


def setup(client):
    client.add_cog(Encryption(client))
