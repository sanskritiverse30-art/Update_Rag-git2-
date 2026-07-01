from app.text_chunker import TextChunker


def test_chunk_text_returns_list():
    chunker = TextChunker(chunk_size=50)

    text = (
        "Python is a programming language. "
        "It is widely used in artificial intelligence. "
        "It is also used for web development."
    )

    chunks = chunker.chunk_text(text)

    assert isinstance(chunks, list)
    assert len(chunks) > 0


def test_chunk_text_filters_small_chunks():
    chunker = TextChunker(chunk_size=100)

    text = "Hi."

    chunks = chunker.chunk_text(text)

    assert chunks == []