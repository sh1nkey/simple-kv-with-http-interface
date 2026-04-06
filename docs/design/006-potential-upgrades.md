A list of potential upgrades i can come up with:
- try mypyc compilation for better performance
- try free threading for TCP server for better performance
- do a cron-task to clean duplicated while kvdb is working, not only after launch
- faster serialization via C-extensions or libraries like msgspec or orjson
- add healthcheck endpoint for faster start
- support using .pyi files for typing and docs for people who would import it as a library