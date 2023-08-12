# First mini project
import keyboard

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
    
    def remove(self, word):
        node = self.root
        copy_node = node
        counter = 0

        for char in word:
            if len(node.children) > 1:
                counter += 1
            node = node.children[char]
        
        new_counter = 0
        for char in word:
            if len(copy_node.children) > 1:
                new_counter += 1
            
            if new_counter == counter:
                del copy_node.children[char]
                break
            
            copy_node = copy_node.children[char]
            
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
    
    def new_contact(self, name, company, number, email):
        self.list_of_names.add(name)

        self.information[name] = {
            "Company": company,
            "Phone Number": number,
            "Email": email
        }
    
    def possible_contacts(self, input):
        return self.list_of_names.contacts_list(input)
    
    def remove_contact(self, name):
        if name in self.information:
            del self.information[name]
            self.list_of_names.remove(name)
    
    def change_contact(self, name, input):
        if name in self.information:
            self.list_of_names.add(input)
            self.information[input] = self.information[name]
            self.remove_contact(name)
    

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
        if name not in self.information:
            return
        
        if type not in self.information[name]:
            return
        
        else:
            self.information[name][type] = input
    
    def valid_information_type(self, type, input):
        if input == "N/A":
            return True
        
        if type == "Phone Number":
            if len(input) != 10:
                return False
        
        # only checks for name and first TLD
        if type == "Email":
            if "@" not in input or "." not in input:
                return False
            
            at_sign_index = input.index("@")
            dot_sign_index = input.index(".")

            if at_sign_index == 0 or dot_sign_index <= at_sign_index + 1:
                return False
            
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
        
            if local_part.count('.') > 1:
                return False
            
            if domain_part not in valid_domains:
                return False
            
            return True
    
    def phone_number_format(self, number):
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








contact_list = ContactList()

while True:
    print("-------------------------------------Contact List-------------------------------------")
    
    choice = input("Would you like to (create, access, update) a contact or exit? : ")
    
    if choice == "create":
        print("----------------------------------------Create----------------------------------------")
        print("If there is no information to add to the contact besides the name please enter 'N/A'.")
        print("")
        
        name = input("Please enter the name of the contact: ")
        while name in contact_list.information:
            name = input("Contact already exits, enter a new contact name: ")

        company = input("Please enter the company of the contact: ")
        
        number = input("Please enter a phone number: ")
        while contact_list.valid_information_type("Phone Number", number) == False:
            number = input("Please enter a valid phone number: ")
        number = contact_list.phone_number_format(number)

        email = input("Please enter an email address: ")
        while contact_list.valid_information_type("Email", email) == False:
            email = input("Please enter a valid email address: ")
        
        contact_list.new_contact(name, company, number, email)
    
    if choice == "access":
        print("----------------------------------------Access----------------------------------------")
        print("Will autocomplete from contacts if you cannot find whole name")
        print("")
        while True:
            user_input = input("Enter name: ")
            if user_input == "esc":
                break
            contact = contact_list.possible_contacts(user_input)
            print("Possible contacts:", contact)

            if len(contact) == 1:
                print("-------------------------------------------------------------------------------------")
                print(contact_list.contact_access(contact[0]))
                break
    
    if choice == "update":
        print("----------------------------------------Update----------------------------------------")
        print("Will autocomplete from contacts if you cannot find whole name")
        print("")
        
        user_input = ""

        while True:
            user_input = input("Enter name: ")
            if user_input == "esc":
                break
            contact = contact_list.possible_contacts(user_input)
            print("Possible contacts:", contact)
            
            if len(contact) == 1:
                break
        
        print("")

        while True:
            sub_choice = input("Do you want to update (Name, Company, Number, Email) or exit: ").lower()
            
            if sub_choice == "name":
                change = input("What do you want to change the contact name to? ")
                while change in contact_list.information:
                    change = input("Contact already exits, enter a new contact name: ")
                contact_list.change_contact(contact[0], change)
                print("")
                print(contact_list.contact_access(change))
                print("")
            
            if sub_choice == "company":
                change = input("What do you want to change the company to? ")
                contact_list.update_information(contact[0], "Company", change)
                print("")
                print(contact_list.contact_access(contact[0]))
                print("")
                    
            if sub_choice == "number":
                change = input("What do you want to change the number to? ")
                while contact_list.valid_information_type("Phone Number", change) == False:
                    change = input("Please enter a valid phone number: ")
                contact_list.update_information(contact[0], "Number", contact_list.phone_number_format(change))
                print("")
                print(contact_list.contact_access(contact[0]))
                print("")
                    
            if sub_choice == "email":
                change = input("What do you want to change the email to? ")
                while contact_list.valid_information_type("Email", email) == False:
                    email = input("Please enter a valid email address: ")
                contact_list.update_information(contact[0], "Email", change)
                print("")
                print(contact_list.contact_access(contact[0]))
                print("")
            
            if sub_choice == "exit":
                break
        
    if choice == "exit":
        break


