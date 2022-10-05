#CSC435Assignment5

Simple web server that handles one HTTP request at a time.

Methods: Handles only GET requests Returns a HTTP response 200 OK and the requested resource if successful and 404 Not Found in the event the resource is unavailable.
If a non-GET request is received the server reponds with a 400 Bad Request.
In both the 404 and 400 case there is an error html page returned.
Requests are also logged in the Common Log Format

Instructions: Server is to be launched from the command line and has the following command line flags. -p used to declare the port the server will be bound to and is required -h used to give the help menu to explain operation and other command line flags
Pages are accessed via a browser via the loopbvack IP addresss and the selected port.


Notes: Potential areas for improvement are the handling of the GET request. There may be a more efficient way to parse the incoming request aside from the string proceiing done in the current version.
Some of the code in the GET and inavlid handling may be redundant and could be merged with some refactoring.

Likewise the construction of the GET response may be better handled than the try except structure and the string manipulation currently used.

A deficiency in the code is that it does not include the UTC offset in the date time part of the code.
