from django.apps import apps
from django.conf import settings
from django.db.migrations.state import ModelState
from django.core.management.base import BaseCommand
from django.db.migrations import operations
from django.db.migrations.migration import Migration
from django.db import connections
from django.db.migrations.state import ProjectState
from unittest.mock import MagicMock


class CursorMock:
    connection = MagicMock()

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        return


class Command(BaseCommand):
    help = "Prints the DDL of the database"

    def add_arguments(self, parser):
        parser.add_argument(
            "--db_alias",
            help="Alias of DB to be used (from settings), defaults to 'default'",
        )

    def handle(self, *args, **options):
        db_alias = options['db_alias'] if options['db_alias'] else 'default'
        connection = connections[db_alias]
        self.mock_db_connection(connection)
        for app in settings.INSTALLED_APPS:
            app_name: str = app.split('.')[0]
            app_models = apps.get_app_config(app_name).get_models()
            # Let the migration framework think that the project is in an initial state
            state = ProjectState()
            for model in app_models:
                model_state = ModelState.from_model(model)

                # Create a fake migration with the CreateModel operation
                cm = operations.CreateModel(
                    name=model_state.name, fields=model_state.fields.items())
                migration = Migration("fake_migration", app_name)
                migration.operations.append(cm)

                with connection.schema_editor(collect_sql=True, atomic=False) as schema_editor:
                    state = migration.apply(
                        state, schema_editor, collect_sql=True)

                sqls: list[str] = schema_editor.collected_sql
                sqls_without_comments = []
                for sql in sqls:
                    if sql.startswith('--'):
                        continue
                    sqls_without_comments.append(sql)

                self.stdout.writelines(sqls_without_comments)

    @staticmethod
    def mock_db_connection(connection):
        connection.cursor = CursorMock
        if connection.vendor == 'sqlite':
            connection.disable_constraint_checking = lambda: True
            connection.check_constraints = lambda: None
            connection.enable_constraint_checking = lambda: None
        if connection.vendor == 'mysql':
            # TODO: pass in mariadb, mysql version, and storage engine as flags
            connection.mysql_is_mariadb = False
            connection.mysql_version = (10, 7)
            connection.introspection.get_storage_engine = lambda x, y: 'InnoDB'
        # TODO: support oracle
