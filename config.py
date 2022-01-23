from utils.suggester import SuggestionBoard
from utils.jsonx import JSONx


class colors:

    success = 0x34c789

    error = 0xff005c

    warning = 0x006aff


class emojis:

    success = "<:success:889206855321157683>"

    error = "<:error:911240678342819870>"

    warning = "<:warning:889206830637666334>"


class channels:

    draft = 934365215418613850

    approved = 934497235457159249

    rejected = 934497248639860756


class roles:

    approvers = [934364031962189824, 934364196953530378]

class internal:

    modules_to_not_load = []


sboard = SuggestionBoard("./jsondb/suggestions.json")
db = JSONx("./jsondb/db.json")
