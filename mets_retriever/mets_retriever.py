import logging
import os
import sys

import sqlalchemy
from amclient import AMClient
from sqlalchemy.ext.declarative import declarative_base

MODULE_NAME = "mets_retriever" if __name__ == "__main__" else __name__
logger = logging.getLogger(MODULE_NAME)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler(stream=sys.stdout)
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)

THIS_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE_FILE = os.path.join(THIS_DIR, "mets.db")

API_FILE_PREFIX = "/api/v2/file/"

Base = declarative_base()


class AIP(Base):
    __tablename__ = "aips"
    id = sqlalchemy.Column("aip_id", sqlalchemy.Integer, primary_key=True)
    uuid = sqlalchemy.Column(sqlalchemy.String(120))

    def __repr__(self):
        return "<AIP(id={s.id}, uuid={s.uuid}>".format(s=self)


class METSRetriever:
    def __init__(
        self,
        storage_service_url="http://127.0.0.1:62081",
        storage_service_api_key="test",
        storage_service_username="test",
        output_directory="mets_files",
        add_sidecar=False,
    ):
        self.storage_service_url = storage_service_url
        self.storage_service_api_key = storage_service_api_key
        self.storage_service_username = storage_service_username
        self.output_directory = os.path.abspath(output_directory)
        self.add_sidecar = add_sidecar

        self.init_db()

    def init_db(self):
        if not os.path.isfile(DATABASE_FILE):
            # Create database file if it does not exist already
            with open(DATABASE_FILE, "a"):
                pass
        engine = sqlalchemy.create_engine(
            "sqlite:///{}".format(DATABASE_FILE), echo=False
        )
        Session = sqlalchemy.orm.sessionmaker(bind=engine)
        Base.metadata.create_all(engine)
        self.session = Session()

    def check_if_aip_in_database(self, uuid):
        """Check if AIP in database and return boolean."""
        matching_aip = self.session.query(AIP).filter_by(uuid=uuid).first()
        return matching_aip is not None

    def add_aip_to_database(self, uuid):
        """Add AIP UUID to database."""
        aip = AIP(uuid=uuid)
        self.session.add(aip)
        self.session.commit()

    def _verify_download(self, expected_path):
        """Raise OSError if file doesn't exist at expected path."""
        if not os.path.isfile(expected_path):
            raise OSError("METS file not found at expected path after downloading")

    def _get_replica_locations(self, replicas):
        """Return list of AIP replica locations."""
        replica_locations = []
        for replica in replicas:
            uuid = replica.replace(API_FILE_PREFIX, "").rstrip("/")
            am = AMClient(
                ss_url=self.storage_service_url,
                ss_user_name=self.storage_service_username,
                ss_api_key=self.storage_service_api_key,
                package_uuid=uuid,
            )
            details = am.get_package_details()
            if details.get("current_location"):
                replica_locations.append(details.get("current_location"))
        return replica_locations

    def write_sidecar_file(self, uuid):
        """Write sidecar file containing information not in METS.

        This file will have the same name as the METS file but with a .txt
        extension and is written next to the METS file in the output directory.
        """
        am = AMClient(
            ss_url=self.storage_service_url,
            ss_user_name=self.storage_service_username,
            ss_api_key=self.storage_service_api_key,
            package_uuid=uuid,
        )
        details = am.get_package_details()
        location_uuid = details.get("current_location")
        replicas = details.get("replicas")
        replica_locations = self._get_replica_locations(replicas)

        sidecar_file = os.path.join(self.output_directory, f"METS.{uuid}.txt")
        with open(sidecar_file, "w") as sidecar:
            sidecar.write(
                "Storage location: {}\nAIP replicas: {}\nAIP replica storage locations: {}\n".format(
                    location_uuid, ", ".join(replicas), ", ".join(replica_locations)
                )
            )

    def download_mets_file(self, uuid):
        """Download METS file with given UUID to self.output_directory."""
        am = AMClient(
            ss_url=self.storage_service_url,
            ss_user_name=self.storage_service_username,
            ss_api_key=self.storage_service_api_key,
        )
        am.aip_uuid = uuid
        am.directory = self.output_directory

        if not os.path.exists(self.output_directory):
            os.makedirs(self.output_directory)

        am.extract_aip_mets_file()

        self._verify_download(os.path.join(self.output_directory, f"METS.{uuid}.xml"))

        if self.add_sidecar:
            self.write_sidecar_file(uuid)

        logger.info(f"Downloaded METS file METS.{uuid}.xml")

    def _filter_aips(self, aips):
        """Return only original AIPs (no replicas) with status UPLOADED."""
        return [
            aip
            for aip in aips
            if aip["status"] == "UPLOADED" and aip["replicated_package"] is None
        ]

    def download_all_mets_files(self, with_replicas_only=False):
        am = AMClient(
            ss_url=self.storage_service_url,
            ss_user_name=self.storage_service_username,
            ss_api_key=self.storage_service_api_key,
        )
        aips = self._filter_aips(am.aips())
        for aip in aips:
            if with_replicas_only and not aip.get("replicas"):
                continue

            aip_uuid = aip["uuid"]
            if not self.check_if_aip_in_database(aip_uuid):
                try:
                    self.download_mets_file(aip_uuid)
                    self.add_aip_to_database(aip_uuid)
                except OSError as err:
                    logger.error(
                        f"Unable to download METS file for AIP with UUID {aip_uuid}: {err}"
                    )
