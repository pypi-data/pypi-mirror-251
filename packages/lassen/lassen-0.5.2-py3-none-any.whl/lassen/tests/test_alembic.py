import pytest
from alembic.config import Config
from alembic.runtime import migration
from alembic.script import ScriptDirectory

from lassen.alembic.cli import AlembicManager
from lassen.assets import get_asset_path
from lassen.db.session import get_db_context

# Since we embed the test_harness module in the test_harness package, we can
# cite it directly via absolute import
TEST_HARNESS_MODULE = "lassen.tests.fixtures.test_harness.test_harness"


@pytest.fixture()
def alembic_manager():
    return AlembicManager(TEST_HARNESS_MODULE)


@pytest.fixture()
def alembic_script(alembic_manager: AlembicManager):
    """
    We use a fake script directory to get the current state of the on-disk migrations.
    """
    with alembic_manager.make_script_directory() as directory:
        config = Config(get_asset_path("alembic.ini"))
        config.set_main_option("script_location", str(directory))
        script = ScriptDirectory.from_config(config)
        yield script


def check_base(engine, script: ScriptDirectory):
    """
    Check that the state of the database is at the base revision
    """
    with engine.begin() as conn:
        context = migration.MigrationContext.configure(conn)
        assert context.get_current_revision() is None
        assert script.get_current_head() is not None


def check_head(engine, script: ScriptDirectory):
    """
    Check that the state of the database is at the head revision
    """
    with engine.begin() as conn:
        context = migration.MigrationContext.configure(conn)
        assert context.get_current_revision() == script.get_current_head()


def test_upgrade(
    clear_db,
    alembic_script: ScriptDirectory,
    alembic_manager: AlembicManager,
):
    # Use an explicit db to avoid the fixture creating the test models for us
    # We want to test for that within this unit test
    with get_db_context(refresh=False) as db:
        engine = db.get_bind()

        check_base(engine, alembic_script)

        alembic_manager.upgrade(revision="head")
        check_head(engine, alembic_script)


def test_downgrade(
    clear_db,
    alembic_script: ScriptDirectory,
    alembic_manager: AlembicManager,
):
    with get_db_context(refresh=False) as db:
        engine = db.get_bind()

        check_base(engine, alembic_script)

        alembic_manager.upgrade(revision="head")
        check_head(engine, alembic_script)

        alembic_manager.downgrade(revision="base")
        check_base(engine, alembic_script)
