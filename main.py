import discord, urllib.parse, requests, json
from discord.ext import commands

#Code - 0.75
#Last Change - Added actor search.


# This will search for a file named 'token_key.txt' in the same directory where 'main.py' is (unless you specify otherwise) and
# store the text in its first line in a variable named 'token' and the text in its second line in a variable named 'api_key'. 
file = open('token_key.txt', 'r')
token = file.readline()
api_key = file.readline()
file.close()


# First line tells the program what our prefix is going to be, you can edit it if you want. The second line removes the default 'help'
# command that comes integrated with discord.py and allows you to have your own custom 'help' command.
client = commands.Bot(command_prefix = 'tv!')
client.remove_command('help')


# The code that get executed as soon as your bot comes online, right now it sets its status as 'playing a game' and prints 'Online as {bot name}.
@client.event
async def on_ready():
    game = discord.Game("innocent. Type - tv!help.")
    await client.change_presence(status=discord.Status.online, activity=game)
    print('Online as {0.user}'.format(client))


# Response to 'tv!ping' command.
@client.command()
async def ping(ctx):
    await ctx.send(f'Pong! {round(client.latency*1000)}ms')


# Resposne to 'tv!help', it is an embedded message as all of our next resposnes are going to be, see this page - 'https://cog-creators.github.io/discord-embed-sandbox/'
@client.command()
async def help(ctx):
    embed=discord.Embed(title="Visit TMDb website.", url="https://www.themoviedb.org/", description="This product uses the TMDb API but is not endorsed or certified by TMDb.")
    embed.set_thumbnail(url="https://i.ibb.co/V9y2wh1/ezgif-3-d878dd47b3b4.png")
    embed.add_field(name="tvBot help page.", value="Commands and basic info: ", inline=True)
    embed.add_field(name="tv!ping", value="Check latency.", inline=False)
    embed.add_field(name="tv!movie", value="Search for a movie.", inline=False)
    embed.add_field(name="tv!tvshow", value="Search for a TV show.", inline=False)
    embed.add_field(name="tv!person", value="Search for an actor or actress.", inline=False)
    embed.set_footer(text="Talk to the developer - Sam Cooper#9490")
    await ctx.send(embed=embed)



