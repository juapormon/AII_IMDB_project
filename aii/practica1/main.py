
from repository import Repository
import requester_practica1


def reset(repo):
    conn = repo.connect()
    conn.execute("DROP TABLE IF EXISTS FILMS;")
    conn.execute("CREATE TABLE FILMS("
                 "TITLE TEXT NOT NULL, "
                 "ORIGINAL_TITLE TEXT NOT NULL, "
                 "COUNTRIES TEXT NOT NULL, "
                 "RELEASE_DATE TEXT NOT NULL, "
                 "DIRECTOR TEXT NOT NULL, "
                 "GENRES TEXT NOT NULL);")
    conn.commit()
    conn.close()


def write_repo(conn, title, original_title, countries, release_date, director, genres):
    conn.execute(
        """INSERT INTO FILMS (TITLE, ORIGINAL_TITLE, COUNTRIES, RELEASE_DATE, DIRECTOR, GENRES) VALUES (?,?,?,?,?,?)""",
        (title, original_title, countries, release_date, director, genres))
    conn.commit()


def main(reset_repo=False):
    repo = Repository('../db/practica1.db')
    if reset_repo:
        reset(repo)

    films = requester_practica1.main()
    conn = repo.connect()
    conn.text_factory = str
    for film in films:
        write_repo(conn, film['TITLE'], film['ORIGINAL_TITLE'], film['COUNTRIES'],
                   film['RELEASE_DATE'], film['DIRECTOR'], film['GENRES'])
    else:
        cursor = conn.execute("SELECT TITLE from FILMS")
        for row in cursor:
            print("TITLE = ", row[0])
        conn.close()


if __name__ == '__main__':
    main(True)
