# sql-index-demo

The code behind the video **[Why one database index makes a slow query fast (SQLite demo)](https://youtu.be/QX29qif9-c0)** on [Show Me the Query](https://www.youtube.com/@ShowMeTheQuery).

One `CREATE INDEX` turns a query that scans a million rows into one that jumps straight to the 13 rows it needs.

## Run it

You only need Python 3. The script uses the standard library only, with no installs.

```bash
python3 index_demo.py
```

It builds an in-memory SQLite table of 1,000,000 orders (fixed seed, so you get the same rows we did). It then runs the same query before and after adding an index, printing the query plan and the average time over 50 runs.

## What we got

From [`sample-output.txt`](sample-output.txt):

```
sqlite 3.53.1 | python 3.13.18 | rows 1000000
result: (13, 2797.32)
plan (no index):   ['SCAN orders']
avg time (no index): 23.761 ms
index build: 325 ms
plan (with index): ['SEARCH orders USING INDEX idx_orders_customer (customer_id=?)']
avg time (with index): 0.004 ms
```

These numbers come from a single run on a 2-vCPU cloud VM with an in-memory database. **Your numbers will differ.** Hardware, an on-disk database or another engine will all change them. The result that holds everywhere is the plan: **SCAN** (every row) becomes **SEARCH** (only the matching rows).

## What's in here

| File | What it is |
|---|---|
| [`index_demo.py`](index_demo.py) | The demo from the video: plan + timing, before and after the index |
| [`sample-output.txt`](sample-output.txt) | The exact output shown in the video |
| [`pov-version/before_index.py`](pov-version/before_index.py) | Step-by-step version without the index |
| [`pov-version/after_index.py`](pov-version/after_index.py) | The same file plus the single `CREATE INDEX` line |

## Try this next

- Add `EXPLAIN QUERY PLAN` in front of your own slow queries and look for `SCAN`.
- Index a column you **don't** filter on, and confirm the plan doesn't change.
- Time 100,000 `INSERT`s with zero, one and three indexes to see the write cost.

## Sources

- [SQLite: Query Planning](https://www.sqlite.org/queryplanner.html)
- [SQLite: EXPLAIN QUERY PLAN](https://www.sqlite.org/eqp.html)
- [SQLite: Database File Format (b-trees)](https://www.sqlite.org/fileformat2.html)
- [PostgreSQL: Indexes, Introduction](https://www.postgresql.org/docs/current/indexes-intro.html)

## License

MIT. See [LICENSE](LICENSE).
