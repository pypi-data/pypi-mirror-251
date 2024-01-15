from phi.k8s.app.postgres.postgres import PostgresDb


class PgVectorDb(PostgresDb):
    # -*- App Name
    name: str = "pgvector"

    # -*- Image Configuration
    image_name: str = "phidata/pgvector"
    image_tag: str = "15"
