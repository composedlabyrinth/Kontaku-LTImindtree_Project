# Kontaku 📒

**Kontaku** is a robust and user-friendly desktop Contact Management System built using Python and Tkinter. It follows a modular MVC architecture to ensure clean code and scalability. Designed with a modern aesthetic, it provides essential tools for organizing personal and professional connections efficiently.

---

## ✨ Features

### **Modern UI**

* Clean, professional interface with striped rows, centered alignment, and responsive layout.

### **Smart Validation**

* Real-time phone number validation (rejects non-digits).
* Country-specific length checks (Default: India +91).
* Duplicate name prevention.

### **Category Management**

* Filter contacts by groups (Family, Friend, Work, Other) via a dedicated sidebar.

### **Advanced Search**

* Global search functionality to find contacts by name or phone number instantly.

### **Data Portability**

* **Import:** Bulk add contacts from CSV files with error handling.
* **Export:** Backup your data to CSV (supports exporting specific categories or the full list).

### **Batch Operations**

* Multi-select support for deleting multiple contacts at once.

### **Sorting**

* Automatic alphabetical sorting of contacts.

### **Persistent Storage**

* Uses SQLite (`contacts.db`) to save data automatically.

---

## 🛠️ Tech Stack

* **Language:** Python 3.x
* **GUI Framework:** Tkinter (ttk)
* **Database:** SQLite3
* **Style:** Custom ttk styling

---

## 📂 Project Structure

```
Kontaku-LTImindtree_Project/
│
├── kontaku_app/              # Main Application Folder
│   ├── main.py               # Application entry point
│   ├── ui.py                 # User Interface logic & Event handling
│   ├── database.py           # Database connectivity & CRUD operations
│   ├── styles.py             # Centralized UI styling and theming
│   └── Cicon.png             # Application Icon
│
└── README.md                 # Documentation
```

---

## 🚀 Installation & Run

### **Prerequisites**

* Python 3.x installed on your system.
* (Optional) No external pip packages required since it uses standard libraries.

### **Steps**

1. **Clone the repository:**

   ```bash
   git clone https://github.com/composedlabyrinth/Kontaku-LTImindtree_Project
   cd Kontaku-LTImindtree_Project/kontaku_app
   ```

2. **Prepare the Icon:**
   Ensure you have the `Cicon.png` file in the project folder for the app icon to load correctly.

3. **Run the Application:**

   ```bash
   python main.py
   ```

---

## 📖 Usage Guide

* **Adding a Contact:** Fill in the details on the left panel. The phone number field automatically formats based on the selected country code (India +91 by default).
* **Editing:** Click a contact in the list to load their details. Make changes and click **"Update Selected"**.
* **Deleting:** Select one or more rows (use **Ctrl** or **Shift**) and click **"Delete Selected"**.
* **Importing:** Click **"Import CSV"** in the sidebar. Ensure your CSV has headers: `Name, Phone, Email, Address, Category`.
* **Exporting:** Navigate to a category (e.g., *Work*) and click **"Export Page"** to save only those contacts.

---

## 📸 Project Screenshot

<img width="600" height="1400" alt="image" src="https://github.com/user-attachments/assets/aaab0cd3-d0e3-44e3-b25d-31441c9cfd71" />


---

## 🎓 Acknowledgements

This project was developed as part of the LTIMindtree Python Training Program. Special thanks to the instructors for their guidance.
