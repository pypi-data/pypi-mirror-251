from datetime import datetime, timedelta
from azure.storage.blob.aio import BlobServiceClient
from azure.storage.blob import BlobType, BlobSasPermissions, generate_blob_sas
import haskellian.asynch as hka
from .. import CONN_STR, KEY
from ..util import with_client

@with_client
async def upload(
    container: str, blob: str, data: str | bytes, overwrite: bool = True,
    *, client: BlobServiceClient, conn_str: str | None = CONN_STR
):
    bc = client.get_blob_client(container=container, blob=blob)
    await bc.upload_blob(data, overwrite=overwrite)

@with_client
async def append(
    container: str, blob: str, data: str | bytes,
    *, client: BlobServiceClient, conn_str: str | None = CONN_STR
):
    bc = client.get_blob_client(container=container, blob=blob)
    await bc.upload_blob(data, blob_type=BlobType.APPENDBLOB)

@with_client
async def download(
    container: str, blob: str,
    *, client: BlobServiceClient, conn_str: str | None = CONN_STR
) -> bytes:
    bc = client.get_blob_client(container=container, blob=blob)
    d = await bc.download_blob()
    return await d.readall()
    
@with_client
async def delete(
    container: str, blobs: str | list[str],
    *, client: BlobServiceClient, conn_str: str | None = CONN_STR
):
    """Delete one or multiple blobs"""
    cc = client.get_container_client(container)
    if isinstance(blobs, str):
        await cc.delete_blob(blobs)
    else:
        await cc.delete_blobs(*blobs)

def url(
    container: str, blob: str, *, account_key: str = KEY,
    client: BlobServiceClient | None = None, conn_str: str | None = CONN_STR,
    expiry: datetime = datetime.now() + timedelta(days=1),
    permission = BlobSasPermissions(read=True)
) -> str:
    assert conn_str is not None or client is not None, "Provide a connection string or a client"
    client = client or BlobServiceClient.from_connection_string(conn_str)
    bc = client.get_blob_client(container, blob)
    token = generate_blob_sas(
        bc.account_name, bc.container_name, bc.blob_name,
        account_key=account_key, expiry=expiry, permission=permission
    )
    return f"{bc.url}?{token}"