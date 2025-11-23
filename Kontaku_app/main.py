import tkinter as tk
from ui import ContactApp
import os

def main():
    root = tk.Tk()
    
    #Icon Configuration
    icon_path = "Cicon.png"
    
    if os.path.exists(icon_path):
        try:
            icon = tk.PhotoImage(file=icon_path)
            root.iconphoto(True, icon)
            
            try:
                import ctypes
                myappid = 'mycompany.contactmanager.app.1.0'
                ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
            except:
                pass 
            
        except Exception as e:
            print(f"Could not load icon: {e}")

    app = ContactApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()