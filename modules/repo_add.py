import discord
import requests
from discord.ext import commands
import config
import os
from utils.embed import embed


class RepoAdd(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.group()
    async def block(self, ctx):
        if ctx.invoked_subcommand is None:
            pass

    @block.command()
    @commands.has_any_role(*config.roles.approvers)
    async def add(self, ctx, member_id: str):
        try:
            int(member_id)
        except ValueError:
            return await ctx.reply(embed=embed.error("Invalid member id"), mention_author=False)
        if len(str(member_id)) != 17:
            return await ctx.reply(embed=embed.error("Invalid member id"), mention_author=False)
        blocked = config.db.get("blocked", default=[])
        if member_id in blocked:
            return await ctx.reply(embed=embed.error("Member already blocked"), mention_author=False)
        blocked.append(member_id)
        config.db.set("blocked", blocked)
        await ctx.reply(embed=embed.success("Member successfully blocked"), mention_author=False)

    @block.command()
    @commands.has_any_role(*config.roles.approvers)
    async def remove(self, ctx, member_id: str):
        try:
            int(member_id)
        except ValueError:
            return await ctx.reply(embed=embed.error("Invalid member id"), mention_author=False)
        if len(str(member_id)) != 17:
            return await ctx.reply(embed=embed.error("Invalid member id"), mention_author=False)
        blocked = config.db.get("blocked", default=[])
        if member_id not in blocked:
            return await ctx.reply(embed=embed.error("Member is not blocked what are you doing"), mention_author=False)
        blocked.remove(member_id)
        config.db.set("blocked", blocked)
        await ctx.reply(embed=embed.success("Member successfully unblocked"), mention_author=False)

    @block.command(name="list")
    @commands.has_any_role(*config.roles.approvers)
    async def _list(self, ctx, member_id: str):
        blocked_members = config.db.get("blocked", default=[])
        descstr = ""
        for member_id in blocked_members:
            descstr += f"{member_id} - <@{member_id}>\n"
        if descstr == "":
            descstr = "*No members blocked*"
        await ctx.reply(embed=embed.success("Successfully fetched the blocked members list", descstr))

    @commands.command()
    async def submit(self, ctx, link: str):
        if not link.startswith("https://github.com/") or link.count("/") != 4:
            return await ctx.reply(embed=embed.error("Invalid repo link supplied", "Links must start with `https://github.com/` and not end with a `/`.\ne.g `https://github.com/mantikafasi/StupidityDBServer`"), mention_author=False)
        elif link in config.internal.get_devlist():
            return await ctx.reply(embed=embed.error("Your link is already in the PluginRepo database"), mention_author=False)
        elif config.sboard.search(link, funnel="?+") != []:
            return await ctx.reply(embed=embed.error("Your link is waiting to be approved or it was approved before"), mention_author=False)
        sID = config.sboard.add_suggestion(link, ctx.author.id)
        channel = ctx.guild.get_channel(config.channels.draft)
        await channel.send(f"Submission: <{link}>\nAuthor: {ctx.author.mention}\n`-submission (approve|reject) {sID}`", allowed_mentions=None)
        return await ctx.reply(embed=embed.success("Link submitted", "Please wait for it to be approved"), mention_author=False)

    @commands.command()
    async def submissions(self, ctx):
        subs = config.sboard.search(funnel="?")
        response_str = ""
        response_list = []
        i = 0
        for sub in subs:
            i += 1
            if i > 10:
                break
            i += 1
            sID = sub["sID"]
            content = sub["content"]
            author_id = sub["author"]
            response_list.append(
                f"sID: `{sID}`\nSubmission: {content}\nAuthor: <@{author_id}>\n")
        if len(response_list) == 0:
            response_str = "*No draft submissions*"
        else:
            response_str = "\n".join(response_list)
        await ctx.reply(embed=embed.success("Successfully fetched the first 10 draft submissions", response_str[:-1]), mention_author=False)

    @commands.group()
    async def submission(self, ctx):
        if ctx.invoked_subcommand is None:
            pass

    @submission.command()
    @commands.has_any_role(*config.roles.approvers)
    async def approve(self, ctx, sID: str):
        sub = config.sboard.search(sid=sID, funnel="?")
        if sub is None:
            return await ctx.reply(embed=embed.error("No such submission"), mention_author=False)
        link = sub["content"]
        if link in config.internal.get_devlist():
            return await ctx.reply(content="<@!287555395151593473> <@!512640455834337290>", embed=embed.error("That link is already in the database???", f"Submission: {link}"), mention_author=False)
        apitoken = os.getenv("apitoken")
        response = requests.get(
            f"https://mantikralligi1.pythonanywhere.com/addDeveloper?token={apitoken}&githuburl={link}").text
        if response != "Success":
            return await ctx.reply(content="<@!287555395151593473> <@!512640455834337290>", embed=embed.error("Server is offline", "Try again later"), mention_author=False)
        config.sboard.approve_suggestion(sID)
        await ctx.reply(embed=embed.success("Submission approved"), mention_author=False)
        sub = config.sboard.search(sid=sID)
        sID = sub["sID"]
        content = sub["content"]
        author_id = sub["author"]
        member = await ctx.guild.fetch_member(author_id)
        try:
            await member.send(embed=embed.success("Your submission has been approved",
                                                  f"Submission: {content}"))
        except (discord.Forbidden, discord.HTTPException):
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
            await member.send(embed=embed.error("Your submission has been rejected",
                                                f"Submission: {content}"))
        except (discord.Forbidden, discord.HTTPException):
            pass
        channel = ctx.guild.get_channel(config.channels.rejected)
        await channel.send(embed=embed.error("Submission rejected", f"sID: `{sID}`\nSubmission: {content}\nAuthor: <@{author_id}>"))


def setup(bot):
    bot.add_cog(RepoAdd(bot))
