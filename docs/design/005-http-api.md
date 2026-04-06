route not found? 404.
some strange error? 500.

set success? 202.
set failed? 500.


get success? 200 with response body that is value
value not found? 404.
get failed? 500.

multiple get success? 200 with response body format [value,value]
one found, one not? 200 with response body format [value,None]
nothing found? 200 with response body format [None,None]
multiple get failed? 500.