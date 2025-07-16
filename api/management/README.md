# Management Commands Module

This module contains custom Django management commands for the News Summary API. These commands provide administrative functionality and maintenance tools for the application.

## Module Structure

```
api/management/
├── __init__.py              # Package initialization
└── commands/
    ├── __init__.py          # Commands package initialization
    └── clear_articles.py    # Clear articles command
```

## Commands Overview

### 1. Clear Articles Command (`clear_articles.py`)

**Purpose:** Removes all saved articles from the database

**Usage:**
```bash
python manage.py clear_articles
```

**Features:**
- Removes all Article instances from the database
- Preserves user accounts and authentication data
- Provides confirmation feedback
- Safe operation with transaction support

**Implementation:**
```python
from django.core.management.base import BaseCommand
from api.models import Article

class Command(BaseCommand):
    help = 'Clear all saved articles from the database'
    
    def handle(self, *args, **options):
        article_count = Article.objects.count()
        Article.objects.all().delete()
        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully cleared {article_count} articles'
            )
        )
```

## Creating Custom Commands

### Command Structure

To create a new management command:

1. Create a new file in `api/management/commands/`
2. Implement the `Command` class inheriting from `BaseCommand`
3. Define the `handle` method with your command logic

### Example Template

```python
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

class Command(BaseCommand):
    help = 'Description of what your command does'
    
    def add_arguments(self, parser):
        """Add command-line arguments"""
        parser.add_argument(
            '--option',
            type=str,
            help='Description of the option'
        )
    
    def handle(self, *args, **options):
        """Main command logic"""
        try:
            with transaction.atomic():
                # Your command logic here
                self.stdout.write(
                    self.style.SUCCESS('Command completed successfully')
                )
        except Exception as e:
            raise CommandError(f'Command failed: {e}')
```

## Available Commands

### Built-in Django Commands

These standard Django commands are available:

**Database Management:**
```bash
python manage.py migrate          # Apply database migrations
python manage.py makemigrations   # Create new migrations
python manage.py dbshell          # Database shell
python manage.py flush            # Clear all data
python manage.py loaddata         # Load fixture data
python manage.py dumpdata         # Export data
```

**User Management:**
```bash
python manage.py createsuperuser  # Create admin user
python manage.py changepassword   # Change user password
```

**Development:**
```bash
python manage.py runserver        # Start development server
python manage.py shell            # Django shell
python manage.py test             # Run tests
python manage.py check            # System check
```

**Static Files:**
```bash
python manage.py collectstatic    # Collect static files
python manage.py findstatic       # Find static files
```

### Custom Commands

**Application-Specific:**
```bash
python manage.py clear_articles   # Clear all saved articles
```

## Command Development Guidelines

### 1. Command Design Principles

**Single Responsibility:** Each command should have one clear purpose
**Idempotent:** Commands should be safe to run multiple times
**Informative:** Provide clear output and error messages
**Transactional:** Use database transactions for data operations

### 2. Error Handling

```python
from django.core.management.base import CommandError

def handle(self, *args, **options):
    try:
        # Command logic
        pass
    except SomeSpecificError as e:
        raise CommandError(f'Specific error occurred: {e}')
    except Exception as e:
        raise CommandError(f'Unexpected error: {e}')
```

### 3. Output Styling

```python
# Success messages
self.stdout.write(self.style.SUCCESS('Success message'))

# Error messages
self.stdout.write(self.style.ERROR('Error message'))

# Warning messages
self.stdout.write(self.style.WARNING('Warning message'))

# HTTP status codes
self.stdout.write(self.style.HTTP_INFO('200 OK'))
self.stdout.write(self.style.HTTP_SUCCESS('201 Created'))
self.stdout.write(self.style.HTTP_BAD_REQUEST('400 Bad Request'))
```

### 4. Arguments and Options

```python
def add_arguments(self, parser):
    # Positional arguments
    parser.add_argument('poll_ids', nargs='+', type=int)
    
    # Optional arguments
    parser.add_argument(
        '--delete',
        action='store_true',
        help='Delete items instead of creating them'
    )
    
    # Arguments with values
    parser.add_argument(
        '--format',
        type=str,
        choices=['json', 'xml', 'csv'],
        default='json',
        help='Output format'
    )
```

## Common Use Cases

### 1. Data Maintenance Commands

```python
# Clear old data
python manage.py clear_old_articles --days=30

# Backup data
python manage.py backup_articles --format=json

# Import data
python manage.py import_articles --file=articles.json
```

### 2. System Monitoring Commands

```python
# Check system health
python manage.py health_check

# Generate reports
python manage.py generate_report --type=usage

# Monitor performance
python manage.py performance_check
```

### 3. Batch Operations

```python
# Process articles in batches
python manage.py process_articles --batch-size=100

# Update summaries
python manage.py update_summaries --all

# Cleanup duplicates
python manage.py remove_duplicates
```

## Testing Commands

### Unit Testing

```python
from django.test import TestCase
from django.core.management import call_command
from django.core.management.base import CommandError
from io import StringIO

class ClearArticlesCommandTest(TestCase):
    def test_clear_articles_success(self):
        # Create test data
        # ...
        
        # Capture output
        out = StringIO()
        call_command('clear_articles', stdout=out)
        
        # Assert results
        self.assertIn('Successfully cleared', out.getvalue())
```

### Integration Testing

```python
def test_command_integration(self):
    # Test command with real database
    call_command('clear_articles')
    
    # Verify database state
    self.assertEqual(Article.objects.count(), 0)
```

## Deployment Considerations

### Production Commands

```bash
# Run in production environment
python manage.py clear_articles --settings=production_settings

# With logging
python manage.py clear_articles > /var/log/clear_articles.log 2>&1

# As cron job
0 2 * * * /path/to/venv/bin/python /path/to/manage.py clear_articles
```

### Environment Variables

Commands can access environment variables:

```python
import os

def handle(self, *args, **options):
    if os.getenv('ENVIRONMENT') == 'production':
        # Production-specific logic
        pass
```

## Best Practices

1. **Always use transactions** for database operations
2. **Provide meaningful help text** for commands
3. **Handle errors gracefully** with appropriate error messages
4. **Use styled output** for better user experience
5. **Make commands idempotent** when possible
6. **Document command usage** in help text
7. **Test commands thoroughly** before deployment

This module provides essential maintenance and administrative capabilities for the News Summary API, ensuring smooth operations and easy management of the application data.
