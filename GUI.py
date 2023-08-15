import tkinter as tk
from tkinter import font
from tkinter import ttk
from main import ContactList


# Accessing the word file for contact information and storing them

##################
# Window Classes #
##################

class ContactsApp:
    def __init__(self, window, contact_list):
        self.window = window
        self.window.title("Contact List")
        self.contact_list = contact_list

        custom_font = font.Font(family="Helvetica", size=20, weight="bold")
        header = tk.Label(self.window, text="Contacts", height=2, font=custom_font)
        header.pack()

        self.search_var = tk.StringVar()
        self.search_var.trace_add("write", self.update_contacts_list)

        self.search_entry = tk.Entry(self.window, textvariable=self.search_var)
        self.search_entry.pack(padx=10, pady=10)

        contacts_scrollbar = tk.Scrollbar(self.window)
        contacts_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.contacts_listbox = tk.Listbox(self.window, height=380, width=30, yscrollcommand=contacts_scrollbar.set)
        self.contacts_listbox.pack(padx=10, pady=5)

        contacts_scrollbar.config(command=self.contacts_listbox.yview)

        self.create_contact_button = tk.Button(self.window, text="+", width=5, height=2, font=10, command=self.create_contact)
        self.create_contact_button.place(x=350, y=0)

        self.contacts_listbox.bind("<Double-Button-1>", self.listbox_item_double_click)

        self.update_contacts_list()
    
    def listbox_item_double_click(self, event):
        selected_index = self.contacts_listbox.curselection()
        if selected_index:
            selected_contact_name = self.contacts_listbox.get(selected_index[0])  # Get the selected contact name
            selected_contact = None

            # Find the contact in the contact list by matching the name
            for contact in self.contact_list.information:
                if contact[0].lower() == selected_contact_name.lower():
                    selected_contact = contact
                    break

            if selected_contact:
                self.access_contact(selected_contact)
    
    def access_contact(self, contact):
        access_window = ContactAccessWindow(self.window, self.contact_list, contact, self)
        self.window.wait_window(access_window.window)

        # After the access window is closed, update the information in the listbox
        selected_index = self.contacts_listbox.curselection()
        if selected_index:
            self.contacts_listbox.delete(selected_index)
            self.contacts_listbox.insert(selected_index, access_window.contact_name.capitalize())

    def update_contacts_list(self, *args):
        input_text = self.search_var.get().lower()
        contacts = self.contact_list.possible_contacts(input_text)

        self.contacts_listbox.delete(0, tk.END)
        for contact in sorted(contacts):
            self.contacts_listbox.insert(tk.END, contact.capitalize())

    def create_contact(self):
        new_window = ContactInputWindow(self.window, self.contact_list)
        self.window.wait_window(new_window.window)

        valid_contact = new_window.valid_contact
        if valid_contact:
            contact_name = valid_contact["Name"]
            contact_company = valid_contact["Company"]
            contact_number = valid_contact["Phone Number"]
            contact_email = valid_contact["Email"]

            self.contact_list.new_contact(contact_name, contact_company, contact_number, contact_email)
            self.update_contacts_list()
    
    def update_listbox(self):
        self.contacts_listbox.delete(0, tk.END)
        contacts = self.contact_list.possible_contacts(self.search_var.get().lower())
        for contact in sorted(contacts):
            self.contacts_listbox.insert(tk.END, contact.capitalize())


class ContactInputWindow:
    def __init__(self, parent, contact_list):
        self.parent = parent
        self.contact_list = contact_list
        self.window = tk.Toplevel(parent)
        self.window.title("Enter Contact Information")
        self.window.geometry("400x400")
        
        self.valid_contact = None

        tk.Label(self.window, text="Enter contact's name:").pack(pady=5)
        self.name_entry = tk.Entry(self.window)
        self.name_entry.pack(pady=5)

        tk.Label(self.window, text="Enter contact's company:").pack(pady=5)
        self.company_entry = tk.Entry(self.window)
        self.company_entry.pack(pady=5)

        tk.Label(self.window, text="Enter contact's phone number:").pack(pady=5)
        self.number_entry = tk.Entry(self.window)
        self.number_entry.pack(pady=5)

        tk.Label(self.window, text="Enter contact's email address:").pack(pady=5)
        self.email_entry = tk.Entry(self.window)
        self.email_entry.pack(pady=5)

        self.error_label = tk.Label(self.window, text="", fg="red")
        self.error_label.pack()

        self.submit_button = tk.Button(self.window, text="Done", command=self.validate_contact)
        self.submit_button.pack(pady=10)

        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)

    def validate_contact(self):
        name = self.name_entry.get().capitalize()
        company = str(self.company_entry.get()).capitalize()
        number = self.number_entry.get()
        email = self.email_entry.get()

        valid_name = self.contact_list.valid_information_type("Name", name)
        valid_number = self.contact_list.valid_information_type("Phone Number", number)
        valid_email = self.contact_list.valid_information_type("Email", email)

        if valid_number and valid_email and valid_name:
            number = self.contact_list.phone_number_format(number)
            self.contact_list.new_contact(name, company, number, email)
            self.valid_contact = {"Name": name, "Company": company, "Phone Number": number, "Email": email}
            self.window.destroy()

        else:
            error_message = ""
            if not valid_name:
                error_message += "Enter a name. "
            if not valid_number:
                error_message += "Invalid phone number. "
            if not valid_email:
                error_message += "Invalid email address."
            self.error_label.config(text=error_message)

    def on_closing(self):
        self.window.grab_release()
        self.valid_contact = None
        self.window.destroy()

