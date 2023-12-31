import os

class Pager:
    def __init__(
        self,
        file_name: str,
        page_size: int = 4096,
    ):
        self.file_name = file_name
        self.page_size = page_size

    def get_page(
        self,
        page_number: int,
    ) -> bytes:
        with open(self.file_name, 'rb+') as file:
            file.seek(self.get_offset(page_number))
            return file.read(self.page_size)

    def write_page(
        self,
        page_number: int,
        data: bytes,
    ):
        # create the file if it doesn't exist
        if not os.path.exists(self.file_name):
            with open(self.file_name, 'w'):
                pass

        with open(self.file_name, 'rb+') as file:
            file.seek(self.get_offset(page_number))
            file.write(data)

    def get_offset(
        self,
        page_number: int,
    ):
        return (page_number - 1) * self.page_size

class MemoryPager:
    def __init__(
        self,
        page_size: int = 4096,
    ):
        self.page_size = page_size
        self.pages = {}

    def get_page(
        self,
        page_number: int,
    ) -> bytes:
        if page_number not in self.pages:
            self.pages[page_number] = self.new_page()
        return self.pages[page_number]

    def write_page(
        self,
        page_number: int,
        data: bytes,
    ):
        self.pages[page_number] = data

    def new_page(self) -> bytes:
        return bytes([0x00] * self.page_size)
