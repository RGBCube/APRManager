import discord
import traceback
import sys
import config
from utils.embed import embed
from discord.ext import commands


class CommandErrorHandler(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if hasattr(ctx.command, 'on_error'):
            return
        cog = ctx.cog
        if cog:
            if cog._get_overridden_method(cog.cog_command_error) is not None:
                return
        ignored = (commands.CommandNotFound, commands.DisabledCommand)
        error = getattr(error, 'original', error)
        if isinstance(error, ignored):
            return
        elif isinstance(error, commands.NoPrivateMessage):
            try:
                await ctx.reply(embed=embed.error(f'You cannot use this command in DMs'), mention_author=False)
            except (discord.HTTPException, discord.Forbidden):
                pass
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.reply(embed=embed.error("Please give all the required arguments"), mention_author=False)
        elif isinstance(error, commands.MissingAnyRole):
            await ctx.reply(embed=embed.error("You cannot use this command"), mention_author=False)
        else:
            print('Ignoring exception in command {}:'.format(ctx.command), file=sys.stderr)
            traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)


def setup(bot):
    bot.add_cog(CommandErrorHandler(bot))
