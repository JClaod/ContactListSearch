# ContactListSearch
**Goal:** Create a contact list application where users can search for contacts by entering partial names. Use a trie to quickly search for and display matching contacts as the user types.

## TrieNode
For each time a new node is created:
- Creates an empty dictionary for potential children
- Creates a bool variable to identify if it's a word or not (initialized as False)
- Creates a counter variable that keeps track of how many times it's being used

## Trie Class
**Methods**

### `add(self, word)`
Given a word, it will add it to the trie.

### `remove(self, word)`
Given a word, it will remove it from the trie.
- Accounts for specific edge cases such as multiple occurrences of the same word and if the word is within a longer word (e.g., "span" and "spanning").
- It will traverse down the tree and then handle the mentioned edge cases while going back up the tree.

### `contact_list(self, input)`
Implementing a depth-first search (DFS), it will search for all of the possible words within the trie and return a list.

## ContactList Class
**Methods**

### Constructor
- Carries a trie.
- Creates an array containing the name and the contact information (company, phone number, email).

## GUI
Based on Apple's contacts list.
Implemented buttons such as creating, updating, and removing contacts.
