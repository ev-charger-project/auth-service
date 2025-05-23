from dependency_injector import containers, providers

from app.core.config import configs
from app.core.database import Database
from app.repository import UserRepository
from app.repository.refresh_token_repository import RefreshTokenRepository
from app.services import AuthService, UserService


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        modules=[
            "app.core.dependencies",
            "app.api.v1.endpoints.auth",
            "app.api.v1.endpoints.user",
        ]
    )

    db = providers.Singleton(Database, db_url=configs.DATABASE_URI)

    user_repository = providers.Factory(UserRepository, session_factory=db.provided.session)
    refresh_token_repository = providers.Factory(RefreshTokenRepository, session_factory=db.provided.session)
    auth_service = providers.Factory(AuthService, user_repository=user_repository, refresh_token_repository=refresh_token_repository)
    user_service = providers.Factory(UserService, user_repository=user_repository)
