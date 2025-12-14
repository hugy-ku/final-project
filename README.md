# Crypto Dashboard  
Dashboard for Cryptocurrencies (Final Project)  
  
## File system  
- crypto_board.py  
- order_book_manager.py  
- order_book_panel.py  
- overview_manager.py  
- overview_panel.py  
- preferences.txt  
- socket_manager.py  
- title_bar.py  
  
Everything is in one directory mainly to allow convenient testing (see How to run).  
  
## File descriptions  
  
### crypto_board.py  
Main program. Uses title_bar.py, overview_manager.py, and order_book_manager.py.  
Handles the mainloop, user input processing, and saving/loading.  
  
### title_bar.py  
Title bar for the program.  
Handles buttons for user input and sends events to crypto_board.py.  
  
### overview_manager.py  
Manages overview panels. Uses overview_panel.py.  
Handles loading, unloading, and positioning (using grid) for overview panels.  
  
### overview_panel.py  
An overview panel. Uses socket_manager.py.  
Handles everything inside panels (status, title, current/24h prices) and its own socket connection.  
  
### socket_manager.py  
Socket manager. Takes a URL and on_message function (at minimum).  
Handles a websocket connection. mainly exists to be reused by overview_panel.py and order_book_manager.py.  
  
### order_book_manager.py  
Manages an order book for a symbol. Uses order_book_panel.py and socket_manager.py.  
Also has one of the worst inits I have ever created. (My brain has melted after coding for 5 days straight)  
Handles a websocket connection and passes the data to overview_panel.py.  
  
### order_book_panel.py  
Manages one side of the order book (bid/ask).  
Exists to slightly improve order_book_manager.py's insanity.  
  
### preferences.txt  
Automatically created. Used for user input peristence.  
Example file can be found in this repository.  
  
  
## How to run  
Copy all the Python files to the same directory and run crypto_board.py.  
Tests are found in each Python file and can be run directly.  
Note: You must implement error handling outside the class if you wish to import any class.