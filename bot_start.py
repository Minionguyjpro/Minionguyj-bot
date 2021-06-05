import discord
from discord.ext import commands
from sql_work import MongoLite

mn = MongoLite("server.db")

TOKEN = 'ODUwMDg3ODg0ODM1OTEzNzk5.YLkoCQ.81BO0zyLkQ5cqf01xDafARyF7p8'
bot = commands.Bot(command_prefix='=', activity=discord.Activity(type=discord.ActivityType.watching, name="out for ="))

@bot.event
async def on_message(message):
    await bot.process_commands(message)
    if not message.author == bot.user:
        if await mn.vlookup("CHANNELS_SETUP", "suggestion_chnl", "guildid", message.guild.id) == message.channel.id:
            try:
                await message.delete()
            except discord.errors.NotFound:
                pass


@bot.command(name="setup-suggestion-channel", help="Sets up a suggestion channel")
@commands.has_permissions(manage_messages=True)
async def setup_suggestion_channel(ctx, channel: discord.TextChannel):
    await mn.update_suggestion_channel(ctx.guild.id, channel.id)
    await ctx.send(channel.mention + " was set as a suggestions channel!")

@bot.command(name="consider", help="Considers a suggestion")
@commands.has_permissions(manage_messages=True)
async def consider(ctx, mid, *note):
    if await mn.vlookup("CHANNELS_SETUP", "suggestion_chnl", "guildid", ctx.guild.id) == ctx.channel.id:
        msg = await ctx.channel.fetch_message(mid)
        embed = msg.embeds[0]
        embed_dict = embed.to_dict()

        for field in embed_dict["fields"]:
            if field["name"] == "Pending Approval..":
                field["name"] = "Stand"
                field["value"] = "Considered by " + ctx.message.author.name

        embed = discord.Embed.from_dict(embed_dict)
        if len(note) > 0:
            embed.add_field(name="Reason", value=" ".join(note), inline=False)
        await msg.edit(embed=embed)
        ctx.message.delete()
    else:
        ctx.send("This is not a suggestions channel!")



@bot.command(name="approve", help="Approves a suggestion")
@commands.has_permissions(manage_messages=True)
async def approve(ctx, mid, *note):
    if await mn.vlookup("CHANNELS_SETUP", "suggestion_chnl", "guildid", ctx.guild.id) == ctx.channel.id:
        msg = await ctx.channel.fetch_message(mid)
        embed = msg.embeds[0]
        embed_dict = embed.to_dict()

        for field in embed_dict["fields"]:
            if field["name"] == "Pending Approval..":
                field["name"] = "Stand"
                field["value"] = "Approved By " + ctx.message.author.name +  " ✅"

        embed = discord.Embed.from_dict(embed_dict)
        if len(note) > 0:
            embed.add_field(name="Reason", value=" ".join(note), inline=False)
        await msg.edit(embed=embed)
        ctx.message.delete()
    else:
        ctx.send("This is not a suggestions channel!")


@bot.command(name="deny", help="Denies a suggestion")
@commands.has_permissions(manage_messages=True)
async def deny(ctx, mid, *note):
    if await mn.vlookup("CHANNELS_SETUP", "suggestion_chnl", "guildid", ctx.guild.id) == ctx.channel.id:
        msg = await ctx.channel.fetch_message(mid)
        embed = msg.embeds[0]
        embed_dict = embed.to_dict()

        for field in embed_dict["fields"]:
            if field["name"] == "Pending Approval..":
                field["name"] = "Stand"
                field["value"] = "Denied by " + ctx.message.author.name + " ❌"

        embed = discord.Embed.from_dict(embed_dict)
        if len(note) > 0:
            embed.add_field(name="Reason", value=" ".join(note), inline=False)
        await msg.edit(embed=embed)
        ctx.message.delete()
    else:
        ctx.send("This is not a suggestions channel!")


@bot.command(name="suggest", help="Allows users to suggest")
async def suggest(ctx, *suggestion):
    if await mn.vlookup("CHANNELS_SETUP", "suggestion_chnl", "guildid", ctx.guild.id) == ctx.channel.id:
        await ctx.message.delete()
        # suggest
        embed = discord.Embed(title=" ", description=" ", color=0x7CFC00)
        embed.set_author(name=ctx.message.author.name + "#" + ctx.message.author.discriminator, icon_url=ctx.message.author.avatar_url)
        embed.add_field(name="Suggestion 💡", value=" ".join(suggestion), inline=False)
        embed.add_field(name="Pending Approval..", value="⌛")

        embed.set_footer(text="Powered by 1bhm#6827")
        await ctx.send(embed=embed)
    else:
        await ctx.send("This is not a suggestions channel!")




bot.run(TOKEN)