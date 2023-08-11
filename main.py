# First mini project


class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end_of_word = False

class Trie:
    def __init__(self):
        self.root = TrieNode()
    
    def contains(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                return False
            node = node.children[char]
        return node.is_end_of_word
        
    def add(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end_of_word = True
    
    def contacts_list(self, input):
        contacts = []
        node = self.root

        for char in input:
            if char not in node.children:
                return contacts
            else:
                node = node.children[char]
        
        def dfs(input, node):
            input_copy = input

            if not node:
                return
            if node.is_end_of_word:
                contacts.append(input_copy)
     
            for child in node.children:
                dfs(input_copy + child, node.children[child])
        
        dfs(input, node)
        return contacts

class ContactList:
    def __init__(self):
        self.list_of_names = Trie()
        self.information = {}
    
    def new_contact(self, name, number):
        self.list_of_names.add(name)
        self.information[name] = number
    
    def possible_contacts(self, input):
        return self.list_of_names.contacts_list(input)

    def contact_access(self, name):
        full_information = name + ": " + str(self.information[name])
        return full_information




