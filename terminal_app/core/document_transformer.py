from pathlib import Path
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from pypdf import PdfReader

from terminal_app.base import BaseOptions
from .cycle_functions import app_input


def read_file(file_path: Path) -> str:
    assert file_path.exists(), "File don't exist"
    with open(file_path, "r") as file:
        return file.read()


def test_transformer(file_path: Path) -> list[str]:
    file_data: str = read_file(file_path)

    tmp: str = ""

    for row in file_data.split("\n"):
        if not (row.startswith("#") or row.startswith("[[")):
            tmp += row + "\n"

    return tmp.split("\n\n")


def test2_transformer(file_path: Path) -> list[str]:
    file_data: str = read_file(file_path)

    return file_data.split("\n\n")


def create_splitter() -> RecursiveCharacterTextSplitter:
    chunk = app_input("Enter chunk: ")
    try:
        chunk = int(chunk)
    except:
        chunk = 1000
    chunk_overlap = app_input("Enter chunk_overlap: ")
    try:
        chunk_overlap = int(chunk_overlap)
    except:
        chunk_overlap = 200

    return RecursiveCharacterTextSplitter(
        chunk_size=chunk,
        chunk_overlap=chunk_overlap,
        length_function=len,
        is_separator_regex=False,
    )


def recursive(file_path: Path) -> list[str]:
    file_data: str = read_file(file_path)
    splitter = create_splitter()
    return splitter.split_text(file_data)


def pdf(file_path: Path) -> list[str]:
    interval = app_input("Enter interval (ex [0:100]): ")
    try:
        s, e = map(int, interval.split(":"))
    except:
        return []
    splitter = create_splitter()
    loader = PdfReader(file_path)
    docs = [Document(page.extract_text()) for page in loader.pages[s:e]]
    return [doc.page_content for doc in splitter.split_documents(docs)]


class DocumentTransformerOptions(BaseOptions):
    TEST1_TRANSFORMER = "t1", test_transformer
    TEST2_TRANSFORMER = "t2", test2_transformer
    RECURSIVE = "tr", recursive
    PDF = "pdf", pdf