# 'movie/movies' command, it only prints out 3 results maximum since the number of results can vary and I couldn't figure out how to deal with that.
@client.command(aliases=['movies'])
async def movie(ctx, *, movie_search_str):
    encoded_search_str = urllib.parse.quote(movie_search_str)    #URL-encodes the search string.
    response = requests.get(f'https://api.themoviedb.org/3/search/movie?api_key={api_key}&query={encoded_search_str}&page=1&include_adult=false')
    movie_result_dict = response.json()      #To understand how I am fetching values from the response dictionary, make a separate program and print the json response.
    if (movie_result_dict['total_results']) == 0:
        await ctx.send('Your search returned 0 results.')

    elif (movie_result_dict['total_results']) == 1:
        movie_title1 = ((movie_result_dict.get('results')[0])['title'])
        movie_id1 = ((movie_result_dict.get('results')[0])['id'])
        movie_desc1 = ((movie_result_dict.get('results')[0])['overview'])
        movie_thumb1 = ((movie_result_dict.get('results')[0])['poster_path'])
        embed1 = discord.Embed(
        title=f'{movie_title1}',
        url=f"https://www.themoviedb.org/movie/{movie_id1}",
        description=f"{movie_desc1}",
        color = discord.Colour.blue()
        )
        embed1.set_image(url=f"https://image.tmdb.org/t/p/original{movie_thumb1}")
        embed1.add_field(name="Movie ID: ", value=f"{movie_id1} (Use this ID for ID based commands.)", inline=True)
        await ctx.send(f'Search results for: **{movie_search_str}**')
        await ctx.send(embed=embed1)

    elif (movie_result_dict['total_results']) == 2:
        movie_title1 = ((movie_result_dict.get('results')[0])['title'])
        movie_id1 = ((movie_result_dict.get('results')[0])['id'])
        movie_desc1 = ((movie_result_dict.get('results')[0])['overview'])
        movie_thumb1 = ((movie_result_dict.get('results')[0])['poster_path'])
        movie_title2 = ((movie_result_dict.get('results')[1])['title'])
        movie_id2 = ((movie_result_dict.get('results')[1])['id'])
        movie_desc2 = ((movie_result_dict.get('results')[1])['overview'])
        movie_thumb2 = ((movie_result_dict.get('results')[1])['poster_path'])
        embed1 = discord.Embed(
        title=f'{movie_title1}',
        url=f"https://www.themoviedb.org/movie/{movie_id1}",
        description=f"{movie_desc1}",
        color = discord.Colour.blue()
        )
        embed1.set_image(url=f"https://image.tmdb.org/t/p/original{movie_thumb1}")
        embed1.add_field(name="Movie ID: ", value=f"{movie_id1} (Use this ID for ID based commands.)", inline=True)
        embed2 = discord.Embed(
        title=f'{movie_title2}',
        url=f"https://www.themoviedb.org/movie/{movie_id2}",
        description=f"{movie_desc2}",
        color = discord.Colour.blue()
        )
        embed2.set_image(url=f"https://image.tmdb.org/t/p/original{movie_thumb2}")
        embed2.add_field(name="Movie ID: ", value=f"{movie_id2} (Use this ID for ID based commands.)", inline=True)
        await ctx.send(f'Search results for: **{movie_search_str}**')
        await ctx.send(embed=embed1)
        await ctx.send(embed=embed2)

    else:  # since the number of results is not 0, 1, or 2, it must be 3 or more, in this case, we can safely fetch values for first 3 results without checking how many results are there.
        movie_title1 = ((movie_result_dict.get('results')[0])['title'])
        movie_id1 = ((movie_result_dict.get('results')[0])['id'])
        movie_desc1 = ((movie_result_dict.get('results')[0])['overview'])
        movie_thumb1 = ((movie_result_dict.get('results')[0])['poster_path'])
        movie_title2 = ((movie_result_dict.get('results')[1])['title'])
        movie_id2 = ((movie_result_dict.get('results')[1])['id'])
        movie_desc2 = ((movie_result_dict.get('results')[1])['overview'])
        movie_thumb2 = ((movie_result_dict.get('results')[1])['poster_path'])
        movie_title3 = ((movie_result_dict.get('results')[2])['title'])
        movie_id3 = ((movie_result_dict.get('results')[2])['id'])
        movie_desc3 = ((movie_result_dict.get('results')[2])['overview'])
        movie_thumb3 = ((movie_result_dict.get('results')[2])['poster_path'])

        embed1 = discord.Embed(
        title=f'{movie_title1}',
        url=f"https://www.themoviedb.org/movie/{movie_id1}",
        description=f"{movie_desc1}",
        color = discord.Colour.blue()
        )
        embed1.set_image(url=f"https://image.tmdb.org/t/p/original{movie_thumb1}")
        embed1.add_field(name="Movie ID: ", value=f"{movie_id1} (Use this ID for ID based commands.)", inline=True)
        embed2 = discord.Embed(
        title=f'{movie_title2}',
        url=f"https://www.themoviedb.org/movie/{movie_id2}",
        description=f"{movie_desc2}",
        color = discord.Colour.blue()
        )
        embed2.set_image(url=f"https://image.tmdb.org/t/p/original{movie_thumb2}")
        embed2.add_field(name="Movie ID: ", value=f"{movie_id2} (Use this ID for ID based commands.)", inline=True)
        embed3 = discord.Embed(
        title=f'{movie_title3}',
        url=f"https://www.themoviedb.org/movie/{movie_id3}",
        description=f"{movie_desc3}",
        color = discord.Colour.blue()
        )
        embed3.set_image(url=f"https://image.tmdb.org/t/p/original{movie_thumb3}")
        embed3.add_field(name="Movie ID: ", value=f"{movie_id3} (Use this ID for ID based commands.)", inline=True)
        await ctx.send(f'Search results for: **{movie_search_str}**')
        await ctx.send(embed=embed1)
        await ctx.send(embed=embed2)
        await ctx.send(embed=embed3)

