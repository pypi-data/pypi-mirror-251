from .system import check_if_installed


def is_ffmpeg_installed():
    return check_if_installed("ffmpeg", "ffmpeg -version", True)


def is_imagemagick_installed():
    return check_if_installed("imagemagick", "convert -version", True)
