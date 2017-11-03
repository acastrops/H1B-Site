import psycopg2

try:
    conn = psycopg2.connect("dbname='h1bdb' user='h1bdb_admin' password='f?8XwakmNbgRBxeL' host='h1bdb.cbpnpl7q4eto.us-east-2.rds.amazonaws.com'")
    print("Connected successfully")
except:
    print("Connection failed!")

cur = conn.cursor()

cur.execute("select job_title, substring(begin_date, '\d{4}') as yr, count(*) from cases group by job_title, yr limit 10;")
rows = cur.fetchall()


yeard = dict()
[yeard.update({y: []}) for y in range(2002, 2019)]
[yeard[int(r[1])].append((r[0], r[2])) for r in rows if r[1] is not None and r[1].isdigit() and int(r[1]) >= 2002]

tops = dict()

for k in range(2007, 2017):
    tops.update({k: sorted(yeard[k], key=lambda x: x[1], reverse=True)[:3]})
