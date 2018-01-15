

from invoke import task

from frontline.db import engine
from frontline.models import Base


@task
def drop_db(ctx):
    Base.metadata.drop_all(engine)


@task
def create_db(ctx):
    Base.metadata.create_all(engine)


@task(drop_db, create_db)
def reset_db(ctx):
    pass
