from .application_layer import FrameParser
from .link_layer import InvalidDatasetError, InvalidChecksumError
from .autodetect import autodetect, detect


class Tic:

    @classmethod
    async def create(cls, device_path):
        res = await detect(device_path)
        if not res:
            raise RuntimeError(f'No tic found at {device_path}')
        return cls(*res)

    def __init__(self, link, serial_number=None):
        self.link = link
        self.device_path = link.line.port
        self.serial_number = serial_number
        self.groups = {}
        self.err_count = 0

    @classmethod
    async def discover(cls):
        tics_params = await autodetect()
        return [cls(*p) for p in tics_params]

    async def async_update(self):
        raw_groups = await self._update()
        self.groups = FrameParser(raw_groups).to_dict()
        return self.groups

    async def _update(self):
        self.err_count = 0
        while True:
            try:
                return await self.link.frame()
            except (InvalidDatasetError, InvalidChecksumError):
                self.err_count = self.err_count + 1
