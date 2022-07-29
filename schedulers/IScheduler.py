class IScheduler:
    async def schedule_to_output_stream(self, message: str, image_path: str):
        raise NotImplementedError
