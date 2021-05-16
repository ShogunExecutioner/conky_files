from os import environ
from os.path import abspath, dirname, expanduser, isfile
from shutil import copyfileobj
from loguru import logger
import requests
from pyowm import OWM

env_file = f"{abspath(dirname(__file__))}/.env"
if isfile(env_file):
    with open(env_file) as file:
        for line in file.readlines():
            key, value = line.split("=", maxsplit=1)
            environ[key] = value

API_KEY = environ.get("OWM_API_KEY")
CITY_ID = int(environ.get("OWM_CITY_ID"))
DATA_PATH = f'{expanduser("~")}/.conky/weather'


@logger.catch()
def get_data(key: str):
    owm = OWM(key)
    weather_manager = owm.weather_manager()
    logger.debug(weather_manager.one_call(31.1061, 30.6398))
    return
    weather_data = weather_manager.weather_at_id(CITY_ID)
    logger.info(weather_data)
    # weather_data = owm.weather_at_id(CITY_ID).get_weather()
    download_img(
        f"http://openweathermap.org/img/wn/{weather_data.get_weather_icon_name()}@2x.png"
    )
    return weather_data


@logger.catch()
def download_img(icon_url: str):
    r = requests.get(icon_url, stream=True, timeout=10)
    if r.status_code == 200:
        with open(f"{DATA_PATH}/icon.png", "wb") as file:
            r.raw.decode_content = True
            copyfileobj(r.raw, file)


@logger.catch()
def main():
    weather_data = get_data(API_KEY)
    if weather_data:
        with open(f"{DATA_PATH}/data", "w") as final_file:
            final_file.write(
                f"{weather_data.get_temperature(unit='celsius')['temp']:.0f}\n"
            )
            final_file.write(f"{weather_data.get_wind()['speed']*3.6:.1f}\n")
            final_file.write(f"{weather_data.get_humidity()}%")


if __name__ == "__main__":
    r = requests.get(
        f"https://api.openweathermap.org/data/2.5/weather?q=London&appid={API_KEY}"
    )
    print(r.text)
    # main()
