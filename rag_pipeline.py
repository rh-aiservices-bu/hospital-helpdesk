"""
RAG Ingestion Pipeline
======================
This script defines and runs a Kubeflow Pipeline that ingests documents
into a Llama Stack vector store for Retrieval-Augmented Generation (RAG).

The pipeline has two steps:
  1. create_vector_store        — creates a new vector store in Milvus, or reuses the existing one if VECTOR_STORE_NAME = ""
  2. upload_and_index_documents — lists ALL files in the S3 bucket, downloads each one, uploads it
                                  to the Llama Stack file service, and adds it to the vector store

After the pipeline completes, note the vector store ID printed in the run logs.
You will need it in the next step: 2_rag.ipynb

Prerequisites:
  - The 'data' S3 bucket must exist and contain your documents (e.g. pavilion_regulations.pdf).
    Apply setup/setup-s3.yaml to create the bucket and upload the files automatically.
  - The 'data-connection-data' Secret must exist in your namespace (also created by the setup job).
    In your workbench, attach it as a data connection so the AWS_* env vars are available.
"""

import os

from kfp import dsl, compiler
from kfp.client import Client

# ─────────────────────────────────────────────────────────────────
# CONFIGURATION — update these to match your environment
# ─────────────────────────────────────────────────────────────────
LLAMA_STACK_URL = os.getenv("LLAMA_STACK_URL", "http://lsd-genai-playground-service.hospital-helpdesk.svc.cluster.local:8321")

# S3 — read from the data connection environment variables (set automatically when
# the 'data-connection-data' Secret is attached to the workbench)
S3_ENDPOINT   = os.getenv("AWS_S3_ENDPOINT", "http://s4.hospital-helpdesk.svc.cluster.local:7480")
S3_BUCKET     = os.getenv("AWS_S3_BUCKET", "data")
S3_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY_ID", "")
S3_SECRET_KEY = os.getenv("AWS_SECRET_ACCESS_KEY", "")

# NOTE: Leave this empty to use the same vector store that you used in the playground
VECTOR_STORE_NAME = ""


# ─────────────────────────────────────────────────────────────────
# PIPELINE COMPONENTS
# ─────────────────────────────────────────────────────────────────

@dsl.component(base_image="python:3.12", packages_to_install=["llama-stack-client>=0.7", "fire", "requests"])
def create_vector_store(
    llama_stack_url: str,
    vector_store_name: str,
    use_existing: bool,
) -> str:
    """Create a new Milvus-backed vector store, or return the ID of an existing one by name."""
    from llama_stack_client import LlamaStackClient

    client = LlamaStackClient(base_url=llama_stack_url)

    if use_existing:
        stores = client.vector_stores.list()
        if stores.data:
            existing = stores.data[0]
            print(f"Reusing existing vector store '{existing.name}' with ID: {existing.id}")
            return existing.id
        # No existing stores — fall through and create one with a default name
        vector_store_name = "hospital-helpdesk"
        print(f"No existing vector stores found. Creating '{vector_store_name}'...")

    vector_store = client.vector_stores.create(
        name=vector_store_name,
        extra_body={"provider_id": "milvus"},
    )
    print(f"Created vector store '{vector_store_name}' with ID: {vector_store.id}")
    return vector_store.id


