import core.boost
import core.setup
import discord, os, time
from datetime import datetime
from core.logger import logger
from discord.ext import commands
from discord.ui import InputText, Modal
from discord.ui import Select, View
from colorama import Fore

data = core.setup.setup()
guild = data.guild
types = data.acti_type == ""


def is_admin(author: int):
    if author in data.admins:
        return True
    else: 
        return False

def licensed(user):
    try:
        open(f"users/{user}.txt", "r")
        return True
    except FileNotFoundError:
        return False

no_perms = discord.Embed(title="**🚫 | Access Denied**", description="You dont have permissions to do this", timestamp=datetime.now(), color=discord.Colour.red())
bot = commands.Bot(command_prefix=data.prefix, intents=discord.Intents.all())

@bot.event
async def on_ready():
    core.setup.setup().print_data()

    if data.status_type == "idle":
        await bot.change_presence(status=discord.Status.idle)
    elif data.status_type == "online":
        await bot.change_presence(status=discord.Status.online)
    elif data.status_type == "do_not_disturb":
        await bot.change_presence(status=discord.Status.do_not_disturb)

    if data.acti_type == "playing":
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name=data.activity))
    elif data.acti_type == "watching":
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=data.activity))
    elif data.acti_type == "streaming":
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.streaming, name=data.activity))
    elif data.acti_type == "competing":
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.competing, name=data.activity))
    elif data.acti_type == "listening":
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=data.activity))
    logger().success("Finished Starting")

class question(Modal):
    def __init__(self) -> None:
        super().__init__(title="Server Boosting info") #title of the modal up top
        self.add_item(InputText(label="Discord Server Invite", placeholder="https://discord.gg/highboost", required=True)) 
        self.add_item(InputText(label="How many boosts (even)", placeholder="14", required=True, max_length=5))

    async def callback(self, interaction: discord.Interaction):
        invite = self.children[0].value
        amount = int(self.children[1].value)
        if not (amount % 2) == 0:
            await interaction.response.send_message("Amount must be even")
        inv = invite.replace("//", "")
        if "/invite/" in inv: inv = inv.split("/invite/")[1]
        elif "/" in inv: inv = inv.split("/")[1]
        await interaction.response.send_message(f"Started Boosting {amount}x's")
        go = time.time()
        core.boost.boosting().boost(interaction.user.id, inv, amount)
        end = time.time()
        time_went = round(end - go, 5)
        return await interaction.channel.send(f"Finished boosting for {amount}x's  in {time_went}s")

if data.payment:
    @bot.slash_command(guild = discord.Object(id=guild), name="payments", description="Shows all the payment methods")
    async def payments(interaction: discord.Interaction):
        logger().info(f"{interaction.user} ({interaction.user.id}) ran a command")
        select = Select(
            max_values=1,
            placeholder="Payment Tags and Addresses",
            options=[
                    discord.SelectOption(label="Paypal", emoji=data.pp, description="Paypal Email", value=str(data.paypal)) if data.d_pp else None, 
                    discord.SelectOption(label="Cashapp", emoji=data.capp, description="Cashapp Tag", value=str(data.cashapp)) if data.d_ca else None, 
                    discord.SelectOption(label="Litecoin", emoji=data.ltc, description="Litecoin Address", value=str(data.litecoin)) if data.d_ltc else None, 
                    discord.SelectOption(label="Bitcoin", emoji=data.btc, description="Bitcoin Address", value=str(data.bitcoin)) if data.d_btc else None,
                    discord.SelectOption(label="Ethereum", emoji=data.eth, description="Ethereum Address", value=str(data.ethereum)) if data.d_eth else None,
                    discord.SelectOption(label="Solana", emoji=data.sol, description="Solana Address", value=str(data.solana)) if data.d_sol else None,
                    discord.SelectOption(label="Monero", emoji=data.mon, description="Monero Address", value=str(data.monero)) if data.d_mon else None,
                    discord.SelectOption(label="Bitcoin Cash", emoji=data.bhc, description="Bitcoin Cash Address", value=str(data.bit_cash)) if data.d_bhc else None,
            ]
        )
        async def my_callback(interaction: discord.Interaction):
            await interaction.response.send_message(f"{select.values[0]}", ephemeral=True)
        select.callback = my_callback
        view = View()
        view.add_item(select)
        embed=discord.Embed(title="Select your Payment Method", timestamp=datetime.now(), color=discord.Colour.magenta())
        await interaction.response.send_message(embed=embed, view=view)


if data.stock:
    @bot.slash_command(guild = discord.Object(id=guild), name="stock", description="shows ur stock")
    async def stock(interaction: discord.Interaction):
        logger().info(f"{interaction.user} ({interaction.user.id}) ran a command")
        if not licensed(interaction.user.id):
            stock = open(f"users/{data.main}.txt").read().splitlines()
            await interaction.response.send_message(f"{len (2 * (stock))} boosts in stock")
        elif licensed(interaction.user.id):
            stock = open(f"users/{interaction.user.id}.txt").read().splitlines()
            await interaction.response.send_message(f"{len (2 * (stock))} boosts in stock")

if data.restock:
    @bot.slash_command(guild = discord.Object(id=guild), name="restock", description="Restock tokens")
    async def restock(interaction: discord.Interaction, file: discord.Attachment):
        logger().info(f"{interaction.user} ({interaction.user.id}) ran a command")
        if not licensed(interaction.user.id):
            await interaction.response.send_message(embed=no_perms, ephemeral=True)
        if licensed(interaction.user.id):
            tokens = await file.read()
            tokens = tokens.decode()
            with open(f"users/{interaction.user.id}.txt", "a") as tokens_input:
                for token in tokens.splitlines():
                    tokens_input.write(token + "\n")
            await interaction.response.send_message(f"Restocked {len(tokens.splitlines())} tokens")



if data.license:
    @bot.slash_command(guild = discord.Object(id=guild), name="license", description="name tells everything")
    async def license(interaction: discord.Interaction, user: discord.User):
        logger().info(f"{interaction.user} ({interaction.user.id}) ran a command")
        if not is_admin(interaction.user.id):
            await interaction.response.send_message(embed=no_perms, ephemeral=True)
        elif is_admin(interaction.user.id):
            if not licensed(user.id):
                logger().info(f"{user} ({user.id}) is not licensed, giving his license")
                open(f"users/{user.id}.txt", 'w')
                await interaction.response.send_message(f"Licensed {user.mention}")
            elif licensed(user.id):
                logger().info(f"{user} ({user.id}) is licensed, removed his license")
                os.remove(f"users/{user.id}.txt")
                await interaction.response.send_message(f"Unlicensed {user.mention}")

if data.boost:
    @bot.slash_command(guild = discord.Object(id=guild), name="boost", description="boost servers")
    async def boost1(interaction: discord.Interaction):   
        logger().info(f"{interaction.user} ({interaction.user.id}) ran a command")
        if not licensed(interaction.user.id):
            await interaction.response.send_message(embed=no_perms, ephemeral=True)
        elif licensed(interaction.user.id):
            await interaction.response.send_modal(question())



bot.run(data.token)
