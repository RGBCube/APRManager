import config
import discord


class embed:

    @staticmethod
    def success(title: str, description: str = ""):
        emoji, color = config.emojis.success, config.colors.success
        return discord.Embed(
            title=f"{emoji} {title}", description=description, color=color)

    @staticmethod
    def error(title: str, description: str = ""):
        emoji, color = config.emojis.error, config.colors.error
        return discord.Embed(
            title=f"{emoji} {title}", description=description, color=color)

    @staticmethod
    def warning(title: str, description: str = ""):
        emoji, color = config.emojis.warning, config.colors.warning
        return discord.Embed(
            title=f"{emoji} {title}", description=description, color=color)
