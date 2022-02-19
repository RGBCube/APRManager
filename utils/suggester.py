import os
import string
import json
import random


class Error(Exception):
    pass


class NoSuchSuggestion(Error):
    pass


class SuggestionAlreadyApproved(Error):
    pass


class SuggestionWasApprovedBefore(Error):
    pass


class SuggestionAlreadyRejected(Error):
    pass


class SuggestionWasRejectedBefore(Error):
    pass


class Utils:

    @staticmethod
    def validate_json(path_to_json: str):
        if (
            os.path.isfile(path_to_json)
            and os.path.getsize(path_to_json) == 0
            or not os.path.isfile(path_to_json)
        ):
            with open(path_to_json, "w") as json_file:
                json.dump({}, json_file)

    @staticmethod
    def generate_random(randstr, *, length: int, exclude: list = []):
        rand = ''.join(random.choices(randstr, k=length))
        if rand in exclude:
            return Utils.generate_random(randstr, length=length, exclude=exclude)
        return rand


class SuggestionBoard:

    def __init__(self, path_to_json: str):
        self.path_to_json = path_to_json
        self.utils = Utils

    def add_suggestion(self, content: str, author: int):
        """
        Creates a suggestion in the draft category.
        Will return the suggestions sID.
        1234567890: {"content": content, "author": author}
        """
        self.utils.validate_json(self.path_to_json)
        with open(self.path_to_json, mode="r") as json_file:
            json_data = json.load(json_file)
        draft = json_data.get("draft", {})
        all_suggestions = {
            **draft, **json_data.get("approved", {}), **json_data.get("rejected", {})}
        sID = self.utils.generate_random(
            string.digits, length=10, exclude=list(all_suggestions.keys()))
        draft.update({sID: {"content": content, "author": author}})
        json_data["draft"] = draft
        with open(self.path_to_json, mode="w") as json_file:
            json.dump(json_data, json_file, indent=4)
        return sID

    def approve_suggestion(self, sID: str):
        """
        Moves a suggestion from the draft category to the approved category.
        Will raise:
            NoSuchSuggestion: if there is not a suggestion with that sID.
            SuggestionAlreadyApproved: if the suggestion was already approved.
            SuggestionWasRejectedBefore: if the suggestion was rejected earlier.
        """
        self.utils.validate_json(self.path_to_json)
        with open(self.path_to_json, mode="r") as json_file:
            json_data = json.load(json_file)
        draft, approved, rejected = json_data.get("draft", {}), json_data.get(
            "approved", {}), json_data.get("rejected", {})
        if sID in draft.keys():
            suggestion = draft.pop(sID)
            approved = json_data.get("approved", {})
            approved.update({sID: suggestion})
            json_data["approved"] = approved
            with open(self.path_to_json, mode="w") as json_file:
                json.dump(json_data, json_file, indent=4)
        elif sID in approved.keys():
            raise SuggestionAlreadyApproved("Suggestion was approved before.")
        elif sID in rejected.keys():
            raise SuggestionWasRejectedBefore(
                "Suggestion was rejected before.")
        else:
            raise NoSuchSuggestion(f"No suggestion matches the sID '{sID}'.")

    def reject_suggestion(self, sID: str):
        """
        Moves a suggestion from the draft category to the rejected category.
        Will raise:
            NoSuchSuggestion: if there is not a suggestion with that sID.
            SuggestionAlreadyRejected: if the suggestion was already rejected.
            SuggestionWasApprovedBefore: if the suggestion was approved earlier.
        """
        self.utils.validate_json(self.path_to_json)
        with open(self.path_to_json, mode="r") as json_file:
            json_data = json.load(json_file)
        draft, approved, rejected = json_data.get("draft", {}), json_data.get(
            "approved", {}), json_data.get("rejected", {})
        if sID in draft.keys():
            suggestion = draft.pop(sID)
            rejected = json_data.get("rejected", {})
            rejected.update({sID: suggestion})
            json_data["rejected"] = rejected
            with open(self.path_to_json, mode="w") as json_file:
                json.dump(json_data, json_file, indent=4)
        elif sID in rejected.keys():
            raise SuggestionAlreadyRejected("Suggestion was rejected before.")
        elif sID in approved.keys():
            raise SuggestionWasRejectedBefore(
                "Suggestion was apoproved before.")
        else:
            raise NoSuchSuggestion(f"No suggestion matches the sID '{sID}'.")

    def search(self, *args, **kwargs):
        """
        kwargs:
            sid:
                If this kwarg is given, it will return the suggestion with the sID while ignoring all other args and kwargs except funnel
            funnel:
                Filters suggestions by its status.
                ?: draft, +: approved, -: rejected.
            author:
                Filters suggestions by its author.
        args:
            Filters suggestions if all of the args are in the suggestions content.

        """
        self.utils.validate_json(self.path_to_json)
        with open(self.path_to_json, mode="r") as json_file:
            json_data = json.load(json_file)
        funnel = kwargs.get("funnel", "?+-")  # +approved -rejected ?draft
        sID = kwargs.get("sid", None)
        author = kwargs.get("author", None)
        draft, approved, rejected = json_data.get("draft", {}), json_data.get(
            "approved", {}), json_data.get("rejected", {})
        if sID is not None:
            all_suggestions = {}
            to_funnel = {"?": draft, "+": approved, "-": rejected}
            for symbol, value_ in to_funnel.items():
                if symbol in funnel:
                    all_suggestions.update(value_)
            sub = all_suggestions.get(sID)
            if sub is not None:
                sub["sID"] = sID
            return sub
        suggestions_list = []
        for section, symbol in [(draft, "?"), (approved, "+"), (rejected, "+")]:
            if symbol not in funnel:
                continue
            suggestions_list.extend(
                {"sID": sID, **value}
                for sID, value in section.items()
                if all(arg in value.get("content", "") for arg in args)
                and (author is None or value["author"] == author)
            )

        return suggestions_list
