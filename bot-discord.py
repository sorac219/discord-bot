import discord
import os
from discord.ext import commands

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="/", intents=intents)


@bot.event
async def on_ready():
    print(f'Bot conectado como {bot.user}')
    try:
        synced = await bot.tree.sync()
        print(f"Comandos slash sincronizados: {len(synced)}")
    except Exception as e:
        print(f"Error al sincronizar comandos: {e}")


@bot.tree.command(name="ayuda", description="Muestra un menú de ayuda con varias opciones")
async def ayuda(interaction: discord.Interaction):
    options = [
        discord.SelectOption(label="Subir de Nivel", description="Ayuda para subir de nivel", emoji="💪"),
        discord.SelectOption(label="Farmear Ítem", description="Ayuda para ir a farmear un item especifico", emoji="🔄"),
        discord.SelectOption(label="Derrotar un Boss", description="Ayuda para derrotar a algun boss", emoji="👹"),
        discord.SelectOption(label="Poner stats a un equipo", description="Solicitud para poner stats a un equipamiento", emoji="🔮"),
        discord.SelectOption(label="Refinar equipo", description="Solicitud para refinar equipamiento", emoji="⚒️")
    ]

    select = discord.ui.Select(placeholder="Elige una opción...", options=options)

    async def select_callback(interaction: discord.Interaction):
        if interaction.message:
            try:
                await interaction.message.delete()  # Intentar eliminar el mensaje solo si existe
            except discord.Forbidden:
                print("El bot no tiene permisos para eliminar mensajes.")
            except discord.HTTPException as e:
                print(f"Error al intentar eliminar el mensaje: {e}")

        if select.values[0] == "Subir de Nivel":
            await handle_subir_nivel(interaction)
        elif select.values[0] == "Farmear Ítem":
            await handle_farmear_item(interaction)
        elif select.values[0] == "Derrotar un Boss":
            await handle_derrotar_boss(interaction)
        elif select.values[0] == "Poner stats a un equipo":
            await handle_arma_encantada(interaction)
        elif select.values[0] == "Refinar equipo":
            await interaction.response.send_message(
                f"{interaction.user.mention} ha solicitado ayuda para **Refinar equipo**.", ephemeral=False)

    select.callback = select_callback

    view = discord.ui.View()
    view.add_item(select)

    await interaction.response.send_message("Selecciona una opción del menú:", view=view)


async def handle_subir_nivel(interaction: discord.Interaction):
    class NivelModal(discord.ui.Modal, title="Subir de Nivel"):
        nivel = discord.ui.TextInput(label="Nivel deseado", placeholder="Ingresa un nivel entre 1 y 180")

        async def on_submit(self, interaction: discord.Interaction):
            try:
                if interaction.message:
                    await interaction.message.delete()  # Intentar eliminar el mensaje solo si existe

                nivel_value = int(self.nivel.value)
                if 1 <= nivel_value <= 180:
                    await interaction.response.send_message(f"{interaction.user.mention} quiere subir hasta el **nivel {nivel_value}**. ¡Ayuda requerida!", ephemeral=False)
                else:
                    await interaction.response.send_message(f"El nivel ingresado ({nivel_value}) no es válido. Debe ser entre 1 y 180.", ephemeral=True)
            except ValueError:
                await interaction.response.send_message("Por favor, ingresa un número válido.", ephemeral=True)

    await interaction.response.send_modal(NivelModal())


async def handle_farmear_item(interaction: discord.Interaction):
    class ItemModal(discord.ui.Modal, title="Farmear Ítem"):
        item_name = discord.ui.TextInput(label="Nombre del Ítem", placeholder="Escribe el nombre del ítem")

        async def on_submit(self, interaction: discord.Interaction):
            if interaction.message:
                await interaction.message.delete()  # Intentar eliminar el mensaje solo si existe

            await interaction.response.send_message(
                f"{interaction.user.mention} quiere farmear el ítem **{self.item_name.value}**. ¡Apoyen en la tarea!",
                ephemeral=False)

    await interaction.response.send_modal(ItemModal())


async def handle_derrotar_boss(interaction: discord.Interaction):
    class BossModal(discord.ui.Modal, title="Derrotar un Boss"):
        boss_name = discord.ui.TextInput(label="Nombre del Boss", placeholder="Escribe el nombre del boss")

        async def on_submit(self, interaction: discord.Interaction):
            if interaction.message:
                await interaction.message.delete()  # Intentar eliminar el mensaje solo si existe

            await interaction.response.send_message(
                f"{interaction.user.mention} quiere derrotar a **{self.boss_name.value}**. ¡Prepárense para la batalla!",
                ephemeral=False)

    await interaction.response.send_modal(BossModal())


async def handle_arma_encantada(interaction: discord.Interaction):
    options = [
        discord.SelectOption(label="Armor", description="Poner stats a Armadura", emoji="🥋"),
        discord.SelectOption(label="Hb", description="Poner stats a Hb", emoji="🪓"),
        discord.SelectOption(label="Knuckle", description="Poner stats a Knuckles", emoji="🥊"),
        discord.SelectOption(label="Bow", description="Poner stats a Bow", emoji="🏹"),
        discord.SelectOption(label="Bowgun", description="Poner stats a Bowgun", emoji="🔫"),
        discord.SelectOption(label="1h", description="Poner stats a Espada", emoji="⚔"),
        discord.SelectOption(label="2h", description="Poner stats a Espada 2 manos", emoji="🗡"),
        discord.SelectOption(label="Md", description="Poner stats a Wings", emoji="🪁"),
        discord.SelectOption(label="Staff", description="Poner stats a Staff", emoji="🦯"),
        discord.SelectOption(label="Ktn", description="Poner stats a Katana", emoji="🔪"),
    ]

    select = discord.ui.Select(placeholder="Elige el tipo de arma...", options=options)

    async def select_arma_callback(interaction: discord.Interaction):
        if interaction.message:
            await interaction.message.delete()  # Intentar eliminar el mensaje solo si existe

        await interaction.response.send_message(
            f"{interaction.user.mention} ha solicitado ayuda para encantar una **{select.values[0]}**.",
            ephemeral=False)

    select.callback = select_arma_callback

    view = discord.ui.View()
    view.add_item(select)

    await interaction.response.send_message("Selecciona el tipo de arma para encantar:", view=view)

TOKEN = os.getenv('DISCORD_TOKEN')
bot.run(TOKEN)