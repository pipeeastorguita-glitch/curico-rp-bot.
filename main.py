import os
import re
import unicodedata
import discord
from discord.ext import commands

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)


def limpiar(texto):
    texto = unicodedata.normalize("NFKD", texto)
    texto = "".join(c for c in texto if not unicodedata.combining(c))
    return re.sub(r"[^a-z0-9]", "", texto.lower())


@bot.event
async def on_ready():
    print(f"Bot conectado: {bot.user}")
    await bot.tree.sync()


@bot.tree.command(
    name="crear_canales",
    description="Crear canales de Curicó RP"
)
async def crear_canales(interaction: discord.Interaction):

    if not interaction.user.guild_permissions.manage_channels:
        await interaction.response.send_message(
            "No tienes permiso.", ephemeral=True
        )
        return

    canales = {
        "INFORMACION": ["📜・reglas", "📢・anuncios"],
        "GENERAL": ["💬・chat-general", "🎮・chat-erlc"],
        "VERIFICACION": ["✅・verificacion", "❓・ayuda"],
        "TICKETS": ["🎫・abrir-ticket"],
        "POSTULACIONES": ["👮・policia", "🚒・bomberos", "🚑・ems"],
        "REPORTES": ["🚨・reportar-jugador"],
        "EVENTOS": ["🎉・eventos"],
        "MEDIA": ["📸・fotos", "🎥・videos"],
    }

    await interaction.response.defer(ephemeral=True)

    creados = 0
    no_encontradas = []

    for categoria_nombre, nombres in canales.items():
        categoria = next(
            (
                c for c in interaction.guild.categories
                if limpiar(c.name).endswith(limpiar(categoria_nombre))
            ),
            None
        )

        if categoria is None:
            no_encontradas.append(categoria_nombre)
            continue

        for nombre in nombres:
            existe = discord.utils.get(
                categoria.text_channels, name=nombre
            )
            if not existe:
                await interaction.guild.create_text_channel(
                    name=nombre, category=categoria
                )
                creados += 1

    mensaje = f"¡Listo! Se crearon {creados} canales."
    if no_encontradas:
        mensaje += "\nNo encontré estas categorías: " + ", ".join(no_encontradas)

    await interaction.followup.send(mensaje, ephemeral=True)


bot.run(os.environ["DISCORD_TOKEN"])
