import pytest
from utils import extract_google_doc_link

def test_extract_google_doc_link():
    content = "I have created the doc: https://docs.google.com/document/d/1abc123/edit"
    link = extract_google_doc_link(content)
    assert link == "/document/d/1abc123/edit"

def test_extract_google_doc_link_none():
    content = "No link here"
    link = extract_google_doc_link(content)
    assert link is None

def test_extract_google_doc_link_malformed():
    content = "Check https://docs.google.com without path"
    link = extract_google_doc_link(content)
    assert link is None
