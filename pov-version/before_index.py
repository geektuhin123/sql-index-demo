import random, sqlite3, time

random.seed(42)
con = sqlite3.connect(":memory:")
con.execute("CREATE TABLE orders (id INTEGER PRIMARY KEY,"
            " customer_id INTEGER, total REAL)")
con.executemany("INSERT INTO orders (customer_id, total) VALUES (?, ?)",
    ((random.randint(1, 100_000), round(random.uniform(5, 500), 2))
     for _ in range(1_000_000)))

Q = "SELECT COUNT(*), SUM(total) FROM orders WHERE customer_id = ?"

def plan():
    return [r[3] for r in con.execute("EXPLAIN QUERY PLAN " + Q, (4242,))]

def timed(reps=50):
    t = time.perf_counter()
    for _ in range(reps):
        con.execute(Q, (4242,)).fetchone()
    return (time.perf_counter() - t) / reps * 1000

print("result:", con.execute(Q, (4242,)).fetchone())
print("plan:", plan())
print(f"avg: {timed():.3f} ms")
