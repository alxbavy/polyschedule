from typing import Optional

from polyschedule.image_tools.generate_algorythms import IImageGenerateAlgorythm


def generate(day_data, algorythm: IImageGenerateAlgorythm) -> Optional[bytes]:
    if not day_data:
        return None

    return algorythm.generate(day_data)
