import os

import pytest

from mets_retriever import mets_retriever

AIP_UUID = "8c09cd9f-0da3-4bdb-be2a-2295ed799f4c"


def test_init_db(retriever):
    """Test that database is created and session set."""
    assert os.path.isfile(mets_retriever.DATABASE_FILE)
    assert retriever.session is not None


def test_database_helpers(retriever):
    assert retriever.check_if_aip_in_database(AIP_UUID) is False
    retriever.add_aip_to_database(AIP_UUID)
    assert retriever.check_if_aip_in_database(AIP_UUID) is True


def test_download_mets_file(retriever, mocker):
    extract_mets = mocker.patch("amclient.AMClient.extract_aip_mets_file")
    mocker.patch("mets_retriever.METSRetriever._verify_download")

    retriever.download_mets_file(AIP_UUID)
    extract_mets.assert_called_once()


def test_download_mets_file_verify_failed(retriever, mocker):
    mocker.patch("amclient.AMClient.extract_aip_mets_file")

    with pytest.raises(OSError):
        retriever.download_mets_file(AIP_UUID)
