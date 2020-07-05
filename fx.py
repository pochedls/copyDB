def quickQuery(db, query):
    cursor = db.cursor()
    cursor.execute(query)
    records = cursor.fetchall()
    return records


def quickWrite(fn, text, lineend='\n\n'):
    f = open(fn, 'a')
    f.write(text + lineend)
    f.close()