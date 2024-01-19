import subprocess
import logging
from typing import Optional


def check_if_installed(app_name: str, verify_command: str, is_required: Optional[bool] = False):
    try:
        subprocess.run(verify_command.split(), check=True,
                       stdout=subprocess.PIPE,)
        return True
    except FileNotFoundError:
        if is_required:
            logging.error(
                f'{app_name} is not installed. This tool is required.')
        else:
            logging.warning(
                f'{app_name} is not installed.')
        logging.error(
            f'Please install {app_name} manually: https://ffmpeg.org/download.html')
        return False
