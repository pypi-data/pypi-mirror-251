from azure.storage.blob.aio import BlobServiceClient
from .. import CONN_STR
from ..util import with_client

@with_client
async def create(
    container: str, *, client: BlobServiceClient, conn_str: str = CONN_STR
):
    await client.create_container(container)

@with_client
async def delete(
    container: str, *, client: BlobServiceClient, conn_str: str = CONN_STR
):
    await client.delete_container(container)
