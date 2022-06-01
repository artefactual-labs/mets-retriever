import click

from .mets_retriever import METSRetriever


@click.group()
@click.version_option()
def retriever():
    """METS Retriever CLI tool"""


@retriever.command("fetch-all")
@click.option(
    "--ss-url",
    required=True,
    help="Storage Service host URL",
    default="http://127.0.0.1:62081",
    show_default=True,
)
@click.option(
    "--ss-api-key",
    required=True,
    help="Storage Service API key",
    default="test",
    show_default=True,
)
@click.option(
    "--output-dir",
    required=True,
    help="Path to output directory",
    default="mets_files",
    show_default=True,
)
def get_mets_files(ss_url, ss_api_key, output_dir):
    """Fetch all METS files not already retrieved."""
    retriever = METSRetriever(
        storage_service_url=ss_url,
        storage_service_api_key=ss_api_key,
        output_directory=output_dir,
    )
    retriever.download_all_mets_files()


@retriever.command("fetch-one")
@click.option(
    "--ss-url",
    required=True,
    help="Storage Service host URL",
    default="http://127.0.0.1:62081",
    show_default=True,
)
@click.option(
    "--ss-api-key",
    required=True,
    help="Storage Service API key",
    default="test",
    show_default=True,
)
@click.option(
    "--output-dir",
    required=True,
    help="Path to output directory",
    default="mets_files",
    show_default=True,
)
@click.argument("aip-uuid")
def get_mets_file(ss_url, ss_api_key, output_dir, aip_uuid):
    """Fetch single METS file, even if it's already been retrieved."""
    retriever = METSRetriever(
        storage_service_url=ss_url,
        storage_service_api_key=ss_api_key,
        output_directory=output_dir,
    )
    retriever.download_mets_file(aip_uuid)


if __name__ == "__main__":
    retriever()
