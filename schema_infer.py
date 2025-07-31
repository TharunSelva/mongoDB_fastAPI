from mongodb_schema.exporter import MongoSchemaExporter
from functools import lru_cache
import os

@lru_cache()
def get_schema_map():
    uri = os.getenv("MONGODB_URI")
    db_name = os.getenv("DB_NAME")
    exporter = MongoSchemaExporter(uri=uri, database=db_name)
    result = exporter.export_schema(sample_size=50)
    return result  # dict of collections → inferred schema