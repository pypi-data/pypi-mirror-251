

import os
from pathlib import Path
import tempfile
from src.foxlator.sub_movie_generator import SubMovieGenerator
from utils.base import TestBase
from contextlib import contextmanager
import numpy as np
from unittest.mock import MagicMock, patch
from moviepy.editor import VideoClip  # type: ignore
from moviepy.audio.AudioClip import AudioArrayClip  # type: ignore


class SubtitleTests(TestBase):

    @contextmanager
    def _create_video_with_audio_file(self):
        width = 640
        height = 480
        duration = 2
        fps = 24
        rate = 44100
        data_stereo = np.random.uniform(-1, 1, (rate*duration, 2))
        random_frame = np.random.randint(  # type: ignore
            0, 256, size=(height, width, 3), dtype=np.uint8)
        video_clip = VideoClip(lambda _: random_frame,  # type: ignore
                               duration=duration)
        audio_clip = AudioArrayClip(data_stereo, fps=rate)
        video_clip: VideoClip = video_clip.set_audio(
            audio_clip)
        with tempfile.NamedTemporaryFile(suffix=".mp4") as temp_file:
            temp_path = str(temp_file.name)
            video_clip.write_videofile(
                temp_path, codec="libx264", audio_codec="aac", fps=fps)
            yield Path(temp_path)

    def test_gen_movie_with_subtitle_should_be_created(self):
        with self._create_video_with_audio_file() as video_file:
            with tempfile.NamedTemporaryFile(suffix=".mp4") as temp_file:
                try:
                    gen_movie_path = SubMovieGenerator(
                        video_file, 'tiny').gen_movie_with_subtitles(Path(str(temp_file.name)))
                    self.assertTrue(os.path.exists(gen_movie_path))
                except Exception as e:
                    self.fail(f"Unexpected exception: {e}")

    @patch('src.foxlator.utils.checks.is_ffmpeg_installed', return_value=False)
    def test_gen_movie_with_subtitle_no_ffmpeg_installed(self, _: MagicMock):
        from src.foxlator.sub_movie_generator import SubMovieGenerator  # type: ignore

    @patch('src.foxlator.utils.checks.is_imagemagick_installed', return_value=False)
    def test_gen_movie_with_subtitle_no_imagemagick_installed(self, _: MagicMock):
        from src.foxlator.sub_movie_generator import SubMovieGenerator  # type: ignore
