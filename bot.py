import os, asyncio, discord
from discord import app_commands
from dotenv import load_dotenv
load_dotenv()
import db, ia

PROMPT_PADRAO = open("prompts/nexus_souls.md", encoding="utf-8").read()
LIMITE = int(os.getenv("LIMITE_DIARIO", 5))

intents = discord.Intents.default()
intents.message_content = True  # ative também no Developer Portal
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

@client.event
async def setup_hook():
    await tree.sync()

@tree.command(name="personalidade", description="Define o prompt da IA deste servidor")
@app_commands.default_permissions(administrator=True)
async def personalidade(inter: discord.Interaction, prompt: str):
    db.set_prompt(inter.guild_id, prompt)
    await inter.response.send_message("Personalidade atualizada.", ephemeral=True)

@tree.command(name="canal", description="Ativa a IA neste canal")
@app_commands.default_permissions(administrator=True)
async def canal(inter: discord.Interaction):
    _, canais = db.get_config(inter.guild_id)
    db.set_canais(inter.guild_id, list(set(canais + [inter.channel_id])))
    await inter.response.send_message("IA ativada neste canal.", ephemeral=True)

@client.event
async def on_message(msg: discord.Message):
    if msg.author.bot or not msg.guild:
        return
    prompt, canais = db.get_config(msg.guild.id)
    if not (client.user in msg.mentions or msg.channel.id in canais):
        return
    if not db.pode_usar(msg.guild.id, msg.author.id, LIMITE):
        return await msg.reply("Você atingiu o limite de perguntas de hoje.")
    historico = [f"{m.author.display_name}: {m.content}"
                 async for m in msg.channel.history(limit=10, before=msg)]
    contexto = "\n".join(reversed(historico))
    async with msg.channel.typing():
        try:
            texto = await asyncio.to_thread(
                ia.responder, prompt or PROMPT_PADRAO, contexto, msg.clean_content)
            db.registrar_uso(msg.guild.id, msg.author.id)
        except Exception:
            import traceback
            traceback.print_exc()
            texto = "Não consegui responder agora (limite da IA ou erro). Tente de novo em instantes."
    await msg.reply(texto[:1900])

client.run(os.environ["DISCORD_TOKEN"])
