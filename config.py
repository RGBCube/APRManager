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

    draft = 934765555238449162

    approved = 934765607793098762

    rejected = 934765633441239111


class roles:

    approvers = [934773705970700328]

class internal:

    modules_to_not_load = []


sboard = SuggestionBoard("./jsondb/suggestions.json")
db = JSONx("./jsondb/db.json")
