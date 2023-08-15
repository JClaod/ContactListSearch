# First mini project

class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end_of_word = False
        self.counter = 1

class Trie:
    def __init__(self):
        self.root = TrieNode()
        
    def add(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node.counter +=1
            node = node.children[char]
        node.is_end_of_word = True
        node.counter += 1
    
    def remove(self, word):
        node = self.root
        nodes_stack = []

        for char in word:
            node.counter -= 1
            nodes_stack.append(node)
            node = node.children[char]

        node.counter -= 1
        node.is_end_of_word = False

        if bool(node.children) or node.counter > 1:
            return

        for i in range(len(word) - 1, -1, -1):
            char = word[i]
            parent_node = nodes_stack.pop()
            if parent_node.is_end_of_word or len(parent_node.children) > 1:
                parent_node.counter -= 1
                del parent_node.children[char]
                return
            
        else:
            del self.root.children[word[0]]

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
        self.information = []
    
    def new_contact(self, name, company, number, email):
        self.list_of_names.add(name.lower())

        contact_info = {
            "Company": company,
            "Phone Number": number,
            "Email": email
        }
        self.information.append([name, contact_info])
    
    def possible_contacts(self, input):
        return self.list_of_names.contacts_list(input)
    
    def remove_contact(self, name):
        lower_name = name[0].lower()
        if name in self.information: 
            self.information.remove(name)
            self.list_of_names.remove(lower_name)
    
    def change_contact(self, name, input):
        if name in self.information:
            self.list_of_names.add(input.lower())
            updated_contact = [input, name[1]]
            self.information.append(updated_contact)
            self.remove_contact(name)
            return updated_contact
    

    def contact_access(self, name):
        if name in self.information:
            full_information = (
                "Name: " + str(name) + "\n" +
                "Company: " + str(self.information[name]["Company"]) + "\n" +
                "Phone Number: " + str(self.information[name]["Phone Number"]) + "\n" +
                "Email: " + str(self.information[name]["Email"])
            )
        return full_information

    def update_information(self, name, type, input):
            contact_info = name[1]
            contact_info[type] = input
    
    def valid_information_type(self, type, input):
        if type == "Name":
            if input == "":
                return False
        
        if type == "Phone Number":
            if input == "":
                return True
            
            if len(str(input)) != 10:
                return False
            
            for char in input:
                if not char.isdigit():
                    return False
        
        # only checks for name and first TLD
        if type == "Email":
            if input == "":
                return True
            
            if "@" not in input or "." not in input:
                return False
            
            at_sign_index = input.index("@")
            dot_sign_index = input.index(".")

            if at_sign_index == 0 or dot_sign_index == at_sign_index - 1:
                return False

            username = input[:at_sign_index]

            dot_count = 0
            for char in username:
                if char == ".":
                    dot_count += 1
                if dot_count > 1:
                    return False
                else:
                    dot_count = 0

            second_half = input[at_sign_index:]

            if second_half.count('.') > 1:
                return False

            input = input[at_sign_index: ]
            at_sign_index = input.index("@")
            dot_sign_index = input.index(".")

            local_part = input[at_sign_index + 1: dot_sign_index]
            domain_part = input[dot_sign_index + 1:]

            invalid_chars = "!#$%&'*+-/=?^_`{|"
            
            # short list of valid domains
            valid_domains = [
                "com",
                "org",
                "net",
                "edu",
                "gov",
                "mil",
                "info",
                "biz",
                "io",
                "co",
                "tv",
                "me",
                "name",
                "pro",
                "travel",
                "museum",
            ]
                
            if any(char in invalid_chars for char in local_part):
                return False
            
            if domain_part not in valid_domains:
                return False
            
        return True
    
    def phone_number_format(self, number):
        number = str(number)
        number_format = ""

        first_three = number[0:3]
        middle_three = number[3:6]
        last_four = number[6:]

        number_format += "("

        for num in first_three:
            number_format += str(num)

        number_format += ")"

        for num in middle_three:
            number_format += str(num)
        
        number_format += "-"

        for num in last_four:
            number_format += str(num)

        return number_format


