# Database Migrations

This directory contains Django database migrations for the News Summary API. Migrations are Django's way of managing database schema changes over time.

## Overview

Migrations are version control for your database schema. They allow you to:
- Track changes to your models
- Apply schema changes to the database
- Rollback changes if needed
- Share database changes with team members

## Migration Files

### Current Migrations

```
migrations/
├── __init__.py              # Package initialization
├── 0001_initial.py          # Initial database schema
└── 0002_article_unique_constraint.py  # Article unique constraint (if exists)
```

### Migration File Structure

Each migration file contains:
- **Dependencies**: Which migrations must be applied first
- **Operations**: The actual database changes
- **Reverse Operations**: How to undo the changes

Example migration file:
```python
from django.db import migrations, models
import django.db.models.deletion
from django.conf import settings

class Migration(migrations.Migration):
    initial = True
    
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]
    
    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('url', models.URLField(unique=True)),
                ('source_name', models.CharField(max_length=100)),
                ('summary', models.TextField()),
                ('published_at', models.DateTimeField()),
                ('saved_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='article',
            unique_together={('user', 'url')},
        ),
    ]
```

## Database Schema

### Article Model Schema

The main migration creates the Article table with:

```sql
CREATE TABLE api_article (
    id BIGSERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    url VARCHAR(200) UNIQUE NOT NULL,
    source_name VARCHAR(100) NOT NULL,
    summary TEXT NOT NULL,
    published_at TIMESTAMP WITH TIME ZONE NOT NULL,
    saved_at TIMESTAMP WITH TIME ZONE NOT NULL,
    user_id INTEGER NOT NULL REFERENCES auth_user(id) ON DELETE CASCADE
);

-- Unique constraint to prevent duplicate articles per user
ALTER TABLE api_article 
ADD CONSTRAINT api_article_user_id_url_unique 
UNIQUE (user_id, url);

-- Indexes for performance
CREATE INDEX api_article_user_id_idx ON api_article(user_id);
CREATE INDEX api_article_saved_at_idx ON api_article(saved_at);
```

### User Model Schema

Uses Django's built-in User model:
```sql
-- This is managed by Django's auth migrations
CREATE TABLE auth_user (
    id SERIAL PRIMARY KEY,
    username VARCHAR(150) UNIQUE NOT NULL,
    email VARCHAR(254) NOT NULL,
    password VARCHAR(128) NOT NULL,
    first_name VARCHAR(150),
    last_name VARCHAR(150),
    is_active BOOLEAN DEFAULT true,
    is_staff BOOLEAN DEFAULT false,
    is_superuser BOOLEAN DEFAULT false,
    date_joined TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    last_login TIMESTAMP WITH TIME ZONE
);
```

## Migration Commands

### Creating Migrations

```bash
# Create migrations for model changes
python manage.py makemigrations

# Create migration for specific app
python manage.py makemigrations api

# Create empty migration file
python manage.py makemigrations --empty api

# Name your migration
python manage.py makemigrations --name add_article_index api
```

### Applying Migrations

```bash
# Apply all pending migrations
python manage.py migrate

# Apply migrations for specific app
python manage.py migrate api

# Apply specific migration
python manage.py migrate api 0001

# Fake apply migration (mark as applied without running)
python manage.py migrate --fake api 0001
```

### Migration Information

```bash
# Show migration status
python manage.py showmigrations

# Show migration details
python manage.py showmigrations --verbosity=2

# Show specific app migrations
python manage.py showmigrations api

# Show migration plan
python manage.py migrate --plan
```

### Rollback Migrations

```bash
# Rollback to previous migration
python manage.py migrate api 0001

# Rollback all migrations for an app
python manage.py migrate api zero

# Show SQL for rollback
python manage.py sqlmigrate api 0001 --backwards
```

## Migration Best Practices

### 1. Always Create Migrations

```bash
# After changing models.py
python manage.py makemigrations
python manage.py migrate
```

### 2. Review Migration Files

Before applying migrations:
- Check the generated SQL
- Verify the operations are correct
- Test on a copy of production data

### 3. Backup Before Major Changes

```bash
# PostgreSQL backup
pg_dump news_summary_db > backup.sql

# Apply migrations
python manage.py migrate

# Restore if needed
psql news_summary_db < backup.sql
```

### 4. Handle Data Migrations

For complex data transformations:

```python
# In a migration file
from django.db import migrations

def migrate_data_forward(apps, schema_editor):
    Article = apps.get_model('api', 'Article')
    # Your data transformation logic
    pass

def migrate_data_backward(apps, schema_editor):
    # Reverse data transformation
    pass

class Migration(migrations.Migration):
    dependencies = [
        ('api', '0001_initial'),
    ]
    
    operations = [
        migrations.RunPython(migrate_data_forward, migrate_data_backward),
    ]
```

## Common Migration Scenarios

### 1. Adding New Fields

```python
operations = [
    migrations.AddField(
        model_name='article',
        name='category',
        field=models.CharField(max_length=50, default='general'),
    ),
]
```

### 2. Removing Fields

```python
operations = [
    migrations.RemoveField(
        model_name='article',
        name='old_field',
    ),
]
```

### 3. Changing Field Types

```python
operations = [
    migrations.AlterField(
        model_name='article',
        name='summary',
        field=models.TextField(blank=True),
    ),
]
```

### 4. Adding Indexes

```python
operations = [
    migrations.RunSQL(
        "CREATE INDEX api_article_title_idx ON api_article(title);",
        reverse_sql="DROP INDEX api_article_title_idx;"
    ),
]
```

## Troubleshooting

### Common Issues

1. **Migration Conflicts**
   ```bash
   # Resolve migration conflicts
   python manage.py makemigrations --merge
   ```

2. **Fake Migrations**
   ```bash
   # If migration already applied manually
   python manage.py migrate --fake api 0001
   ```

3. **Reset Migrations**
   ```bash
   # Remove migration files (backup first!)
   rm api/migrations/0*.py
   python manage.py makemigrations api
   ```

4. **Database State Issues**
   ```bash
   # Check current database state
   python manage.py dbshell
   \dt  # List tables in PostgreSQL
   ```

### Testing Migrations

```bash
# Test migration forward and backward
python manage.py migrate api 0001
python manage.py migrate api zero
python manage.py migrate api 0001
```

## Production Deployment

### Migration Checklist

1. **Backup database**
2. **Test migrations on staging**
3. **Review migration SQL**
4. **Plan for rollback**
5. **Monitor after deployment**

### Zero-Downtime Migrations

For production systems:
1. Make additive changes first
2. Deploy application code
3. Remove old code references
4. Remove old database columns

### Example Deployment Script

```bash
#!/bin/bash
# Production migration deployment

# Backup
pg_dump news_summary_db > "backup_$(date +%Y%m%d_%H%M%S).sql"

# Apply migrations
python manage.py migrate --verbosity=2

# Verify
python manage.py showmigrations

# Restart application
sudo systemctl restart gunicorn
```

This migrations directory is crucial for maintaining database consistency and tracking schema changes throughout the development lifecycle.
