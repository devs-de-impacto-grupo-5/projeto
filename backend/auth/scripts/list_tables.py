import os
from sqlalchemy import create_engine, inspect


def main():
    url = os.getenv("DATABASE_URL")
    if not url:
        print("DATABASE_URL não está definida no ambiente.")
        return

    engine = create_engine(url)
    insp = inspect(engine)
    tables = insp.get_table_names()
    print("Tabelas no banco:")
    for t in tables:
        print(f" - {t}")


if __name__ == "__main__":
    main()
