import speech_recognition as sr
import discord
import requests
from discord.ext import commands
from apiKeys import *
import json

privilegios = discord.Intents.all()
client = commands.Bot(intents=privilegios, command_prefix='!')
r = sr.Recognizer()


@client.command(pass_context=True)
async def join(ctx):
    channel = client.get_channel(ctx.author.voice.channel.id)
    if(ctx.author.voice):
        channel == ctx.message.author.voice.channel
        await channel.connect()
    else:
        await ctx.send('')


def pergunta(texto):
    data = {"model": "text-davinci-003",
            "prompt": texto, "max_tokens": 200}
    response = requests.post(API_URL_COMPLETIONS, headers={
        "Authorization": f"Bearer {OPENAI_TOKEN}",
        "Content-Type": "application/json",
    }, data=json.dumps(data))

    # Verifica se a solicitação foi bem-sucedida
    if response.status_code == 200:
        # A resposta gerada pelo modelo está armazenada em response.json()["choices"][0]["text"]
        response_text = response.json()["choices"][0]["text"]
        return response_text
    else:
        # Se a solicitação não foi bem-sucedida, pode haver um erro
        # Verifique a resposta para obter mais informações
        print(response.status_code, response.text)


@client.event
async def on_voice_state_update(member, before, after):
    channelvoz = client.get_channel(after.channel.id)
    channel = client.get_channel(880579854347685888)
    with sr.Microphone() as source:
        audio = r.listen(source)
    try:
        command = r.recognize_google(audio, language="pt-BR")
        # await channel.send(command)
        await channel.send(pergunta(command))
    except sr.UnknownValueError:
        await channel.send('')

client.run(BOT_TOKEN)
