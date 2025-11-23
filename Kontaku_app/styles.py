from tkinter import ttk

def apply_styles():

    style = ttk.Style()
    style.theme_use('clam')

    # Color Palette
    bg_color = "#f4f6f9"         
    primary_color = "#34495e"    
    active_color = "#2c3e50"     
    accent_color = "#e74c3c"     
    text_color = "#2c3e50"       
    header_bg = "#dfe6e9"        
    header_fg = "#2d3436"        

    # General Frame & Label Styles
    style.configure("TFrame", background=bg_color)
    style.configure("TLabelFrame", background=bg_color, padding=10)
    style.configure("TLabelFrame.Label", background=bg_color, foreground=primary_color, font=("Segoe UI", 11, "bold"))
    style.configure("TLabel", background=bg_color, foreground=text_color, font=("Segoe UI", 10))
    
    # Button Styles
    style.configure("TButton", 
                    font=("Segoe UI", 10, "bold"), 
                    background=primary_color, 
                    foreground="white",
                    padding=6,
                    borderwidth=0)
    style.map("TButton", 
              background=[("active", active_color), ("pressed", active_color)],
              relief=[("pressed", "flat")])

    # Danger Button (Delete)
    style.configure("Danger.TButton", background=accent_color, foreground="white")
    style.map("Danger.TButton", background=[("active", "#c0392b")])
    
    # Separator
    style.configure("TSeparator", background="#bdc3c7")

    # Treeview Styles
    style.configure("Treeview.Heading", 
                    font=("Segoe UI", 11, "bold"), 
                    background=header_bg, 
                    foreground=header_fg,
                    relief="flat")
    
    style.configure("Treeview", 
                    background="white",
                    foreground="#2c3e50", 
                    rowheight=30,          
                    fieldbackground="white",
                    font=("Segoe UI", 10),
                    borderwidth=0)
    
    style.layout("Treeview", [('Treeview.treearea', {'sticky': 'nswe'})])
    
    style.map("Treeview", background=[("selected", "#3498db")], foreground=[("selected", "white")])
    
    return bg_color