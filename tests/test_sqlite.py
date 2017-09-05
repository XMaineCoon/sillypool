import sqlite3
import time


if __name__ == '__main__':
    conn = sqlite3.connect('data/example.db', timeout=10)
    c = conn.cursor()
    # c.execute("""
    # CREATE TABLE stocks
    #          (date text,
    #          trans text,
    #          symbol text,
    #          qty real,
    #          price real)
    # """)
    start_time = time.time()
    for i in range(10000):
        while True:
            try:
                print('start: ' + str(i))
                c.execute("INSERT INTO stocks VALUES ('2006-01-05','BUY','RHAT',100,35.14)")
                print('end  : ' + str(i))
                break
            except sqlite3.OperationalError:
                pass
    conn.commit()
    print('total sec: ' + str(time.time() - start_time))
    conn.close()
