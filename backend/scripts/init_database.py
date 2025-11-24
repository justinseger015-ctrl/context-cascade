# Database Initialization Script
# Creates all tables and optionally loads 207 agents from Phase 1 identity files

import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.database import init_db, SessionLocal, Base, engine
from app.models import Agent, Metric, AuditLog
import json

def load_agents_from_files():
    """
    Load 207 agents from Phase 1 identity YAML files into database.

    Scans agents/ directory for .md files with identity frontmatter.
    """
    print("Loading agents from Phase 1 identity files...")

    agents_dir = Path(__file__).parent.parent.parent / "agents"
    if not agents_dir.exists():
        print(f"Agents directory not found: {agents_dir}")
        return 0

    db = SessionLocal()
    loaded_count = 0

    try:
        # Find all .md files in agents directory
        for md_file in agents_dir.rglob("*.md"):
            try:
                content = md_file.read_text(encoding="utf-8")

                # Parse YAML frontmatter (simple parse, assumes proper format)
                if not content.startswith("---"):
                    continue

                parts = content.split("---", 2)
                if len(parts) < 3:
                    continue

                # Extract YAML frontmatter
                frontmatter = parts[1].strip()

                # Parse identity section (very basic YAML parsing)
                # In production, use yaml.safe_load()
                identity = {}
                rbac = {}
                budget = {}
                metadata = {}

                lines = frontmatter.split("\n")
                current_section = None

                for line in lines:
                    line = line.strip()
                    if line.startswith("identity:"):
                        current_section = "identity"
                    elif line.startswith("rbac:"):
                        current_section = "rbac"
                    elif line.startswith("budget:"):
                        current_section = "budget"
                    elif line.startswith("metadata:"):
                        current_section = "metadata"
                    elif current_section and ":" in line:
                        key, value = line.split(":", 1)
                        key = key.strip()
                        value = value.strip()

                        # Simple value parsing
                        if value.startswith("[") and value.endswith("]"):
                            # List value
                            value = [v.strip().strip('"\'') for v in value[1:-1].split(",")]
                        elif value.lower() in ["true", "false"]:
                            value = value.lower() == "true"
                        elif value.replace(".", "").isdigit():
                            value = float(value) if "." in value else int(value)
                        else:
                            value = value.strip('"\'')

                        if current_section == "identity":
                            identity[key] = value
                        elif current_section == "rbac":
                            rbac[key] = value
                        elif current_section == "budget":
                            budget[key] = value
                        elif current_section == "metadata":
                            metadata[key] = value

                # Check if we have required identity fields
                if not identity.get("agent_id"):
                    continue

                # Check if agent already exists
                existing = db.query(Agent).filter(Agent.agent_id == identity["agent_id"]).first()
                if existing:
                    print(f"Skipping existing agent: {identity.get('agent_id')}")
                    continue

                # Extract name from filename (e.g., coder.md -> coder)
                agent_name = md_file.stem

                # Create agent record
                agent = Agent(
                    agent_id=identity["agent_id"],
                    name=agent_name,
                    role=identity.get("role", "developer"),
                    role_confidence=identity.get("role_confidence", 0.0),
                    role_reasoning=identity.get("role_reasoning", ""),
                    capabilities=[],  # Would parse from frontmatter
                    rbac_allowed_tools=rbac.get("allowed_tools", []),
                    rbac_path_scopes=rbac.get("path_scopes", []),
                    rbac_api_access=rbac.get("api_access", []),
                    rbac_requires_approval=rbac.get("requires_approval", False),
                    rbac_approval_threshold=rbac.get("approval_threshold", 10.0),
                    budget_max_tokens_per_session=budget.get("max_tokens_per_session", 100000),
                    budget_max_cost_per_day=budget.get("max_cost_per_day", 10.0),
                    budget_currency=budget.get("currency", "USD"),
                    metadata_category=metadata.get("category", "foundry"),
                    metadata_specialist=metadata.get("specialist", False),
                    metadata_version=metadata.get("version", "1.0.0"),
                    metadata_tags=metadata.get("tags", [])
                )

                db.add(agent)
                loaded_count += 1

                if loaded_count % 20 == 0:
                    print(f"Loaded {loaded_count} agents...")

            except Exception as e:
                print(f"Error loading {md_file}: {e}")
                continue

        db.commit()
        print(f"\nSuccessfully loaded {loaded_count} agents into database!")

    finally:
        db.close()

    return loaded_count

def main():
    """Initialize database and optionally load agents"""
    print("Initializing Agent Reality Map Backend Database...")

    # Create all tables
    print("\n1. Creating database tables...")
    init_db()

    # Load agents from Phase 1 identity files
    print("\n2. Loading agents from identity files...")
    loaded = load_agents_from_files()

    print("\n" + "=" * 50)
    print("DATABASE INITIALIZATION COMPLETE")
    print("=" * 50)
    print(f"Agents loaded: {loaded}")
    print("\nNext steps:")
    print("1. Start the API server: cd backend && python -m app.main")
    print("2. Test endpoints: curl http://localhost:8000/health")
    print("3. View API docs: http://localhost:8000/docs")

if __name__ == "__main__":
    main()