# same as above, just tv shows instead of movies.
@client.command(aliases=['tvshows'])
async def tvshow(ctx, *, tv_search_str):
    encoded_search_str = urllib.parse.quote(tv_search_str)
    response = requests.get(f'https://api.themoviedb.org/3/search/tv?api_key={api_key}&query={encoded_search_str}&page=1&include_adult=false')
    tv_result_dict = response.json()
    
    if (tv_result_dict['total_results']) == 0:
        await ctx.send('Your search returned 0 results.')

    elif (tv_result_dict['total_results']) == 1:
        tv_title1 = ((tv_result_dict.get('results')[0])['name'])
        tv_id1 = ((tv_result_dict.get('results')[0])['id'])
        tv_desc1 = ((tv_result_dict.get('results')[0])['overview'])
        tv_thumb1 = ((tv_result_dict.get('results')[0])['poster_path'])

        embed1 = discord.Embed(
        title=f'{tv_title1}',
        url=f"https://www.themoviedb.org/tv/{tv_id1}",
        description=f"{tv_desc1}",
        color = discord.Colour.blue()
        )
        embed1.set_image(url=f"https://image.tmdb.org/t/p/original{tv_thumb1}")
        embed1.add_field(name="TV Show ID: ", value=f"{tv_id1} (Use this ID for ID based commands.)", inline=True)
        await ctx.send(f'Search results for: **{tv_search_str}**')
        await ctx.send(embed=embed1)


    elif (tv_result_dict['total_results']) == 2:
        tv_title1 = ((tv_result_dict.get('results')[0])['name'])
        tv_id1 = ((tv_result_dict.get('results')[0])['id'])
        tv_desc1 = ((tv_result_dict.get('results')[0])['overview'])
        tv_thumb1 = ((tv_result_dict.get('results')[0])['poster_path'])
        tv_title2 = ((tv_result_dict.get('results')[1])['name'])
        tv_id2 = ((tv_result_dict.get('results')[1])['id'])
        tv_desc2 = ((tv_result_dict.get('results')[1])['overview'])
        tv_thumb2 = ((tv_result_dict.get('results')[1])['poster_path'])

        embed1 = discord.Embed(
        title=f'{tv_title1}',
        url=f"https://www.themoviedb.org/tv/{tv_id1}",
        description=f"{tv_desc1}",
        color = discord.Colour.blue()
        )
        embed1.set_image(url=f"https://image.tmdb.org/t/p/original{tv_thumb1}")
        embed1.add_field(name="TV Show ID: ", value=f"{tv_id1} (Use this ID for ID based commands.)", inline=True)

        embed2 = discord.Embed(
        title=f'{tv_title2}',
        url=f"https://www.themoviedb.org/tv/{tv_id2}",
        description=f"{tv_desc2}",
        color = discord.Colour.blue()
        )
        embed2.set_image(url=f"https://image.tmdb.org/t/p/original{tv_thumb2}")
        embed2.add_field(name="TV Show ID: ", value=f"{tv_id2} (Use this ID for ID based commands.)", inline=True)

        await ctx.send(f'Search results for: **{tv_search_str}**')
        await ctx.send(embed=embed1)
        await ctx.send(embed=embed2)


    else:
        tv_title1 = ((tv_result_dict.get('results')[0])['name'])
        tv_id1 = ((tv_result_dict.get('results')[0])['id'])
        tv_desc1 = ((tv_result_dict.get('results')[0])['overview'])
        tv_thumb1 = ((tv_result_dict.get('results')[0])['poster_path'])
        tv_title2 = ((tv_result_dict.get('results')[1])['name'])
        tv_id2 = ((tv_result_dict.get('results')[1])['id'])
        tv_desc2 = ((tv_result_dict.get('results')[1])['overview'])
        tv_thumb2 = ((tv_result_dict.get('results')[1])['poster_path'])
        tv_title3 = ((tv_result_dict.get('results')[2])['name'])
        tv_id3 = ((tv_result_dict.get('results')[2])['id'])
        tv_desc3 = ((tv_result_dict.get('results')[2])['overview'])
        tv_thumb3 = ((tv_result_dict.get('results')[2])['poster_path'])

        embed1 = discord.Embed(
        title=f'{tv_title1}',
        url=f"https://www.themoviedb.org/tv/{tv_id1}",
        description=f"{tv_desc1}",
        color = discord.Colour.blue()
        )
        embed1.set_image(url=f"https://image.tmdb.org/t/p/original{tv_thumb1}")
        embed1.add_field(name="TV Show ID: ", value=f"{tv_id1} (Use this ID for ID based commands.)", inline=True)

        embed2 = discord.Embed(
        title=f'{tv_title2}',
        url=f"https://www.themoviedb.org/tv/{tv_id2}",
        description=f"{tv_desc2}",
        color = discord.Colour.blue()
        )
        embed2.set_image(url=f"https://image.tmdb.org/t/p/original{tv_thumb2}")
        embed2.add_field(name="TV Show ID: ", value=f"{tv_id2} (Use this ID for ID based commands.)", inline=True)

        embed3 = discord.Embed(
        title=f'{tv_title3}',
        url=f"https://www.themoviedb.org/tv/{tv_id3}",
        description=f"{tv_desc3}",
        color = discord.Colour.blue()
        )
        embed3.set_image(url=f"https://image.tmdb.org/t/p/original{tv_thumb3}")
        embed3.add_field(name="TV Show ID: ", value=f"{tv_id3} (Use this ID for ID based commands.)", inline=True)

        await ctx.send(f'Search results for: **{tv_search_str}**')
        await ctx.send(embed=embed1)
        await ctx.send(embed=embed2)
        await ctx.send(embed=embed3)


        
