Writes are saved on disk and in memory (dict)
CA by CAP (no replication, so no partition tolerance)

How exactly does it work? Writes on disk for durability, reads from in-memory hashmap

Why doesn't read from disk? It's much easier to read from in-memory hashmap, reading from disk will be a bit slower and trickier to implement (need to manage seek() and concurency via asyncio.Lock)

Why didn't I use aiofile for async file management? It's not really async, it uses threadpool or smth under the hood

Why didn't i use aiofiles? Benchmark showed a little difference between async file libraries and sync ones

What will happen if it will suddenly receive a burst of writes? It's fine, the in-memory queue stores write requests, 500_000 max

Are writes immidiate? No, they are eventual. That's why i use worker and queue.

Will queue collapse from unpected reason? It should not. Gracefull shutdown is implemented via finally

How does adding new values work? Just writing in at the end of the file, and update in-memory hashtable

How are old values deleted? Duplicated are deleted after restart of the program

Will kvdb accept new writes if it is being turned off due to some exception? No, it will return 500 status code, new writes will not be accepted. And kvdb will will finish already gotten tasks before stopping

