import nox


@nox.session(python=["3.8"])
def tests(session):
    session.run("pipenv", "install", external=True)
    session.run("pipenv", "run", "test", external=True)
