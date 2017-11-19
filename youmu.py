#!/usr/bin/env python

import discord
from discord.ext import commands
import asyncio
from config.keyconfig import KEY
from config.japdicconfig import JAPDIC
from config.sokuhostconfig import hosts

hostlist = {}

youmu = discord.ext.commands.Bot(command_prefix="!?",
                                 description="Discord bot to deal with touhou stuff",
                                 pm_help=True)


@youmu.event
async def on_ready():
    print("Logged in as")
    print(youmu.user.name)
    print(youmu.user.id)
    print("------")


@youmu.command()
async def addhost(ctx, *args):
    if args:
        ip = args[0]
        hamachi = False
        room = ""
        if len(args) == 3:
            if args[1] == "hamachi":
                hamachi = True
                room = args[2]

        if await valid_ip(ip):
            hosts[ctx.author.id] = {"IP": ip, "hamachi": hamachi, "roomID": room}
            f = open("./config/sokuhostconfig.py", "w")
            f.write("hosts = " + repr(hosts))
            f.close()
            await ctx.channel.send("Host IP has been added")
            if not hamachi:
                await ctx.channel.send("Add `hamachi [hamachi room name]` to indicate you are using hamachi")
        else:
            await ctx.channel.send("Invalid IP format")
            await ctx.channel.send("Example: {}".format(hosts["example"]["IP"]))


async def valid_ip(ip):
    if ip.count(":") != 1 or ip.count(".") != 3:
        return False
    return True


@youmu.command()
async def host(ctx):
    global hostlist
    if ctx.author.id in hosts:
        hostlist[ctx.author] = await ctx.channel.send("{} hosting at {}".format(ctx.author.name, hosts[ctx.author.id]["IP"]))
    else:
        await ctx.channel.send("Unknown host!")
        await ctx.channel.send("Please record your IP using !?addhost first")


@youmu.command()
async def endhost(ctx):
    global hostlist
    if ctx.author in hostlist:
        await hostlist[ctx.author].edit(content="{} has ended hosting".format(ctx.author.name))
        hostlist.pop(ctx.author)


youmu.run(KEY)
