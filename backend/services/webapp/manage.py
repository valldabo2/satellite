from flask.cli import FlaskGroup
from project import app, db
from project.models.fire import Fire
from fake_data import FAKE_DATA,COLUMNS

cli = FlaskGroup(app)


@cli.command("create_db")
def create_db():
    _create_db()


def _create_db():
    db.drop_all()
    db.create_all()
    db.session.commit()


@cli.command("seed_db")
def seed_db():
    _seed_db()


def _seed_db():

    for fake_record in FAKE_DATA:
        db.session.add(
            Fire(**dict(zip(COLUMNS,fake_record))))

    db.session.commit()


if __name__ == "__main__":
    _create_db()
    _seed_db()
    cli()

