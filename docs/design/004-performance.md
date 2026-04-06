What about performance? You can run benchmarks with ```make bench```, but I'll do a bit of analysis myself here


For 5000 requests we need something like 2 seconds (both read and write). Both in concurrent, and in non-concurrent benchmarks
We also have to take into account, that aiohttp can influence benchmarks, since aiohttp caller is placed in the same thread as server

I've analyzed cProfile output, and it seems like the bottleneck currently is network connection management. Seems like other factors aren't that important in this case