# This only prints 1 result
@client.command(aliases=['actor', 'actors'])
async def person(ctx, *, actor_search_str):
    encoded_search_str = urllib.parse.quote(actor_search_str)
    response = requests.get(f'https://api.themoviedb.org/3/search/person?api_key={api_key}&query={encoded_search_str}&page=1&include_adult=false')
    actor_result_dict = response.json()

    if (actor_result_dict.get('total_results')) == 0 or ((actor_result_dict.get('results')[0])['known_for_department']) != 'Acting':   # along with confirming that the response dictionary is not empty, I am also making sure the person is an actor.
        await ctx.send('Your search returned 0 results.')

    else:
        actor_id = ((actor_result_dict.get('results')[0])['id'])
        id_query_response = requests.get(f'https://api.themoviedb.org/3/person/{actor_id}?api_key={api_key}&language=en-US')     # The search api endpoint does not get you their biographies so you have to make another request on person details API.
        actor_info_dict = id_query_response.json()

        actor_name = ((actor_result_dict.get('results')[0])['name'])
        bio = (actor_info_dict.get('biography'))
        
        if (len(bio)) > 2048:                   # The discription body of an embedded message has a limit of 2048 characters, this code slices out a portion of biography to make sure it fits in.
            actor_bio = (bio[0:2030] + '.....')
        else:
            actor_bio = bio

        actor_img = ((actor_result_dict.get('results')[0])['profile_path'])

        embed1 = discord.Embed(
        title=f'{actor_name}',
        url=f"https://www.themoviedb.org/person/{actor_id}",
        description=f"{actor_bio}",
        color = discord.Colour.blue()
        )
        embed1.set_image(url=f"https://image.tmdb.org/t/p/original{actor_img}")
        
        await ctx.send(f'Search results for: **{actor_search_str}**')
        await ctx.send(embed=embed1)





# That was it, have a good day!

client.run(token)
