from minio import Minio

client = Minio(
    "localhost:9000",
    access_key="minioadmin",
    secret_key="minioadmin",
    secure=False
)

def download_file(bucket_name, object_name, local_file_path):
    client.fget_object(bucket_name, object_name, local_file_path)