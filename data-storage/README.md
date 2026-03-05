# Data Storage (S3 + Bedrock Knowledge Base Data)

This folder stores sample UTD chatbot data used by Bedrock Knowledge Base retrieval.

## Files

- `sample-data/dining.json`
- `sample-data/events.json`
- `sample-data/parking.json`

## Data role in this project

1. Upload JSON files to S3.
2. Connect S3 path to Bedrock Knowledge Base.
3. Sync the knowledge base.
4. Lambda retrieves relevant chunks during chat requests.

## Steps to set up in AWS console

1. Create S3 bucket (or use existing).
2. Create a folder/prefix for chatbot data (example: `utd-data/`).
3. Upload all `sample-data/*.json` files.
4. In Bedrock console, create a Knowledge Base.
5. Add S3 data source pointing to the same bucket/prefix.
6. Run sync/ingestion and wait until status is complete.
7. Copy the `Knowledge Base ID` into Lambda environment variable `KNOWLEDGE_BASE_ID`.

## Data quality notes

1. Keep consistent field names per file.
2. Prefer normalized text values for building names and locations.
3. Update files in S3 and re-sync KB after each change.

## Common issues and fixes

1. KB sync failed
   - Check S3 permissions for the KB role.
   - Verify bucket and prefix path are correct.
2. Chatbot returns outdated info
   - Re-upload changed files and re-run KB sync.
3. Retrieval misses expected records
   - Check JSON formatting and text clarity.
   - Break very large files into smaller logical files if needed.
4. Empty responses from backend
   - Confirm Lambda is using the correct `KNOWLEDGE_BASE_ID`.
   - Confirm KB status is `Active` and last sync succeeded.

## Run and validate (end)

1. Update one record in `sample-data` and upload to S3.
2. Re-sync Bedrock KB.
3. Ask frontend a question about that updated record.
4. Confirm new answer appears and CloudWatch shows successful Bedrock call.
