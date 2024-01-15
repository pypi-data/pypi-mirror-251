import getpass
from loguru import logger

from tesseract_client.config import store_credentials, get_config, clean_up
from tesseract_client.api_manager import APIManager, API_URL


def login(username: str = None, password: str = None):
    """Validate and store the username and password in the config file and keyring"""
    if username is None:
        username = input("Username: ")
    if password is None:
        password = getpass.getpass("Password: ")

    _, _, api_url = get_config()
    api_manager = APIManager(
        username=username, password=password, api_urls=API_URL(api_url)
    )
    try:
        api_manager.login()
        logger.info(f"Logged in as {username}")
    except Exception as e:
        logger.info(e)
        return

    try:
        clean_up()
    except FileNotFoundError:
        pass

    store_credentials(username, password)
