from litestar import Litestar
from litestar.contrib.sqlalchemy.plugins import SQLAlchemyAsyncConfig, SQLAlchemyInitPlugin

# Create SQLAlchemy configuration
sqlalchemy_config = SQLAlchemyAsyncConfig(
    connection_string="",
    session_dependency_key="db_session"
)  # Create 'async_session' dependency
sqlalchemy_plugin = SQLAlchemyInitPlugin(sqlalchemy_config)


async def on_startup() -> None:
    """Initializes the database (...)"""
    async with sqlalchemy_config.create_engine().begin as conn:
        await conn.run_sync()

app = Litestar(
    route_handlers=[],
    on_startup=[on_startup],
    plugins=[SQLAlchemyInitPlugin(sqlalchemy_config)],
)
