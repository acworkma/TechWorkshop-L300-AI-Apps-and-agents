import os
from dotenv import load_dotenv
load_dotenv()

errors = []

# 1. Check all required env vars are set
required = [
    "FOUNDRY_ENDPOINT", "FOUNDRY_KEY", "gpt_endpoint", "gpt_deployment",
    "gpt_api_key", "embedding_endpoint", "embedding_deployment",
    "embedding_api_key", "blob_connection_string", "storage_account_name",
    "COSMOS_ENDPOINT", "COSMOS_KEY", "DATABASE_NAME", "CONTAINER_NAME",
    "APPLICATIONINSIGHTS_CONNECTION_STRING",
]
for var in required:
    if not os.getenv(var):
        errors.append(f"Missing: {var}")

# 2. Test Cosmos DB connection
try:
    from azure.cosmos import CosmosClient
    client = CosmosClient(os.getenv("COSMOS_ENDPOINT"), os.getenv("COSMOS_KEY"))
    db = client.get_database_client(os.getenv("DATABASE_NAME"))
    db.read()
    print("✓ Cosmos DB connected")
except Exception as e:
    errors.append(f"Cosmos DB: {e}")

# 3. Test Blob Storage connection
try:
    from azure.storage.blob import BlobServiceClient
    blob = BlobServiceClient.from_connection_string(os.getenv("blob_connection_string"))
    props = blob.get_account_information()
    print("✓ Blob Storage connected")
except Exception as e:
    errors.append(f"Blob Storage: {e}")

# 4. Test GPT endpoint
try:
    from openai import AzureOpenAI
    oai = AzureOpenAI(
        azure_endpoint=os.getenv("gpt_endpoint"),
        api_key=os.getenv("gpt_api_key"),
        api_version=os.getenv("gpt_api_version"),
    )
    resp = oai.chat.completions.create(
        model=os.getenv("gpt_deployment"),
        messages=[{"role": "user", "content": "Say hello"}],
        max_tokens=5,
    )
    print("✓ GPT endpoint connected")
except Exception as e:
    errors.append(f"GPT: {e}")

if errors:
    print("\n--- FAILURES ---")
    for e in errors:
        print(f"  ✗ {e}")
else:
    print("\nAll connections OK!")
