import re


class Pre_processing:
    MATCH_COMMENTS = r"//.*(?=\n)"

    @staticmethod
    def filter(code: str):
        try:
            return re.sub(Pre_processing.MATCH_COMMENTS, "", code, 0, re.MULTILINE)
        except ValueError:
            return code
