"""Short-lived DB-API connections; no database credentials reach the browser."""
import os
from contextlib import contextmanager


def connect(namespace=None, native=False):
    import iris
    import iris.dbapi
    factory = iris.connect if native else iris.dbapi.connect
    return factory(
        hostname=os.getenv("IRIS_HOST", "localhost"),
        port=int(os.getenv("IRIS_PORT", "1972")),
        namespace=namespace or os.getenv("IRIS_NAMESPACE", "FHIRSERVER"),
        username=os.getenv("IRIS_USERNAME", "SuperUser"),
        password=os.environ["IRIS_PASSWORD"],
        sharedmemory=False,
        sslconfig=False,
        **({} if native else {"autoCommit": False}),
    )


@contextmanager
def transaction():
    conn = connect()
    cursor = conn.cursor()
    try:
        yield cursor
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        cursor.close()
        conn.close()
