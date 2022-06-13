import os

import pytest

from mets_retriever import mets_retriever


@pytest.fixture
def retriever():
    """Return METSRetriever instance with newly-initalized database."""
    if os.path.exists(mets_retriever.DATABASE_FILE):
        os.remove(mets_retriever.DATABASE_FILE)
    retriever = mets_retriever.METSRetriever()
    return retriever
