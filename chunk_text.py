from typing import List

from langchain_core.documents import Document
from promptflow import tool
from langchain_text_splitters import MarkdownHeaderTextSplitter


@tool
def chunk_text(source_file: str) -> list[Document]:
    file = open(source_file, "r")
    markdown_text = file.read()
    file.close()

    headers_to_split_on = [
        ("#", "Question"),
        ("##", "Header 2"),
    ]

    markdown_splitter = MarkdownHeaderTextSplitter(
        headers_to_split_on=headers_to_split_on,
    )

    docs = markdown_splitter.split_text(markdown_text)

    return docs
