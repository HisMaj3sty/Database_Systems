# create db
# psql -d template1
import psycopg2
from faker import Faker
import random
# https://stackabuse.com/working-with-postgresql-in-python/
con = psycopg2.connect(database="customers", user="postgres",
                       password="18216456", host="127.0.0.1", port="5432")

print("Database opened successfully")
cur = con.cursor()




print("After indexing:")




cur.execute('''CREATE INDEX "hash index"
    ON public.customer USING hash
    (age)
    ''')

cur.execute('''CREATE INDEX "btree index"
    ON public.customer USING btree
    (name text_pattern_ops ASC NULLS LAST)
    ''')


con.commit()


cur.execute('''EXPLAIN analyze 
SELECT * FROM public.customer
WHERE age = 50''')
print('\n'.join(map(lambda x: x[0], cur.fetchall())))


cur.execute("""EXPLAIN analyze 
SELECT * FROM public.customer
WHERE name like 'A%'""")
print('\n'.join(map(lambda x: x[0], cur.fetchall())))

cur.execute("""EXPLAIN analyze 
SELECT * FROM public.customer
WHERE to_tsvector('english'::regconfig, review) @@ to_tsquery('blue')""")
print('\n'.join(map(lambda x: x[0], cur.fetchall())))








print("\n\n\n\nBefore indexing:")



cur.execute('''DROP INDEX "hash index"''')

cur.execute('''DROP INDEX "btree index"''')

con.commit()

cur.execute('''EXPLAIN analyze 
SELECT * FROM public.customer
WHERE age = 50''')
print('\n'.join(map(lambda x: x[0], cur.fetchall())))


cur.execute("""EXPLAIN analyze 
SELECT * FROM public.customer
WHERE name like 'A%'""")
print('\n'.join(map(lambda x: x[0], cur.fetchall())))




print("\n\n\n\nNo GIN or GIST:")

cur.execute("""EXPLAIN analyze 
SELECT * FROM public.customer
WHERE to_tsvector('english'::regconfig, review) @@ to_tsquery('blue')""")
print('\n'.join(map(lambda x: x[0], cur.fetchall())))


 
 
 
 
print("\n\n\n\nUsing GIN:")
 
cur.execute('''CREATE INDEX gin ON public.customer USING gin (to_tsvector('english', customer.review))''')
con.commit()

cur.execute("""EXPLAIN analyze 
SELECT * FROM public.customer
WHERE to_tsvector('english'::regconfig, review) @@ to_tsquery('blue')""")
print('\n'.join(map(lambda x: x[0], cur.fetchall())))


cur.execute('''DROP INDEX "gin" ''')
con.commit()



print("\n\n\n\nUsing GIST:")
cur.execute('''CREATE INDEX gist ON public.customer USING gist (to_tsvector('english', customer.review))''')

con.commit()


cur.execute("""EXPLAIN analyze 
SELECT * FROM public.customer
WHERE to_tsvector('english'::regconfig, review) @@ to_tsquery('blue')""")
print('\n'.join(map(lambda x: x[0], cur.fetchall())))


cur.execute('''DROP INDEX "gist" ''')
con.commit()
