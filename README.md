# Pytaxes #

A program/library to manage a hash table for taxcards.
Please note that this is a school project so it probably wont be maintained

## Usage ##

To install just run

    python setup.py install

Then to fire up the server for the ui run\

    pytaxes-webui

After that open a browser window to localhost:8080 and you will se a nice inteface for pytaxes.

### User Interface ###

In the file we have a list of lines of the form

    <id>;<year>;<year day>;<cost>;<vendor code>;<;-separated products>

each of which represents a card to be imported. Whenever a file is
uploaded all previous entries are erased.

#### Search Bar ####

The search bar can either search or pass a command. Searching works
like this:

You pass the search terms in the form `<which column to search>
<whatto search for>` for example you may have `cost 200` which will
search for costs of 200. You may have many space separated search
terms which will pe connected with logical or and many column-tems
pairs that will be connected with logical and. If no column name is
stated at the beginning we search for ids. For example:

    aaaaabbbbbaaaaabbbbbbbbbb aaaaaaaaaaaaaaaaaaaaaaa date 22/3/2011 27/2/2013 cost 200 300

will search for ids aaaaabbbbbaaaaabbbbbbbbbb and
aaaaaaaaaaaaaaaaaaaaaaa, from those we will search for dates ranging
from 22/3/2011 or 27/2/2003 and from those we will only keep costs of
200 or 300.

Note the behaviour of the dates. Single numbers are interpereted as
years and otherwise d/m/y format is expected. We can use '-' or 'to'
(with spaces around them) to indicate date ranges. Date ranges are
always inclusive.

Some commands are also available. If you type 'help' info will tell you some of them. Commands are intentionally not too user friendly but they are there so that's cool.

* `help` - Help
* `ADD <file-style card representation>` - Add a card
* `DEL <card id>` - Delete a card
* `stats` - Show some stats of the hash table
* `toggle duplicate silence` - It is quite logical to show big red errors in case of cards that are duplicates, well it seems that the test files contain 2 in 3 duplicates so that would FLOOOOOOD things up each time such a file is uploaded. Do this to actually show the silenced errors
