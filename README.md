# ContactListSearch
Goal: Create a contact list application where users can search for contacts by entering partial names. Use a trie to quickly search for and display matching contacts as the user types.

# TrieNode
For each time a new node is creates:
-Creates emtpy dictionary for potential children
-Creates bool variable to identify if its a word or not (initalized as False)
-Creates counter variable that keeps track how many times its being used

# Trie Class
Methods

add(self, word):
-Given a word it will add it to the trie

remove(self, word):
-Given a word it will remove it from the trie
-Accounts specific edges cases such as multiple of the same word and if the word is within a longer word i.e. span and spanning
-It will go down the tree then go back up to the following edge cases

contact_list(self, input)
-Implementing a dfs search it will search for all of the possible words within the trie and return a list

# ContactList Class
Methods:

Constructor:
-Carries a trie
-Creates an array containing the name and the contact information(company, phone number, email)

# GUI
Based it off of Apple's contacts list.
Implemented buttons such as creating, updating, and removing contacts.
