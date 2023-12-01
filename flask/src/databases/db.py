from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.orm import declarative_base
from config import config


engine = create_engine(
    "postgresql://{user}:{password}@{host}:{port}/{database}".format(
        user=config.postgres.user,
        password=config.postgres.password,
        host=config.docker.postgres_host,
        port=config.postgres.port,
        database=config.postgres.db,
    )
)
db_session = scoped_session(
    sessionmaker(autocommit=False, autoflush=False, bind=engine)
)
Base = declarative_base()
Base.query = db_session.query_property()


def add_admin_and_roles(app, User, Role) -> None:
    with app.app_context():
        if db_session.query(User).filter(User.login == config.admin.login).count() == 0:
            data = []
            for role in config.admin.all_roles.split(","):
                data.append(Role(name=role))
            db_session.add_all(data)
            db_session.commit()

            admin = User(login=config.admin.login, password=config.admin.password)
            roles = db_session.query(Role).all()
            for role in roles:
                admin.roles.append(role)
            db_session.add(admin)
            db_session.commit()
