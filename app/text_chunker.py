import re


class TextChunker:
    def __init__(self, chunk_size: int = 500, min_chunk_length: int = 30):
        self.chunk_size = chunk_size
        self.min_chunk_length = min_chunk_length

    def chunk_text(self, text: str) -> list[str]:
        sentences = re.split(r'(?<=[.!?])\s+', text)

        chunks = []
        current = ""

        for sentence in sentences:
            if len(current) + len(sentence) < self.chunk_size:
                current += " " + sentence
            else:
                if current.strip():
                    chunks.append(current.strip())
                current = sentence

        if current.strip():
            chunks.append(current.strip())

        return [
            chunk.strip()
            for chunk in chunks
            if len(chunk.strip()) >= self.min_chunk_length
        ]