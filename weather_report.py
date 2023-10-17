import discord
from discord.ext import commands
import requests


bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())
bot_token = "YourBotsToken"
weather_api_key = "YourApiKey"

@bot.event
async def on_ready():
    print(f"We have logged in as {bot.user}")

@bot.command()
async def weather(ctx, *location):
    location = ' '.join(location)
    if await get_weather(ctx, location) == False:
        await ctx.send("Sorry, I couldn't retrieve the weather information.")


async def get_weather(ctx, location):
    base_url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": location, 
        "appid": weather_api_key,
        "units": "metric"
    }
    response = requests.get(base_url, params=params)

    if response.status_code != 200:        
        return False
    
    data = response.json()   
    temperature = data["main"]["temp"]
    description = data["weather"][0]["description"]
    weather_icon = data["weather"][0]["icon"]
    weather_icon_url = f"https://openweathermap.org/img/wn/{weather_icon}.png"
    humidity = data["main"]["humidity"]
    pressure = data["main"]["pressure"]
    wind = data["wind"]["speed"] 
    who_called = ctx.author.display_name
    icon = ctx.author.avatar
    accent_color = ctx.author.accent_color
    embed = discord.Embed(title=f"Weather in {location}", description=f"Currently {temperature}°C, {description}", color=accent_color)
    embed.add_field(name="Humidity", value=f"{humidity}%", inline=True)
    embed.add_field(name="Air Pressure", value=f"{pressure} hPa", inline=True)
    embed.add_field(name="Wind Speed", value=f"{wind} m/s", inline=True)
    embed.set_author(name=who_called, icon_url=icon)
    embed.set_thumbnail(url=weather_icon_url)
    embed.set_image(url="https://i.redd.it/ux93fxldhoxa1.gif")
    embed.set_footer(text="...")
    await ctx.send(embed=embed)


@bot.command()
async def forecast(ctx, *location):
    location = ' '.join(location)
    if await get_forecast(ctx, location) == False:
        await ctx.send("Sorry, I couldn't retrieve the weather information.")

async def get_forecast(ctx, location):
    base_url = "https://api.openweathermap.org/data/2.5/forecast/daily"
    params = {
        "q": location, 
        "appid": weather_api_key, 
        "units": "metric"
    }

    response = requests.get(base_url, params=params)
    if response.status_code != 200:
        return False
    
    embed = discord.Embed(title=f"7-Day Weather Forecast for {location}")

    for day in forecast_data:
        date = day["dt_txt"]
        max = day["main"]["temp_max"]
        min = day["main"]["temp_min"]
        temperature = day["main"]["temp"]
        description = day["weather"][0]["description"]
        embed.add_field(name=date, value=f"{description}\n{temperature}°C", inline=False)

    await ctx.send(embed=embed)
bot.run(bot_token)