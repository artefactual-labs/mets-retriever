import os
import tempfile

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


@pytest.mark.parametrize(
    "package_details, expected_output",
    [
        # Test with multiple AIP replicas.
        (
            {
                "current_location": "/api/v2/location/0c2be2cf-02b8-48ab-b264-75aef504289e/",
                "replicas": [
                    "/api/v2/file/2674e2c5-95a4-4058-b453-66983e47144d/",
                    "/api/v2/file/75426ade-38df-4736-a457-b219e5cadb3b/",
                ],
            },
            "Storage location: /api/v2/location/0c2be2cf-02b8-48ab-b264-75aef504289e/\nAIP replicas: /api/v2/file/2674e2c5-95a4-4058-b453-66983e47144d/, /api/v2/file/75426ade-38df-4736-a457-b219e5cadb3b/\n",
        ),
        # Test with one AIP replica.
        (
            {
                "current_location": "/api/v2/location/0c2be2cf-02b8-48ab-b264-75aef504289e/",
                "replicas": ["/api/v2/file/2674e2c5-95a4-4058-b453-66983e47144d/"],
            },
            "Storage location: /api/v2/location/0c2be2cf-02b8-48ab-b264-75aef504289e/\nAIP replicas: /api/v2/file/2674e2c5-95a4-4058-b453-66983e47144d/\n",
        ),
        # Test with no replicas.
        (
            {
                "current_location": "/api/v2/location/0c2be2cf-02b8-48ab-b264-75aef504289e/",
                "replicas": [],
            },
            "Storage location: /api/v2/location/0c2be2cf-02b8-48ab-b264-75aef504289e/\nAIP replicas: \n",
        ),
    ],
)
def test_write_sidecar_file(mocker, package_details, expected_output):
    get_package_details = mocker.patch("amclient.AMClient.get_package_details")
    get_package_details.return_value = package_details

    with tempfile.TemporaryDirectory() as output_dir:
        retriever = mets_retriever.METSRetriever(output_directory=output_dir)
        retriever.write_sidecar_file("test-uuid")

        sidecar_filepath = os.path.join(output_dir, "METS.test-uuid.txt")
        with open(sidecar_filepath, "r") as sidecar_file:
            assert sidecar_file.read() == expected_output


def test_download_mets_file(retriever, mocker):
    extract_mets = mocker.patch("amclient.AMClient.extract_aip_mets_file")
    mocker.patch("mets_retriever.METSRetriever._verify_download")

    retriever.download_mets_file(AIP_UUID)
    extract_mets.assert_called_once()


def test_download_mets_file_verify_failed(retriever, mocker):
    mocker.patch("amclient.AMClient.extract_aip_mets_file")

    with pytest.raises(OSError):
        retriever.download_mets_file(AIP_UUID)
