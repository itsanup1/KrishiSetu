"""
User table schema reference.
See init_db.sql for the actual table creation SQL.

Columns:
    id              UUID PRIMARY KEY (auto-generated)
    name            VARCHAR(100) NOT NULL
    email           VARCHAR(255) UNIQUE NOT NULL
    phone           VARCHAR(20) NOT NULL
    password_hash   TEXT NOT NULL
    role            VARCHAR(20) NOT NULL DEFAULT 'farmer'
                    Possible values: 'farmer', 'vendor', 'admin'
    location        VARCHAR(255) nullable
    is_active       BOOLEAN DEFAULT TRUE
    created_at      TIMESTAMP DEFAULT NOW()

Note: Farmer and Equipment Owner share the 'farmer' role.
Equipment listing capability will be added as a separate flag later.
"""
