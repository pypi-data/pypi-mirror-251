# DDL Print
DDLPrint is a Django app that prints the DDL of your models without connecting to an actual database, and without relying on your migrations.

## Installation
1. Install the `ddlprint` package:

```bash
pip install ddlprint
```

## Configuration

2. Add `ddl_print` to your Django project's `INSTALLED_APPS` in `settings.py`:

```python
INSTALLED_APPS = [
    ...,
    'ddl_print',
    ...
]
```

## Usage

3. Print the DDL using your default DB driver by running the `ddl` management command:

```bash
python manage.py ddl
```

4. You can specify a specific DB driver by passing the alias to the --db_alias flag. You can find more info on how to set up different DB drivers here https://docs.djangoproject.com/en/5.0/ref/databases/.

```bash
python manage.py ddl --db_alias mycoolalias
```
