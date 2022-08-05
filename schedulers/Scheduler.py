from abc import ABC
from typing import List

from output_streams.IOutputStream import IOutputStream


class Scheduler(ABC):
    def __init__(self, output_streams: List[IOutputStream], *args, **kwargs):
        self.output_streams = output_streams

    async def schedule_to_output_stream(self, message: str, image_path: str):
        raise NotImplementedError
