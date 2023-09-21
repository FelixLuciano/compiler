class Pre_processing:
    @staticmethod
    def filter(code: str):
        try:
            return code[:code.index("//")]
        except ValueError:
            return code
