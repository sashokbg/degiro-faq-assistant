
from langchain_core.documents import Document
from langchain_text_splitters import MarkdownHeaderTextSplitter
from promptflow import tool


@tool
def chunk_text(source_file: str) -> list[Document]:
    file = open(source_file, "r")
    markdown_text = file.read()
    file.close()

    headers_to_split_on = [
        ("#", "title"),
        ("##", "link")
    ]

    markdown_splitter = MarkdownHeaderTextSplitter(
        headers_to_split_on=headers_to_split_on
    )

    docs = markdown_splitter.split_text(markdown_text)

    return docs
