from typing import Optional

from polyschedule.image_tools.generate_algorythms import IImageGenerateAlgorythm


def generate(day_data: dict, algorythm: IImageGenerateAlgorythm) -> bytes:
    return algorythm.generate(day_data)
