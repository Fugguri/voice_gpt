
class TooLongResponce(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__("openAI responce is too long")
