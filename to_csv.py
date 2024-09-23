import csv
import sqlite3
import sys


def export(filename: str) -> None:
    conn = sqlite3.connect("nutritions.db")

    with open("export-all.sql") as fp:
        esql = fp.read()

    cur = conn.cursor()
    cur.execute(esql)

    with open(filename + ".csv", "w", newline="") as csvfile:
        spamwriter = csv.writer(csvfile)
        spamwriter.writerow([h[0] for h in cur.description])
        for r in cur:
            spamwriter.writerow(r)


if __name__ == "__main__":
    filename = "out"
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    export(filename)
