from azure.storage.blob import BlockBlobService
from azure.storage.blob import ContentSettings
import os
import sys

buildId = sys.argv[1]
blob_service = BlockBlobService(account_name='gpuvmtemplatedisks530', account_key='9aSfzJqvoasgkzMod9qNJGDabjtSUbibZjjvsnvHaYMatASwF/y9kH2nbTAOKnLb7bLWjdIJUdwzXhTCvO2L/g==')

ouputPath = '../output'
files = os.listdir(ouputPath)

for file in files:
  blob_service.create_blob_from_path(
      'output',
      str(file+buildId),
      os.path.join(ouputPath, file))
