from dataclasses import dataclass
from typing import List, Union
from environs import Env


@dataclass
class Bot:
    token: str
    admin_ids: List[int]


@dataclass
class Config:
    bot: Bot


def load_config(path: Union[str, None] = None) -> Config:
    env = Env()
    env.read_env(path)
    return Config(Bot(env('BOT_TOKEN'), env('ADMIN_IDS')))