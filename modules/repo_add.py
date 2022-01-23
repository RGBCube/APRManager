import discord
from discord.ext import commands
import config
from utils.embed import embed


class RepoAdd(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.group()
    async def submission(ctx):
        if ctx.invoked_subcommand is None:
            pass

    @commands.command()
    async def submit(self, ctx, link: str):
        if not link.startswith("https://github.com/") or link.count("/") != 4:
            return await ctx.reply(embed=embed.error("Invalid repo link supplied", "Links must start with `https://github.com/` and not end with a `/`.\ne.g `https://github.com/mantikafasi/StupidityDBServer`"), mention_author=False)
        elif config.sboard.search(link, funnel="?+") == []:
            sID = config.sboard.add_suggestion(link, ctx.author.id)
            channel = ctx.guild.get_channel(config.channels.draft)
            await channel.send(f"Submission: <{link}>\nAuthor: {ctx.author.mention}\n`-submission (approve|reject) {sID}`")
            return await ctx.reply(embed=embed.success("Link submitted", "Please wait for it to be approved"), mention_author=False)
        await ctx.reply(embed=embed.error("Your link is waiting to be approved or it was approved before"), mention_author=False)

    @commands.command()
    async def submissions(self, ctx):
        subs = config.sboard.search(funnel="?")
        response_str = ""
        response_list = []
        for sub in subs:
            sID = sub["sID"]
            content = sub["content"]
            author_id = sub["author"]
            response_list.append(
                f"sID: `{sID}`\nSubmission: {content}\nAuthor: <@{author_id}>\n")
        if len(response_list) == 0:
            response_str = "*No draft submissions*"
        else:
            response_str = "\n".join(response_list)
        await ctx.reply(embed=embed.success("Successfully fetched all draft submissions", response_str[:-1]))

    @submission.command()
    @commands.has_any_role(*config.roles.approvers)
    async def approve(self, ctx, sID: str):
        if config.sboard.search(sid=sID, funnel="?") is None:
            return await ctx.reply(embed=embed.error("No such submission"), mention_author=False)
        config.sboard.approve_suggestion(sID)
        # sends the link to the db
        await ctx.reply(embed=embed.success("Submission approved"), mention_author=False)
        sub = config.sboard.search(sid=sID)
        sID = sub["sID"]
        content = sub["content"]
        author_id = sub["author"]
        member = await ctx.guild.fetch_member(author_id)
        try:
            member.send(embed=embed.success("Your submission has been approved",
                        f"Submission: " + config.sboard.search(sID)["content"]))
        except:
            pass
        channel = ctx.guild.get_channel(config.channels.approved)
        await channel.send(embed=embed.success("Submission approved", f"sID: `{sID}`\nSubmission: {content}\nAuthor: <@{author_id}>"))

    @submission.command()
    @commands.has_any_role(*config.roles.approvers)
    async def reject(self, ctx, sID: str):
        if config.sboard.search(sid=sID, funnel="?") is None:
            return await ctx.reply(embed=embed.error("No such submission"), mention_author=False)
        config.sboard.reject_suggestion(sID)
        await ctx.reply(embed=embed.success("Submission rejected"), mention_author=False)
        sub = config.sboard.search(sid=sID)
        sID = sub["sID"]
        content = sub["content"]
        author_id = sub["author"]
        member = await ctx.guild.fetch_member(author_id)
        try:
            member.send(embed=embed.error("Your submission has been rejected",
                        f"Submission: " + config.sboard.search(sID)["content"]))
        except:
            pass
        channel = ctx.guild.get_channel(config.channels.rejected)
        await channel.send(embed=embed.error("Submission rejected", f"sID: `{sID}`\nSubmission: {content}\nAuthor: <@{author_id}>"))


def setup(bot):
    bot.add_cog(RepoAdd(bot))
