from overlearn import create_app, db
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData

convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

app = create_app()
metadata = MetaData(naming_convention=convention)
db = SQLAlchemy(app, metadata=metadata)
manager = Manager(app)
migrate = Migrate(app, db, render_as_batch=True)

manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()