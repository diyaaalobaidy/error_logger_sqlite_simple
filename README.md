# error_logger_sqlite_simple
Logs errors into an sqlite3 db file and retrieve them according to given filters

Examples:
```python showLineNumbers
from logger import LoggingHandler
try:
    handler = LoggingHandler("test", "test.db", "test_table")
    raise(Exception("test0"))
except Exception as e:
    handler.log_error(e)
try:
    handler = LoggingHandler("test1", "test.db", "test_table")
    raise(Exception("test00"))
except Exception as e:
    handler.log_error(e)
try:
    handler = LoggingHandler("test2", "test.db", "test_table")
    raise(Exception("test11"))
except Exception as e:
    handler.log_error(e)
print(handler.get_logs("all"))
```
This code will create a db file called "test.db" and create a table called "test_table" and log errors in it, and will result in the following (most recent error first):
```shell
[
 {
    "id":0,
    "name":"test2",
    "date":"2022-05-25 13:54:29.161010",
    "level":"ERROR",
    "message":"test11",
    "path":"/home/user/parent/child/test.py",
    "line":14,
    "function":"<module>",
    "code":"ZAACQJ-VZBSVX"
 },
 {
    "id":2,
    "name":"test1",
    "date":"2022-05-25 13:54:09.957589",
    "level":"ERROR",
    "message":"test00",
    "path":"/home/user/parent/child/test.py",
    "line":9,
    "function":"<module>",
    "code":"OIPYPP-QDNEGC"
 },
 {
    "id":1,
    "name":"test",
    "date":"2022-05-25 13:54:04.952366",
    "level":"ERROR",
    "message":"test0",
    "path":"/home/user/parent/child/test.py",
    "line":4,
    "function":"<module>",
    "code":"WYYLSQ-NASPRS"
 }
]
```
