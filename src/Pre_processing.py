class Pre_processing:
    @staticmethod
    def filter(code: str):
        return code[:code.index("//")]
