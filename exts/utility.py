import os
import discord
from discord.ext import commands
from newsapi import NewsApiClient
from time import sleep
import requests
from wikipedia import page
import psutil
from discord.ext.commands import Context
import asyncio
from PIL import Image, ImageDraw
from typing import Tuple
from io import BytesIO
import json


def hex_to_rgb(_hex: str) -> Tuple[int]:
    _hex = _hex.strip('#')

    return tuple(int(_hex[i:i+2], 16) for i in (0, 2, 4))


def get_newsapi_key():
    with open("tokens/newsapi_key.key", "r") as f:
        data = f.read()
        f.close()
    
    return data


def get_weather_api_key():
    with open("tokens/weather_api_token.key", "r") as f:
        data = f.read()
        f.close()
    
    return data


def get_rapid_api_key():
    with open("tokens/rapid_api_key.key", "r") as f:
        data = f.read()
        f.close()
    
    return data



newsapi_key = get_newsapi_key()
weather_key = get_weather_api_key()

newsapi = NewsApiClient(api_key=newsapi_key)


class Utility(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command()
    async def ping(self, ctx: Context):
        '''
        Latency of the bot.
        '''
        chnl = ctx.channel

        await chnl.send(f'Pong! Time took to respond: {round((self.bot.latency * 1000))}ms')


    @commands.command()
    async def news(self, ctx: Context, *, topic=""):
        '''
        Get top 3 headlines from the most trusted news sources!
        '''

        chnl = ctx.channel

        if topic != "":
            top_headlines = newsapi.get_top_headlines(
                q=topic,
                sources="abc-news,associated-press,axios,bleacher-report,bloomberg,breitbart-news,business-insider,buzzfeed,cbs-news,cnn,crypto-coins-news,engadget,entertainment-weekly,espn,fox-news,fox-sports,google-news,hacker-news,ign,mashable,medical-news-today,msnbc,mtv-news,national-geographic,national-review,nbc-news,new-scientist,newsweek,new-york-magazine,next-big-future,nfl-news,nhl-news,politico,polygon,recode,reddit-r-all,reuters,techcrunch,techradar,the-american-conservative,the-hill,the-huffington-post,-weekly,espn,espn-cric-info,fortune,fox-news,fox-sports,google-news,hacker-news,ign,mashable,medical-news-today,msnbc,mtv-news,national-geographic,national-review,nbc-news,new-scientist,newsweek,new-york-magazine,next-big-future,nfl-news,nhl-news,politico,polygon,recode,reddit-r-all,reuters,techcrunch,techradar,the-american-conservative,the-hill,the-huffington-post,the-next-web,the-verge,the-wall-street-journal,the-washington-post,the-washington-times,time,usa-today,vice-news,wired",
                language="en"
            )

            articles = top_headlines['articles']

            embed = discord.Embed(
                title=f"Top headlines I could find on topic: `{topic}`!",
                color=discord.Color.blurple()
            )
            
            for i in range(3):
                embed.add_field(
                    name=f"\n**{i+1}. {articles[i]['title']}**",
                    value=f"{articles[i]['description']}\n\nRead more [here]({articles[i]['url']})\n"
                )
            
            embed.set_footer(text='Powered by NewsAPI.')

            await chnl.send(embed=embed)

        else:
            top_headlines = newsapi.get_top_headlines(
                sources="abc-news,associated-press,axios,bleacher-report,bloomberg,breitbart-news,business-insider,buzzfeed,cbs-news,cnn,crypto-coins-news,engadget,entertainment-weekly,espn,fox-news,fox-sports,google-news,hacker-news,ign,mashable,medical-news-today,msnbc,mtv-news,national-geographic,national-review,nbc-news,new-scientist,newsweek,new-york-magazine,next-big-future,nfl-news,nhl-news,politico,polygon,recode,reddit-r-all,reuters,techcrunch,techradar,the-american-conservative,the-hill,the-huffington-post,-weekly,espn,espn-cric-info,fortune,fox-news,fox-sports,google-news,hacker-news,ign,mashable,medical-news-today,msnbc,mtv-news,national-geographic,national-review,nbc-news,new-scientist,newsweek,new-york-magazine,next-big-future,nfl-news,nhl-news,politico,polygon,recode,reddit-r-all,reuters,techcrunch,techradar,the-american-conservative,the-hill,the-huffington-post,the-next-web,the-verge,the-wall-street-journal,the-washington-post,the-washington-times,time,usa-today,vice-news,wired",
                language="en"
            )

            articles = top_headlines['articles']

            embed = discord.Embed(
                title=f"Top headlines I could find!",
                color=discord.Color.blurple()
            )
            
            for i in range(3):
                embed.add_field(
                    name=f"\n**{i+1}. {articles[i]['title']}**",
                    value=f"{articles[i]['description']}\nRead more [here]({articles[i]['url']})\n"
                )
            
            embed.set_footer(text='Powered by NewsAPI.')

            await chnl.send(embed=embed)


    # Weather command using the OpenWeatherMap API
    @commands.command()
    async def weather(self, ctx: Context, *, city: str = ""):
        '''
        Sends you the latest weather forecast in a city or country.
        '''

        chnl = ctx.channel

        if city != "":
            url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={weather_key}&units=metric'

            response = requests.get(url=url)

            data = response.json()

            # Get the basic weather description from the json
            additional_data = data['weather']
            desc = additional_data[0]['description']

            # The important weather data dictionary from the json file
            weather_data = data['main']

            # All the values of the data in the dictionary
            curr_temp = weather_data['temp']
            feels_like_temp = weather_data['feels_like']
            humidity = weather_data['humidity']
            atmospheric_pressure = weather_data['pressure']

            # Wind speed
            wind_data = data['wind']
            wind_speed = wind_data['speed']

            # Cloudiness
            clouds_data = data['clouds']
            cloudiness = clouds_data['all']

            # Getting the city name from the api so it's a little more clean
            city_data = data['name']

            # Initializing an embed to send a nicer looking composite of all the weather data
            embed = discord.Embed(
                title=f'Weather data for {city_data}',
                colour=discord.Color.from_rgb(43, 223, 255)
            )

            embed.add_field(
                name="**Basic weather**",
                value=f'**Description**: {desc}\n**Current temperature**: {curr_temp}\n**What it feels like**: {feels_like_temp}'
            )

            embed.add_field(
                name="**Wind speed, Humidity, etc**",
                value=f"**Wind speed**: {wind_speed} m/s\n**Humidity**: {humidity}%\n**Cloudiness**: {cloudiness}%\n**Atmospheric Pressure**: {round((atmospheric_pressure / 1013.25), 4)} atm ({atmospheric_pressure} hPa)"
            )

            await chnl.send(embed=embed)

        else:
            await chnl.send(":x: Missing required argument <city>")


    # Command for quickly searching wikipedia about a topic
    @commands.command()
    async def wikisearch(self, ctx: Context, *, arg: str = ""):
        '''
        Search Wikipedia about a certain topic.
        '''

        chnl = ctx.channel

        if arg != "":
            wiki_page = page(arg)

            title = wiki_page.title
            desc = (wiki_page.content[:300] + "...") if len(wiki_page.content) > 303 else wiki_page.content
            url = wiki_page.url

            embed = discord.Embed(
                title=f":book: {title}",
                description=f"{desc}\nRead more about it [here]({url})"
            )
        
        else:
            await chnl.send(":x: Missing required argument `search_query`")


    @commands.command(aliases=['coronavirus', 'cases', 'covid'])
    async def corona(self, ctx: Context, *, country: str):
        '''
        Get information about the latest COVID-19 pandemic situation in a city or country.
        '''

        chnl = ctx.channel

        if country != "":

            try:
                url = "https://covid-193.p.rapidapi.com/statistics"

                querystring = {"country":country}

                headers = {
                    'x-rapidapi-host': "covid-193.p.rapidapi.com",
                    'x-rapidapi-key': get_rapid_api_key()
                }

                response = requests.request("GET", url, headers=headers, params=querystring)

                covid_data = response.json()

                data = covid_data['response']
                main_data = data[0]
                
                cases_data = main_data['cases']
                death_data = main_data['deaths']

                location = f"{main_data['country']}, {main_data['continent']}"
                total_cases = cases_data['total']
                new_cases = cases_data['new']
                healed_cases = cases_data['recovered']
                active_cases = cases_data['active']

                new_deaths = death_data['new']
                total_deaths = death_data['total']

                date = main_data['day']


                embed = discord.Embed(
                    title=f":microbe: **COVID-19 statistics for {location}**",
                    color=discord.Color.blurple()
                )

                embed.add_field(
                    name=":mask: Cases",
                    value=f"Total: `{total_cases}`\nActive: `{active_cases}`\nNew: `{new_cases}`"
                )

                embed.add_field(
                    name=":grin: Recovered",
                    value=f"`{healed_cases}`"
                )

                embed.add_field(
                    name=":skull: Deaths",
                    value=f"Total: `{total_deaths}`\nNew: `{new_deaths}`"
                )

                await chnl.send(embed=embed)

            
            except Exception as e:
                await chnl.send(":x: Sorry, I can't seem to fetch any information about it.")

                print(e)
        
        else:
            chnl.send(f':x: Missing required argument: `city/country`')
    

    @commands.command()
    async def avatar(self, ctx: Context, member: discord.Member = None):
        '''
        Like a person's profile picture? You can now get it with this command!
        '''

        if member:
            embed = discord.Embed(title=f"{member.name}#{member.discriminator}'s avatar")

            embed.set_image(url=member.avatar_url)

            await ctx.channel.send(embed=embed)
        
        else:
            embed = discord.Embed(title=f"{ctx.message.author.name}#{ctx.message.author.discriminator}'s avatar")

            embed.set_image(url=ctx.message.author.avatar_url)

            await ctx.channel.send(embed=embed)


    @commands.command(aliases=['bot', 'botinfo', 'i'])
    async def info(self, ctx: Context):
        '''
        Get information about the bot and its status.
        '''

        embed = discord.Embed(
            title="**Bot Info**",
            description="\n",
            color=discord.Color.blurple()
        )

        embed.add_field(
            name=":desktop: **Memory Usage**",
            value=f"CPU Usage: `{psutil.cpu_percent()}%`\nVRAM Usage: `{psutil.virtual_memory().percent}%`",
            inline=True
        )

        embed.add_field(
            name=":floppy_disk: **Bot's Developer**",
            value="`saint#5622`",
            inline=True
        )

        embed.add_field(
            name=":shield: **Servers**",
            value=f"`{len(self.bot.guilds)}`",
            inline=True
        )

        embed.add_field(
            name=":tools: **Source and Framework**",
            value="Framework: `discord.py`\nSource: [Go to GitHub](https://github.com/erick-dsnk/uncle-dunks-discord-bot)",
            inline=True
        )

        embed.add_field(
            name=":robot: Version",
            value="v1.6.7",
            inline=True
        )

        embed.set_footer(
            text="Developed by saint#5622"
        )

        await ctx.channel.send(embed=embed)
    

    @commands.command()
    async def userinfo(self, ctx: Context, user: discord.Member = None):
        '''
        Get information about a certain user!
        '''
        if user == None:
            user = ctx.author
        
        joined = user.joined_at.strftime('`%d-%m-%Y @ %H:%M:%S`')
        created = user.created_at.strftime('`%d-%m-%Y @ %H:%M:%S`')

        embed = discord.Embed(
            title=f"{user.name}#{user.discriminator}",
            description="\n",
            color=discord.Color.blurple()
        )

        embed.add_field(
            name=":clock: **Basic**",
            value=f"Joined server: {joined}\nCreated account: {created}",
            inline=True
        )

        embed.add_field(
            name=":military_medal: **Top Role:**",
            value=f"{user.top_role.mention}",
            inline=True
        )

        if user.status == discord.Status.online:
            embed.add_field(
                name=":moyai: **User Status**",
                value="(*) :green_circle: Online\n( ) :yellow_circle: Idle\n( ) :red_circle: Do Not Disturb\n( ) :black_circle: Offline/Invisible"
            )
        
        elif user.status == discord.Status.idle:
            embed.add_field(
                name=":moyai: **User Status**",
                value="( ) :green_circle: Online\n(*) :yellow_circle: Idle\n( ) :red_circle: Do Not Disturb\n( ) :black_circle: Offline/Invisible"
            )

        elif user.status == discord.Status.do_not_disturb:
            embed.add_field(
                name=":moyai: **User Status**",
                value="( ) :green_circle: Online\n( ) :yellow_circle: Idle\n(*) :red_circle: Do Not Disturb\n( ) :black_circle: Offline/Invisible"
            )        
        
        elif user.status == discord.Status.offline or user.status == discord.Status.invisible:
            embed.add_field(
                name=":moyai: **User Status**",
                value="( ) :green_circle: Online\n( ) :yellow_circle: Idle\n( ) :red_circle: Do Not Disturb\n(*) :black_circle: Offline/Invisible"
            )
        

        await ctx.channel.send(embed=embed)


    @commands.command()
    async def source(self, ctx: Context):
        '''
        Sends the link to the GitHub repository where the source code is kept.
        '''
        embed = discord.Embed(
            title="Source code",
            description="Check out the source code on [GitHub](https://github.com/erick-dsnk/uncle-dunks-discord-bot)"
        )
        await ctx.send(embed=embed)


    @commands.command(aliases=['sv', 'server', 'svinfo', 'svi'])
    async def serverinfo(self, ctx: Context):
        '''
        Get information about the server the command was used in.
        '''
        embed = discord.Embed(
            color=discord.Color.dark_blue()
        )
        c = 0
        b = 0
        for i in ctx.guild.members:
            if i.bot:
                b = b + 1
            else:
                c = c + 1

        offline = 0
        online = 0
        idle = 0
        dnd = 0

        for user in ctx.guild.members:
            if user.status == discord.Status.offline:
                offline += 1
            
            elif user.status == discord.Status.online:
                online += 1

            elif user.status == discord.Status.idle:
                idle += 1

            elif user.status == discord.Status.dnd:
                dnd += 1

        embed.set_thumbnail(url=ctx.guild.icon_url)

        embed.set_author(
            name='Server Info',
            icon_url='https://www.trendmicro.com/azure/wp-content/uploads/2015/11/TM_ServerSequence_300x300.gif'
        )

        embed.add_field(
            name=":ballot_box: Name:",
            inline=True,
            value=f"**{ctx.guild.name}**"
        )

        embed.add_field(
            name=":crown: Owner:", inline=True,
            value=f"{ctx.guild.owner.mention}"
        
        )
        embed.add_field(
            name=":credit_card: Server ID",
            inline=True,
            value=f'`{ctx.guild.id}`'
        )

        embed.add_field(
            name=":person_pouting: Members: ",
            inline=True,
            value=f"`{c}`"
        )

        embed.add_field(
            name=":robot: Bots: ",
            inline=True,
            value=f"`{b}`"
        )

        embed.add_field(
            name="Online: ",
            inline=True,
            value=f":green_circle:  `{online}`"
        )

        embed.add_field(
            name="Idle: ",
            inline=True,
            value=f":yellow_circle:  `{idle}`"
        )

        embed.add_field(
            name="Do not disturb: ",
            inline=True,
            value=f":red_circle:  `{dnd}`"
        )

        embed.add_field(
            name="Offline : ",
            inline=True,
            value=f":black_circle:  `{offline}`"
        )

        embed.add_field(
            name=":calendar: Server created at: ",
            value=f"{ctx.guild.created_at.strftime('%A, %B , `%d` : `%Y` @ `%H:%M:%S` UTC')}",
            inline=False
        )

        embed.add_field(
            name=":printer:  Text Channels:",
            inline=True,
            value=f"`{len(ctx.guild.text_channels)}`"
        )

        embed.add_field(
            name=":microphone2:  Voice Channels:",
            inline=True,
            value=f"`{len(ctx.guild.voice_channels)}`"
        )

        embed.add_field(
            name="Roles: ",
            inline=True,
            value=f'`{len(ctx.guild.roles)}`'
        )

        embed.set_footer(
            icon_url=ctx.author.avatar_url,
            text=f"Requested by {ctx.author.name} on {ctx.message.created_at.strftime ('%A %B %d %Y @ %H:%M:%S %p')}"
        )

        await ctx.send(embed=embed)


    @commands.command()
    async def remindme(self, ctx: Context, after: str, *, reminder: str):
        '''
        Set a reminder and Uncle Dunk will tag you after the amount of time specified!
        '''
        initial = ""
        
        if 's' in after:
            after = int(after.strip('s'))

            initial = f"{after} seconds"
        
        elif 'm' in after:
            after = int(after.strip('m')) * 60

            initial = f"{after} minutes"
        
        elif 'h' in after:
            after = int(after.strip('h')) * 3600

            initial = f"{after} hours"
        
        elif 'd' in after:
            after = int(after.strip('d')) * 86400

            initial = f"{after} days"
        
        else:
            after = int(after)

            initial = f"{after} seconds"
        
        
        embed = discord.Embed(
            title=f":white_check_mark: Successfully set a reminder!",
            description=f"Will remind you to `{reminder}` in `{initial}`.",
            color=discord.Color.blurple()
        )

        await ctx.send(embed=embed)

        await asyncio.sleep(after)

        new_embed = discord.Embed(
            title="Wake up sleepy head!",
            description=f"Time to `{reminder}`! {ctx.author.mention}",
            color=discord.Color.green()
        )

        await ctx.send(embed=new_embed)


    @commands.command()
    async def topgg(self, ctx: Context):
        '''
        Get the top.gg page of Uncle Dunk.
        '''
        await ctx.send("My top.gg page! https://top.gg/bot/743859839821807736")
    

    @commands.command(aliases=['changes', 'change'])
    async def changelog(self, ctx: Context):
        '''
        Show Uncle Dunk's latest features and commands!
        '''

        with open(os.path.abspath('changelog.txt'), 'r') as f:
            changelog_message = f.read()

        embed = discord.Embed(
            title=':robot: Uncle Dunk Changelog!',
            description=changelog_message,
            color=discord.Color.green()
        )

        embed.set_footer(text="Uncle Dunk v1.6.7")

        await ctx.send(embed=embed)

    @commands.command(aliases=['c', 'col', 'hex'])
    async def color(self, ctx: Context, hex_code: str):
        '''
        Get an image of the specified hex color!
        '''
        im = Image.new("RGB", (100, 100), hex_to_rgb(hex_code))

        buffer = BytesIO()

        im.save(buffer, "png")

        buffer.seek(0)

        await ctx.send(file=discord.File(fp=buffer, filename="color.png"))


    @commands.command(aliases=['urban', 'dictionary', 'dict'])
    async def define(self, ctx: Context, *, query: str):
        '''
        Define a phrase using Urban Dictionary!
        '''

        url = "https://mashape-community-urban-dictionary.p.rapidapi.com/define"

        querystring = {"term": query}

        headers = {
            'x-rapidapi-key': get_rapid_api_key(),
            'x-rapidapi-host': "mashape-community-urban-dictionary.p.rapidapi.com"
        }

        resp = requests.request(
            method='GET',
            url=url,
            headers=headers,
            params=querystring
        ).json()['list'][0:3]
        
        i = 0

        embed = discord.Embed(
            title=f'Urban Dictionary: {resp[i]["word"]}',
            description=f'**Definition**: {resp[i]["definition"]}',
            color=discord.Color.blurple()
        )

        msg = await ctx.send(embed=embed)

        await msg.add_reaction('▶️')
        await msg.add_reaction('◀️')
        await msg.add_reaction('❌')

        def check(reaction, user):
            return (
                user == ctx.message.author and reaction.emoji == '◀️'
            ) or (
                user == ctx.message.author and reaction.emoji == '▶️'
            ) or (
                user == ctx.message.author and reaction.emoji == '❌'
            )
        
        while True:
            try:
                reaction, user = await self.bot.wait_for(
                    'reaction_add',
                    timeout=60.0,
                    check=check
                )

                if str(reaction.emoji) == '▶️':
                    if i < 2:
                        i += 1

                    else:
                        i = 0
                
                if str(reaction.emoji) == '◀️':
                    if i > 0:
                        i -= 1

                    else:
                        i = 2
                
                elif str(reaction.emoji) == '❌':
                    break
                    
                embed = discord.Embed(
                    title=f'Urban Dictionary: {resp[i]["word"]}',
                    description=f'**Definition**: {resp[i]["definition"]}',
                    color=discord.Color.blurple()
                )

                await msg.edit(embed=embed)

            except asyncio.TimeoutError:
                break



def setup(bot):
    bot.add_cog(Utility(bot))
