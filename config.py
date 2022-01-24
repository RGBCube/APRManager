from utils.suggester import SuggestionBoard
from utils.jsonx import JSONx
import requests
import json


class colors:

    success = 0x34c789

    error = 0xff005c

    warning = 0x006aff


class emojis:

    success = "<:success:889206855321157683>"

    error = "<:error:911240678342819870>"

    warning = "<:warning:889206830637666334>"


class channels:

    draft = 934765555238449162

    approved = 934765607793098762

    rejected = 934765633441239111


class roles:

    approvers = [934773705970700328]

class internal:

    modules_to_not_load = []

    @staticmethod
    def get_devlist():
        devdict = requests.get("https://mantikralligi1.pythonanywhere.com/getDevelopers").text
        try:
            devdict = json.loads(devdict)
        except:
            return None
        devlist = []
        for dev_raw in devdict:
            dev_name, repo_name = dev_raw["github_username"], dev_raw["plugins_repo_name"]
            devlist.append(f"https://github.com/{dev_name}/{repo_name}")
        return devlist
    
    @staticmethod
    def is_blocked(member_id: (str)):
        return member_id in db.get("blocked", default=[])


sboard = SuggestionBoard("./jsondb/suggestions.json")
db = JSONx("./jsondb/db.json")