class ContactAccessWindow:
    def __init__(self, parent, contact_list, contact, contacts_app):
        self.parent = parent
        self.contact_list = contact_list
        self.contact = contact
        self.contacts_app = contacts_app
        self.window = tk.Toplevel(parent)
        self.window.title("Enter Contact Information")
        self.window.geometry("400x400")

        self.contact_name = contact[0]
        self.contact_info = contact[1]

        self.contact_company = self.contact_info["Company"]
        self.contact_number = self.contact_info["Phone Number"]
        self.contact_email = self.contact_info["Email"]

        custom_font = font.Font(family="Helvetica", size=20, weight="bold")
        label_font = font.Font(family="Helvetica", size=10, weight="bold")

        name_label = tk.Label(self.window, text=self.contact_name, height=2, font=custom_font)
        company_label = tk.Label(self.window, text="Company:", height=2,)
        number_label = tk.Label(self.window, text="Phone Number:", height=2)
        email_label = tk.Label(self.window, text="Email:", height=2)

        self.company = tk.Label(self.window, text=self.contact_company, height=2, font=label_font)
        self.number = tk.Label(self.window, text=self.contact_number, height=2, font=label_font)
        self.email = tk.Label(self.window, text=self.contact_email, height=2, font=label_font)

        self.edit_contact_button = tk.Button(self.window, text="edit", width=5, height=2, font=10, command=self.edit_contact)

        name_label.grid(row=0, column=0, columnspan=2, sticky="w")

        company_label.place(y=70)
        self.company.place(y=95)

        number_label.place(y=130)
        self.number.place(y=155)

        email_label.place(y=190)
        self.email.place(y=215)

        self.edit_contact_button.place(x=350, y=0)

    def edit_contact(self):
        new_window = UpdateContactWindow(self.window, self.contact_list, self.contact, self.contacts_app, self)
        self.window.wait_window(new_window.window)
        if new_window.updated_contact_info:
            self.contact_company, self.contact_number, self.contact_email = new_window.updated_contact_info
            self.update_contact_info(self.contact_company, self.contact_number, self.contact_email)
    
    def update_contact_info(self, company, number, email):
        self.contact_company = company
        self.contact_number = number
        self.contact_email = email

        # Update the displayed labels with new information
        self.company.config(text=self.contact_company)
        self.number.config(text=self.contact_number)
        self.email.config(text=self.contact_email)
        
