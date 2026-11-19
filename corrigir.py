import discord
from discord.ext import commands
import re

# Configurações do bot
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(
    command_prefix="!",
    intents=intents
)

# Dicionário de correções
correcoes = {
    "vc": "você",
    "pq": "porque",
    "tb": "também",
    "q": "que",
    "n": "não",
    "hj": "hoje",
    "blz": "beleza",
    "obg": "obrigado",
    "naum": "não",
    "eh": "é",
    "tbm": "também"
}

# Função para corrigir mensagens
def corrigir_texto(texto):

    for errado, certo in correcoes.items():
        texto = re.sub(
            r'\b' + re.escape(errado) + r'\b',
            certo,
            texto,
            flags=re.IGNORECASE
        )

    # Primeira letra maiúscula
    texto = texto.strip()

    if not texto:
        return texto

    texto = texto[0].upper() + texto[1:]

    # Adiciona pontuação
    if texto[-1] not in ".!?":
        texto += "."

    return texto


# Quando o bot ligar
@bot.event
async def on_ready():
    print(f"Estamos logados como {bot.user}")


# Corrigir mensagens automaticamente
@bot.event
async def on_message(message):

    # Ignora o próprio bot
    if message.author.bot:
        return

    texto_original = message.content

    # Ignora mensagens vazias
    if not texto_original.strip():
        await bot.process_commands(message)
        return

    texto_corrigido = corrigir_texto(texto_original)

    # Só envia se houver alteração
    if texto_corrigido != texto_original:
        await message.channel.send(
            f"**Mensagem corrigida de {message.author.display_name}:**\n"
            f"{texto_corrigido}"
        )

    await bot.process_commands(message)


# Comando de teste
@bot.command()
async def hello(ctx):
    await ctx.send(f"Olá! Eu sou o bot {bot.user}")


@bot.command()
async def oi(ctx, x: int):
    await ctx.send("oi " * x)


# Iniciar bot
bot.run()
