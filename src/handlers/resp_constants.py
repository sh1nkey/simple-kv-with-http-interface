RESPONSE_NOT_FOUND = (
    "HTTP/1.1 404 Not Found\r\n"
    "Content-Length: 0\r\n"
    "Content-Type: text/plain\r\n"
    "Connection: close\r\n"
    "\r\n"
).encode()


RESPONSE_GET_SUCCESS = (
    "HTTP/1.1 200 OK\r\n"
    "Content-Length: {}\r\n"
    "Content-Type: text/plain\r\n"
    "Connection: close\r\n"
    "\r\n"
)

RESPONSE_SET_SUCCESS = (
    "HTTP/1.1 202 Accepted\r\n"
    "Content-Length: 0\r\n"
    "Content-Type: text/plain\r\n"
    "Connection: close\r\n"
    "\r\n"
).encode()

RESPONSE_ERR = (
    "HTTP/1.1 500 Internal Server Error\r\n"
    "Content-Length: 0\r\n"
    "Content-Type: text/plain\r\n"
    "Connection: close\r\n"
    "\r\n"
).encode()