@dsl.component(base_image="python:3.12", packages_to_install=["llama-stack-client>=0.7", "fire", "requests", "boto3>=1.26"])
def upload_and_index_documents(
    llama_stack_url: str,
    vector_store_id: str,
    s3_endpoint: str,
    s3_bucket: str,
    s3_access_key: str,
    s3_secret_key: str,
) -> int:
    """List all objects in the S3 bucket, upload each to Llama Stack, and add to the vector store."""
    import os
    import mimetypes
    import tempfile
    import boto3
    from llama_stack_client import LlamaStackClient

    s3 = boto3.client(
        "s3",
        endpoint_url=s3_endpoint,
        aws_access_key_id=s3_access_key,
        aws_secret_access_key=s3_secret_key,
    )
    client = LlamaStackClient(base_url=llama_stack_url)

    objects = s3.list_objects_v2(Bucket=s3_bucket).get("Contents", [])
    if not objects:
        print(f"No objects found in bucket '{s3_bucket}'. Nothing to index.")
        return 0

    count = 0
    for obj in objects:
        s3_key = obj["Key"]
        file_name = os.path.basename(s3_key)
        suffix = os.path.splitext(file_name)[1].lower()
        content_type = mimetypes.guess_type(file_name)[0] or "application/octet-stream"

        if suffix != ".pdf":
            print(f"Skipping '{file_name}' — only PDF files are indexed.")
            continue

        # Download from S3
        with tempfile.NamedTemporaryFile(suffix=suffix, delete=False) as tmp:
            s3.download_fileobj(s3_bucket, s3_key, tmp)
            tmp_path = tmp.name
        print(f"Downloaded '{s3_key}' from bucket '{s3_bucket}'")

        # Upload to Llama Stack file service
        with open(tmp_path, "rb") as f:
            uploaded_file = client.files.create(
                file=(file_name, f, content_type),
                purpose="assistants",
            )
        os.unlink(tmp_path)
        print(f"Uploaded '{file_name}' to Llama Stack — file ID: {uploaded_file.id}")

        # Add to vector store (triggers chunking & indexing)
        client.vector_stores.files.create(
            vector_store_id=vector_store_id,
            file_id=uploaded_file.id,
        )
        print(f"Added '{file_name}' to vector store '{vector_store_id}' — indexing started.")
        count += 1

    print()
    print("=" * 60)
    print(f"Indexed {count} file(s) into vector store.")
    print("IMPORTANT: Copy this vector store ID into 2_rag.ipynb:")
    print(f'  VECTOR_STORE_ID = "{vector_store_id}"')
    print("=" * 60)
    return count


# ─────────────────────────────────────────────────────────────────
# PIPELINE DEFINITION
# ─────────────────────────────────────────────────────────────────

@dsl.pipeline(
    name="rag-ingestion-pipeline",
    description="Ingest all documents from an S3 bucket into a Llama Stack vector store for RAG",
)
def rag_ingestion_pipeline(
    llama_stack_url: str,
    vector_store_name: str,
    use_existing: bool,
    s3_endpoint: str,
    s3_bucket: str,
    s3_access_key: str,
    s3_secret_key: str,
):
    create_vs_task = create_vector_store(
        llama_stack_url=llama_stack_url,
        vector_store_name=vector_store_name,
        use_existing=use_existing,
    )
    create_vs_task.set_caching_options(False)
    upload_task = upload_and_index_documents(
        llama_stack_url=llama_stack_url,
        vector_store_id=create_vs_task.output,
        s3_endpoint=s3_endpoint,
        s3_bucket=s3_bucket,
        s3_access_key=s3_access_key,
        s3_secret_key=s3_secret_key,
    )
    upload_task.set_caching_options(False)


# ─────────────────────────────────────────────────────────────────
# COMPILE AND SUBMIT
# ─────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    # Compile the pipeline to a YAML spec
    pipeline_yaml = "rag_pipeline.yaml"
    compiler.Compiler().compile(rag_ingestion_pipeline, pipeline_yaml)
    print(f"Pipeline compiled → {pipeline_yaml}")

    namespace_file_path =\
        '/var/run/secrets/kubernetes.io/serviceaccount/namespace'
    with open(namespace_file_path, 'r') as namespace_file:
        namespace = namespace_file.read()

    kubeflow_endpoint =\
        f'https://ds-pipeline-dspa.{namespace}.svc:8443'

    sa_token_file_path = '/var/run/secrets/kubernetes.io/serviceaccount/token'
    with open(sa_token_file_path, 'r') as token_file:
        bearer_token = token_file.read()

    ssl_ca_cert =\
        '/var/run/secrets/kubernetes.io/serviceaccount/service-ca.crt'

    print(f'Connecting to Data Science Pipelines: {kubeflow_endpoint}')
    kfp_client = Client(
        host=kubeflow_endpoint,
        existing_token=bearer_token,
        ssl_ca_cert=ssl_ca_cert
    )

    # Submit the pipeline run
    run = kfp_client.create_run_from_pipeline_func(
        rag_ingestion_pipeline,
        arguments={
            "llama_stack_url": LLAMA_STACK_URL,
            "vector_store_name": VECTOR_STORE_NAME,
            "use_existing": VECTOR_STORE_NAME == "",
            "s3_endpoint": S3_ENDPOINT,
            "s3_bucket": S3_BUCKET,
            "s3_access_key": S3_ACCESS_KEY,
            "s3_secret_key": S3_SECRET_KEY,
        },
        run_name=f"RAG Ingestion — {S3_BUCKET}",
    )
    print(f"\nPipeline run submitted! Run ID: {run.run_id}")
    print("Track it in: RHOAI Dashboard → Data Science Pipelines → Runs")
