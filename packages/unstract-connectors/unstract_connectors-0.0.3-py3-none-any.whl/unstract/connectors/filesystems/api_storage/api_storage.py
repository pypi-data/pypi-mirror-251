import os

from unstract.connectors.filesystems.minio.minio import MinioFS


class UnstractApiStorage(MinioFS):
    """Api Storage.

    Api Storage through Minio.
    """

    @staticmethod
    def get_id() -> str:
        return "api|6d102906-9f17-4faa-92f0-bdc6bb07e4e1"

    @staticmethod
    def get_name() -> str:
        return "API/HTTP"

    @staticmethod
    def get_description() -> str:
        return "Store and retrieve data on Unstract API Storage"

    @staticmethod
    def get_icon() -> str:
        return "https://storage.googleapis.com/pandora-static/connector-icons/ApiStorage.png"  # noqa

    @staticmethod
    def get_json_schema() -> str:
        f = open(f"{os.path.dirname(__file__)}/static/json_schema.json")
        schema = f.read()
        f.close()
        return schema
