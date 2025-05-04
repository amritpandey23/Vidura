import os
from flask_migrate import upgrade, migrate, init, stamp
from tracker import app

app.app_context().push()

migrations_dir = os.path.join(os.getcwd(), "migrations")
if not os.path.exists(migrations_dir):
    print("🔧 Initializing migrations...")
    init()
    stamp()

print("📦 Generating migration...")
migrate(message="Auto migration")

print("⬆️ Applying migration...")
upgrade()

print("✅ Migration complete.")
