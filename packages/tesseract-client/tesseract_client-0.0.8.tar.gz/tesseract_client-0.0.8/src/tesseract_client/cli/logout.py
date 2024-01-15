from loguru import logger

from tesseract_client.config import delete_credentials, clean_up, NoCredentialsError


def logout():
    """Deletes the credentials from the config file and keyring and cleans up the file system"""
    try:
        clean_up()
    except FileNotFoundError:
        pass

    try:
        delete_credentials()
    except NoCredentialsError:
        logger.info("You are not logged in")
        return

    logger.info("Logged out")
