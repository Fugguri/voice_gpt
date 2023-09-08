from dataclasses import dataclass
    
@dataclass
class User:
    id:int
    user_id:int
    username:str
    full_name:str
    has_access:bool
    