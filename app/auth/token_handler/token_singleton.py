from app.auth.token_handler.token_creator import TokenCreator

from environs import Env

env = Env()
env.read_env()

token_creator = TokenCreator(
    token_keys=env("TOKEN_KEYS"),
    exp_time_minutes=int(env("EXP_TIME_MINUTES")),
    refresh_time_minutes=int(env("REFRESH_TIME_MINUTES")),
)
