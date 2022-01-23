import discord
import config
import traceback
from pathlib import Path
from discord.ext import commands
from utils import color
from utils.embed import embed
from utils.webserver import keep_alive

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix="-", help_command=None)

_modules_loaded, _modules_didnt_load, _modules_couldnt_load = "", "", ""
for file_path in Path("./modules").glob("**/*.py"):
    file_path = str(file_path).replace("/", ".")[:-3]
    file_name = file_path.split(".")[-1]
    if any(file in file_name for file in config.internal.modules_to_not_load):
        _modules_didnt_load += f"   │{file_name}\n"
        continue
    try:
        bot.load_extension(file_path)
    except Exception as fail:
        fail = str(fail).split("\n")
        fail = "\n   │".join(fail)
        length = len(f"Couldn't load {file_name}:") - 5
        that = "   ╭" + length*"─" + "╯"
        fail = f"{that}\n   │{fail}"
        _modules_couldnt_load += f"Couldn't load {file_name}:\n{fail}\n\n"
    else:
        _modules_loaded += f"   │{file_name}\n"


@bot.event
async def on_ready():
    print(color.green(f"\n\n\nLoaded:\n   ╭──╯\n{_modules_loaded}") + color.yellow(
        f"\nDidn't load:\n   ╭───────╯\n{_modules_didnt_load}") + color.red(f"\n{_modules_couldnt_load}"))
    print(
        f"\nLogged in as:\n   ╭────────╯\n   │{bot.user.name}\n   │{bot.user.id}\n\nPycord version:\n   ╭──────────╯\n   │{discord.__version__}\n\nServers connected to:\n   ╭────────────────╯")
    for guild in bot.guilds:
        print(f"   │{guild.name}")


@bot.group()
async def module(ctx):
    if ctx.invoked_subcommand is None:
        pass


@module.command()
@commands.is_owner()
async def reload(ctx, module: str):
    for file_path in Path("./modules").glob("**/*.py"):
        file_path = str(file_path).replace("/", ".")[:-3]
        file_name = file_path.split(".")[-1]
        if file_name != module:
            continue
        try:
            bot.reload_extension(file_path)
        except Exception:
            with open("./errorlogs/error.txt", mode="w") as file:
                file.write(traceback.format_exc())
            with open("./errorlogs/error.txt", mode="rb") as file:
                return await ctx.reply(embed=embed.error(f"Couldn't reload {module}"), file=discord.File("./errorlogs/error.txt"), mention_author=False)
        else:
            return await ctx.reply(embed=embed.success(f"Successfully reloaded {module}"), mention_author=False)
    await ctx.reply(embed=embed.error(f"There is no such module named {module}"), mention_author=False)


@module.command()
@commands.is_owner()
async def load(ctx, module: str):
    for file_path in Path("./modules").glob("**/*.py"):
        file_path = str(file_path).replace("/", ".")[:-3]
        file_name = file_path.split(".")[-1]
        if file_name != module:
            continue
        try:
            bot.load_extension(file_path)
        except Exception:
            with open("./errorlogs/error.txt", mode="w") as file:
                file.write(traceback.format_exc())
            with open("./errorlogs/error.txt", mode="rb") as file:
                return await ctx.reply(embed=embed.error(f"Couldn't load {module}"), file=discord.File("./errorlogs/error.txt"), mention_author=False)
        else:
            return await ctx.reply(embed=embed.success(f"Successfully loaded {module}"), mention_author=False)
    await ctx.reply(embed=embed.error(f"There is no such module named {module}"), mention_author=False)


@module.command()
@commands.is_owner()
async def unload(ctx, module: str):
    for file_path in Path("./modules").glob("**/*.py"):
        file_path = str(file_path).replace("/", ".")[:-3]
        file_name = file_path.split(".")[-1]
        if file_name != module:
            continue
        try:
            bot.unload_extension(file_path)
        except Exception:
            with open("./errorlogs/error.txt", mode="w") as file:
                file.write(traceback.format_exc())
            with open("./errorlogs/error.txt", mode="rb") as file:
                return await ctx.reply(embed=embed.error(f"Couldn't unload {module}"), file=discord.File("./errorlogs/error.txt"), mention_author=False)
        else:
            return await ctx.reply(embed=embed.success(f"Successfully unloaded {module}"), mention_author=False)
    await ctx.reply(embed=embed.error(f"There is no such module named {module}"), mention_author=False)

keep_alive()
bot.run("OTAyNDA1MDg4MTM4NjUzNzI2.YXd8Og.4PwBfKKpjUXIxbKPiM3OoigVOUA")
