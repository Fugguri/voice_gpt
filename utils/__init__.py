from .fdftext_to_speech import *
from .speech_to_text import *
from ._openai import *
from .text_to_speech import *
from .texts import Texts
create_text = Texts()
__all__ = [
    "speech_to_text",
    "convert_to_audio",
    "create_responce",
    "text_to_speech",
    'create_text'
]
