def quickQuery(db, query):
    """
    result = quickQuery(db, query)

    Helper function to execute and return result for a query (query)
    on a database that has an existing connection (db).
    """
    cursor = db.cursor()
    cursor.execute(query)
    records = cursor.fetchall()
    return records


def quickWrite(fn, text, lineend='\n\n'):
    """
    quickWrite(fn, text, lineend='\n\n')

    Function simply writes out text to a file (fn) and appends
    two empty lines afterwards. It will create a file if it does
    not exist.
    """
    f = open(fn, 'a')
    f.write(text + lineend)
    f.close()


def str2bool(v):
    """
    x = str2bool(v)

    Helper function to interpret whether command line arguments
    are true/false via string input and return data of Boolean type.
    """
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')
