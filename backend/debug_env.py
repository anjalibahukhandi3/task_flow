import sys
import os

log_file = os.path.join(os.path.dirname(__file__), 'debug_out.txt')

with open(log_file, 'w') as f:
    f.write(f"Python version: {sys.version}\n")
    f.write(f"CWD: {os.getcwd()}\n")
    f.write(f"sys.path: {sys.path}\n")
    try:
        import fastapi
        f.write("FastAPI installed\n")
    except ImportError:
        f.write("FastAPI NOT installed\n")
        
    try:
        import sqlalchemy
        f.write("SQLAlchemy installed\n")
    except ImportError:
        f.write("SQLAlchemy NOT installed\n")

    try:
        import main
        f.write("Successfully imported main\n")
    except Exception as e:
        f.write(f"Error importing main: {str(e)}\n")
        import traceback
        traceback.print_exc(file=f)
