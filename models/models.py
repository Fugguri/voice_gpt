from dataclasses import dataclass
    
@dataclass
class User:
    id:int
    user_id:int
    username:str
    full_name:str
    has_access:bool
    

@dataclass
class Character:
    id:int
    name:str
    description:str
    role_settings:str
    voice_id:int
    use_count:int
    