class UpdateContactWindow:
    def __init__(self, parent, contact_list, contact, contacts_app, access_app):
        self.parent = parent
        self.contact_list = contact_list
        self.contact = contact
        self.contacts_app = contacts_app
        self.access_app = access_app
        self.window = tk.Toplevel(parent)
        self.window.title("Update Contact Information")
        self.window.geometry("400x400")

        # Keeps track of the original contactd
        self.copy_contact = contact

        self.updated_contact_info = None

        custom_font = font.Font(family="Helvetica", size=20, weight="bold")
        sub_font = font.Font(family="Helvetica", size=20)

        title = tk.Label(self.window, text="Update: ", height=2, font=custom_font)
        contact_name = tk.Label(self.window, text=contact[0], height=2, font=sub_font)
        
        title.place(y=30)
        contact_name.place(x=120, y=30)

        name_header = tk.Label(self.window, text="Name", height=2)
        company_header = tk.Label(self.window, text="Company", height=2)
        number_header = tk.Label(self.window, text="Phone Number", height=2)
        email_header = tk.Label(self.window, text="Email", height=2)

        self.name_box = EditableBox(self.window, self.access_app.contact_name, row=2)
        self.company_box = EditableBox(self.window, self.access_app.contact_company, row=3)
        self.number_box = EditableBox(self.window, self.access_app.contact_number, row=4)
        self.email_box = EditableBox(self.window, self.access_app.contact_email, row=5)

        name_header.place(y=90)
        company_header.place(y=150)
        number_header.place(y=210)
        email_header.place(y=270)
        self.name_box.frame.place(y=120)
        self.company_box.frame.place(y=180)
        self.number_box.frame.place(y=240)
        self.email_box.frame.place(y=300)

        self.remove_contact_button = tk.Button(self.window, text="remove", width=16, height=1, command=self.remove)
        self.remove_contact_button.place(x=0, y=350)

        self.done_button = tk.Button(self.window, text="done", width=5, height=2, command=self.validate_contact)
        self.done_button.place(x=360)

        self.cancel_button = tk.Button(self.window, text="cancel", width=5, height=2, command=self.cancel)
        self.cancel_button.place(x=0, y=0)

        self.error_label = tk.Label(self.window, text="", fg="red")
        self.error_label.place(x=200, y=150)
    
    def basic_phone_format(self, number):
        basic = ""
        for char in number:
            if char.isdigit():
                basic += char
        
        return basic

    def cancel(self):
        self.contact = self.copy_contact
        self.window.destroy()

    def remove(self):
        self.contact_list.remove_contact(self.contact) 
        self.access_app.window.destroy()
        self.window.destroy()
    
    def validate_contact(self):
        name = self.name_box.get_entry_content().capitalize()
        company = str(self.company_box.get_entry_content()).capitalize()
        number = self.basic_phone_format(self.number_box.get_entry_content())
        email = self.email_box.get_entry_content()

        valid_name = self.contact_list.valid_information_type("Name", name)
        valid_number = self.contact_list.valid_information_type("Phone Number", number)
        valid_email = self.contact_list.valid_information_type("Email", email)

        if valid_name and valid_number and valid_email:
            if self.access_app.contact_name != name:
                name_change = self.contact_list.change_contact(self.contact, name)
                self.contact = name_change
            number = self.contact_list.update_information(self.contact, "Phone Number", self.contact_list.phone_number_format(number))
            company = self.contact_list.update_information(self.contact, "Company", company)
            email = self.contact_list.update_information(self.contact, "Email", email)

            self.contacts_app.update_listbox()

            self.access_app.window.destroy()
            self.window.destroy()
    

        else:
            error_message = ""
            if not valid_name:
                error_message += "Enter a name. \n"
            if not valid_number:
                error_message += "Invalid phone number.\n"
            if not valid_email:
                error_message += "Invalid email address."
            self.error_label.config(text=error_message)

#############################
# Components within Windows #
#############################

class EditableBox:
    def __init__(self, root, initial_text, row):
        self.root = root
        self.frame = tk.Frame(root)
        
        self.label = tk.Label(self.frame, text=initial_text)
        self.entry = tk.Entry(self.frame)
        self.entry.grid(row=0, column=0, padx=5, pady=5)
        
        self.edit_button = tk.Button(self.frame, text="Edit", command=self.toggle_edit)
        self.edit_button.grid(row=0, column=1, padx=5, pady=5)
        
        self.is_editing = False
        self.toggle_edit()

    def toggle_edit(self):
        self.is_editing = not self.is_editing
        if self.is_editing:
            self.entry.delete(0, tk.END)
            self.entry.insert(0, self.label.cget("text"))
        else:
            updated_text = self.entry.get()
            self.label.config(text=updated_text)
        self.update_display()

    def update_display(self):
        self.entry.grid()
        self.edit_button.config(text="Save" if self.is_editing else "Edit")
    
    def get_entry_content(self):
        return self.entry.get()

###############
# Main window #
###############

def main():
    window = tk.Tk()
    window.title("Contact List")
    window.geometry("400x400")

    contact_list = ContactList()

    # Load contacts from the file
    with open('List.html', 'r') as file:
        for line in file:
            elements = line.strip().split()

            file_name = elements[0].capitalize()
            file_company = str(elements[1]).capitalize()
            file_phone_number = contact_list.phone_number_format(elements[2])
            file_email = elements[3]
            contact_list.new_contact(file_name, file_company, file_phone_number, file_email)

    ContactsApp(window, contact_list)
    window.mainloop()

if __name__ == "__main__":
    main()