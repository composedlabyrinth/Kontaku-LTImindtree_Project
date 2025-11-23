import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import re
import csv
from database import Database
from styles import apply_styles

class ContactApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Kontaku")
        self.root.geometry("1150x700")
        
        # Initialize Database
        self.db = Database()
        
        # Apply Styles
        self.bg_color = apply_styles()
        self.root.configure(bg=self.bg_color)

        # Country Codes Data
        self.country_data = {
            "India (+91)": 10,
            "USA (+1)": 10, "UK (+44)": 10, "China (+86)": 11,
            "Japan (+81)": 10, "Germany (+49)": 11, "Australia (+61)": 9,
            "Canada (+1)": 10, "Other": 0
        }
        self.country_list = list(self.country_data.keys())

        # State Variables
        self.current_category = "All"
        self.categories = ["All", "Family", "Friend", "Work", "Other"]
        
        # Form Variables
        self.selected_id = None
        self.name_var = tk.StringVar()
        self.country_code_var = tk.StringVar()
        self.phone_var = tk.StringVar()
        self.email_var = tk.StringVar()
        self.address_var = tk.StringVar()
        self.category_var = tk.StringVar()
        self.search_var = tk.StringVar()

        self._setup_ui()
        self.populate_list()

    def _setup_ui(self):
        """Builds the UI components."""
        vcmd = (self.root.register(self.validate_number_input), '%P')

        # Top Header Frame
        header_frame = ttk.Frame(self.root, padding="15 15 15 5") # Top padding for breathing room
        header_frame.pack(side=tk.TOP, fill=tk.X)
        
        # Main Title
        self.title_label = ttk.Label(header_frame, text="Kontaku", font=("Segoe UI", 20, "bold"), foreground="#2c3e50")
        self.title_label.pack(side=tk.LEFT)
        
        self.subtitle_label = ttk.Label(header_frame, text=" | All Contacts", font=("Segoe UI", 14), foreground="#7f8c8d")
        self.subtitle_label.pack(side=tk.LEFT, pady=(8, 0)) # Align visually with title

        # Search Bar Area
        search_frame = ttk.Frame(header_frame)
        search_frame.pack(side=tk.RIGHT)
        ttk.Entry(search_frame, textvariable=self.search_var, width=30).pack(side=tk.LEFT, padx=5)
        ttk.Button(search_frame, text="Search", command=self.search_contact).pack(side=tk.LEFT)
        ttk.Button(search_frame, text="Reset", command=self.reset_search).pack(side=tk.LEFT, padx=5)

        # Main Body
        body_frame = ttk.Frame(self.root, padding="15")
        body_frame.pack(fill=tk.BOTH, expand=True)

        # Sidebar (Navigation)
        sidebar = ttk.Frame(body_frame, width=180)
        sidebar.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 15))
        
        ttk.Label(sidebar, text="GROUPS", font=("Segoe UI", 9, "bold"), foreground="#95a5a6").pack(pady=(0, 10), anchor="w")
        
        for cat in self.categories:
            btn = ttk.Button(
                sidebar, 
                text=f"{cat}", 
                command=lambda c=cat: self.switch_category(c),
                width=20
            )
            btn.pack(pady=3, fill=tk.X)

        ttk.Separator(sidebar, orient='horizontal').pack(fill='x', pady=15)
        
        ttk.Label(sidebar, text="ACTIONS", font=("Segoe UI", 9, "bold"), foreground="#95a5a6").pack(pady=(0, 10), anchor="w")
        ttk.Button(sidebar, text="Import CSV", command=self.import_csv).pack(pady=3, fill=tk.X)
        ttk.Button(sidebar, text="Export Page", command=self.export_csv).pack(pady=3, fill=tk.X)

        # Content Area
        content_frame = ttk.Frame(body_frame)
        content_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        form_frame = ttk.LabelFrame(content_frame, text="Contact Details", padding="15")
        form_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 15))

        ttk.Label(form_frame, text="Full Name").pack(anchor="w")
        ttk.Entry(form_frame, textvariable=self.name_var, width=30).pack(fill=tk.X, pady=(0, 10))

        ttk.Label(form_frame, text="Phone Number").pack(anchor="w")
        phone_frame = ttk.Frame(form_frame)
        phone_frame.pack(fill=tk.X, pady=(0, 10))
        
        code_cb = ttk.Combobox(phone_frame, textvariable=self.country_code_var, values=self.country_list, state="readonly", width=12)
        code_cb.pack(side=tk.LEFT, padx=(0, 5))
        
        try:
            india_index = self.country_list.index("India (+91)")
            code_cb.current(india_index)
        except ValueError:
            code_cb.current(0)         
        phone_entry = ttk.Entry(phone_frame, textvariable=self.phone_var, width=16, validate="key", validatecommand=vcmd)
        phone_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)

        ttk.Label(form_frame, text="Email Address").pack(anchor="w")
        ttk.Entry(form_frame, textvariable=self.email_var, width=30).pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(form_frame, text="Address").pack(anchor="w")
        ttk.Entry(form_frame, textvariable=self.address_var, width=30).pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(form_frame, text="Category").pack(anchor="w")
        self.category_cb = ttk.Combobox(form_frame, textvariable=self.category_var, state="readonly", values=("Family", "Friend", "Work", "Other"))
        self.category_cb.set("Other") 
        self.category_cb.pack(fill=tk.X, pady=(0, 20))

        # Action Buttons
        ttk.Button(form_frame, text="Save New Contact", command=self.add_contact).pack(fill=tk.X, pady=4)
        ttk.Button(form_frame, text="Update Selected", command=self.update_contact).pack(fill=tk.X, pady=4)
        ttk.Frame(form_frame, height=10).pack() # Spacer
        ttk.Button(form_frame, text="Delete Selected", command=self.delete_contact, style="Danger.TButton").pack(fill=tk.X, pady=4)
        ttk.Button(form_frame, text="Clear Form", command=self.clear_form).pack(fill=tk.X, pady=4)

        list_frame = ttk.Frame(content_frame)
        list_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        columns = ("sno", "name", "phone", "email", "address", "category")
        self.tree = ttk.Treeview(list_frame, columns=columns, show="headings", selectmode="extended")
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        headers = {
            "sno": "#", "name": "Name", "phone": "Phone", 
            "email": "Email", "address": "Address", "category": "Category"
        }
        widths = {
            "sno": 40, "name": 140, "phone": 130, 
            "email": 160, "address": 150, "category": 90
        }
        
        for col, title in headers.items():
            self.tree.heading(col, text=title)
            self.tree.column(col, width=widths[col], anchor="center")

        self.tree.tag_configure('oddrow', background='white')
        self.tree.tag_configure('evenrow', background='#f4f6f9')

        self.tree.bind('<<TreeviewSelect>>', self.select_item)

    def validate_number_input(self, new_value):
        if new_value == "": return True
        return new_value.isdigit()

    def validate_phone_logic(self):
        code_label = self.country_code_var.get()
        number = self.phone_var.get().strip()
        required_len = self.country_data.get(code_label, 0)
        
        if not number:
            messagebox.showerror("Validation Error", "Phone number is required.")
            return None
            
        if required_len > 0 and len(number) != required_len:
            messagebox.showerror("Validation Error", f"For {code_label}, phone number must be exactly {required_len} digits.\nYou entered {len(number)}.")
            return None
            
        code_only = code_label.split(" ")[-1] 
        full_phone = f"{code_only} {number}"
        return full_phone

    def switch_category(self, category):
        self.current_category = category
        self.subtitle_label.config(text=f" | {category} Contacts")
        self.clear_form()
        self.populate_list()

    def populate_list(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        
        if self.current_category == "All":
            data = self.db.fetch_contacts()
        else:
            data = self.db.fetch_by_category(self.current_category)

        for index, row in enumerate(data, start=1):
            db_id = row[0]
            display_values = (index, row[1], row[2], row[3], row[4], row[5])
            
            tag = 'evenrow' if index % 2 == 0 else 'oddrow'
            self.tree.insert("", tk.END, iid=db_id, values=display_values, tags=(tag,))

    def add_contact(self):
        name = self.name_var.get().strip()
        email = self.email_var.get().strip()
        address = self.address_var.get().strip()
        full_phone = self.validate_phone_logic()
        if not full_phone: return

        if name == "":
            messagebox.showerror("Required Fields", "Name is required")
            return
        
        if self.db.contact_exists(name):
            messagebox.showerror("Duplicate", f"A contact with '{name}' already exists.")
            return
        
        self.db.add_contact(name, full_phone, email, address, self.category_var.get())
        self.clear_form()
        self.populate_list()
        messagebox.showinfo("Success", "Contact Added")

    def select_item(self, event):
        try:
            if not self.tree.selection(): return
            selected_iid = self.tree.selection()[0]
            self.selected_id = selected_iid
            row = self.tree.item(selected_iid)['values']
            
            self.name_var.set(row[1])
            raw_phone = str(row[2]) 
            parts = raw_phone.split(" ")
            if len(parts) >= 2 and parts[0].startswith("(+"):
                code_part = parts[0] 
                number_part = parts[1]
                found_code = False
                for label in self.country_list:
                    if label.endswith(code_part):
                        self.country_code_var.set(label)
                        found_code = True
                        break
                if not found_code:
                    self.country_code_var.set("India (+91)")
                self.phone_var.set(number_part)
            else:
                self.country_code_var.set("India (+91)")
                self.phone_var.set(raw_phone)

            self.email_var.set(row[3])
            self.address_var.set(row[4]) 
            self.category_var.set(row[5])
        except IndexError:
            pass

    def update_contact(self):
        if len(self.tree.selection()) > 1:
            messagebox.showwarning("Multiple Selection", "Please select one contact to update.")
            return

        if not self.selected_id:
            messagebox.showwarning("Selection", "Please select a contact to update")
            return
            
        name = self.name_var.get().strip()
        email = self.email_var.get().strip()
        address = self.address_var.get().strip()
        full_phone = self.validate_phone_logic()
        if not full_phone: return
        
        if name == "":
             messagebox.showerror("Required Fields", "Name is required")
             return

        self.db.update_contact(self.selected_id, name, full_phone, email, address, self.category_var.get())
        self.clear_form()
        self.populate_list()
        messagebox.showinfo("Success", "Contact Updated")

    def delete_contact(self):
        selected_items = self.tree.selection()
        if not selected_items:
            messagebox.showwarning("Selection", "Please select contact(s) to delete")
            return
        
        count = len(selected_items)
        confirm = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete {count} contact(s)?")
        if confirm:
            for iid in selected_items:
                self.db.remove_contact(iid)
            self.clear_form()
            self.populate_list()

    def clear_form(self):
        self.selected_id = None
        self.name_var.set("")
        self.phone_var.set("")
        
        try:
            self.country_code_var.set("India (+91)")
        except:
            self.country_code_var.set(self.country_list[0])
            
        self.email_var.set("")
        self.address_var.set("")
        self.category_var.set("Other") 
        self.tree.selection_remove(self.tree.selection())

    def search_contact(self):
        query = self.search_var.get().strip()
        if not query: return
        for i in self.tree.get_children():
            self.tree.delete(i)
        data = self.db.search_contacts(query)
        for index, row in enumerate(data, start=1):
            db_id = row[0]
            display_values = (index, row[1], row[2], row[3], row[4], row[5])
            
            tag = 'evenrow' if index % 2 == 0 else 'oddrow'
            self.tree.insert("", tk.END, iid=db_id, values=display_values, tags=(tag,))

    def reset_search(self):
        self.search_var.set("")
        self.populate_list()

    def export_csv(self):
        if self.current_category == "All":
            rows = self.db.fetch_contacts()
            filename = "kontaku_all_export.csv"
        else:
            rows = self.db.fetch_by_category(self.current_category)
            filename = f"kontaku_{self.current_category.lower()}_export.csv"
        
        if not rows:
            messagebox.showwarning("Export", "No contacts to export in this view.")
            return

        try:
            with open(filename, "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(["ID", "Name", "Phone", "Email", "Address", "Category"])
                writer.writerows(rows)
            messagebox.showinfo("Export Success", f"Exported {len(rows)} contacts to:\n{filename}")
        except PermissionError:
            messagebox.showerror("Permission Error", f"Could not save to '{filename}'.\nIt might be open in Excel.\nPlease close it.")
        except Exception as e:
            messagebox.showerror("Export Error", f"Could not save file:\n{e}")

    def import_csv(self):
        file_path = filedialog.askopenfilename(title="Select CSV File", filetypes=[("CSV Files", "*.csv")])
        if not file_path: return

        success_count = 0
        skip_count = 0
        encodings = ['utf-8', 'latin-1', 'cp1252']
        
        for enc in encodings:
            try:
                with open(file_path, "r", newline="", encoding=enc) as f:
                    reader = csv.DictReader(f)
                    if not reader.fieldnames: raise ValueError("Empty file")
                    
                    def get_col_val(row, target_keys):
                        for key in row.keys():
                            if key and key.lower() in target_keys: return row[key]
                        return ""

                    for row in reader:
                        name = get_col_val(row, ["name"]).strip()
                        phone = get_col_val(row, ["phone", "number"]).strip()
                        if not name or not phone: continue

                        email = get_col_val(row, ["email"]).strip()
                        address = get_col_val(row, ["address"]).strip()
                        category = get_col_val(row, ["category"]).strip()
                        valid_cats = ["Family", "Friend", "Work", "Other"]
                        if category not in valid_cats: category = "Other"

                        if self.db.contact_exists(name):
                            skip_count += 1
                            continue
                        self.db.add_contact(name, phone, email, address, category)
                        success_count += 1
                
                self.populate_list()
                messagebox.showinfo("Import Result", f"Imported: {success_count}\nSkipped: {skip_count}")
                return
            except UnicodeDecodeError: continue
            except Exception as e:
                messagebox.showerror("Import Error", f"Failed to import:\n{e}")
                return
        messagebox.showerror("Import Error", "Could not decode file.")