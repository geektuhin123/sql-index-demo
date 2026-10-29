"""Demo for the "Show Me the Query" video (https://youtu.be/QX29qif9-c0): the same lookup with and without an index (SQLite)."""
import random, sqlite3, sys, time

N = 1_000_000
random.seed(42)
con = sqlite3.connect(":memory:")
con.execute("CREATE TABLE orders (id INTEGER PRIMARY KEY, customer_id INTEGER, total REAL)")
con.executemany("INSERT INTO orders (customer_id, total) VALUES (?, ?)",
                ((random.randint(1, 100_000), round(random.uniform(5, 500), 2)) for _ in range(N)))
con.commit()
Q = "SELECT COUNT(*), SUM(total) FROM orders WHERE customer_id = ?"

def plan():
    return [r[3] for r in con.execute("EXPLAIN QUERY PLAN " + Q, (4242,))]

def timed(reps=50):
    t = time.perf_counter()
    for _ in range(reps):
        con.execute(Q, (4242,)).fetchone()
    return (time.perf_counter() - t) / reps * 1000

print("sqlite", sqlite3.sqlite_version, "| python", sys.version.split()[0], "| rows", N)
print("result:", con.execute(Q, (4242,)).fetchone())
print("plan (no index):  ", plan())
print(f"avg time (no index): {timed():.3f} ms")
t = time.perf_counter(); con.execute("CREATE INDEX idx_orders_customer ON orders(customer_id)")
print(f"index build: {(time.perf_counter()-t)*1000:.0f} ms")
print("plan (with index):", plan())
print(f"avg time (with index): {timed():.3f} ms")
