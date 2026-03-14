import models
from database import engine
import os

print("Starting database test...")
try:
    print("Attempting to create all tables...")
    models.Base.metadata.create_all(bind=engine)
    print("Tables created successfully.")
    
    db_file = "task_intern.db"
    if os.path.exists(db_file):
        print(f"Database file {db_file} exists.")
    else:
        print(f"Database file {db_file} does NOT exist.")
except Exception as e:
    print(f"Error occurred: {str(e)}")
    import traceback
    traceback.print_exc()
