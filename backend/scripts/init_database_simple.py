# Simple Database Initialization Script
# Creates all tables without loading agents (use API to add agents)

import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.database import init_db, engine, DATABASE_PATH

def main():
    """Initialize database tables only"""
    print("Initializing Agent Reality Map Backend Database...")
    print("\n1. Creating database tables...")

    try:
        init_db()
        print(f"SUCCESS: Database initialized at {DATABASE_PATH}")

        # Verify tables were created
        from sqlalchemy import inspect
        inspector = inspect(engine)
        tables = inspector.get_table_names()

        print(f"\n2. Verifying tables...")
        print(f"   Tables created: {len(tables)}")
        for table in tables:
            print(f"   - {table}")

        print("\n" + "=" * 50)
        print("DATABASE INITIALIZATION COMPLETE")
        print("=" * 50)
        print("\nNext steps:")
        print("1. Start the API server: cd backend && python -m app.main")
        print("2. Test endpoints: curl http://localhost:8000/health")
        print("3. Add agents via API: POST http://localhost:8000/api/v1/agents/")
        print("4. View API docs: http://localhost:8000/docs")

    except Exception as e:
        print(f"\nERROR: Failed to initialize database")
        print(f"Details: {e}")
        return 1

    return 0

if __name__ == "__main__":
    sys.exit(main())
