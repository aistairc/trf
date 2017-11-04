from typing import List


class Chunk(object):

    def __init__(self, chunk_id: int, link: int, description: str):

        self.chunk_id = chunk_id
        self.link = link
        self.description = description
