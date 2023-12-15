import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
import tkinter.messagebox
import pandas as pd
import os
from main_backend import get_text_and_csv_files_with_paths as df_get
from search_duplicate_files import find_duplicates_within_groups as fd
from file_deletion import display_content



class FolderApp:
    def __init__(self, root):
        self.result=[]
        self.root = root
        self.root.title("Folder Selection App")
        self.root.geometry("850x600")

        # main frame
        main_frame = tk.Frame(root)
        main_frame.pack()

        # Left Frame
        left_frame = tk.Frame(main_frame)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.label1 = tk.Label(left_frame, text="Choose Folder:")
        self.label1.pack(pady=10)

        self.choose_button1 = tk.Button(left_frame, text="Choose Folder 1", command=lambda: self.choose_folder(1))
        self.choose_button1.pack(pady=10)

        self.choose_button2 = tk.Button(left_frame, text="Choose Folder 2", command=lambda: self.choose_folder(2))
        self.choose_button2.pack(pady=10)

        self.label2 = tk.Label(left_frame, text="Selected Folder 1: None")
        self.label2.pack()

        self.label3 = tk.Label(left_frame, text="Selected Folder 2: None")
        self.label3.pack()

        self.start_button = tk.Button(left_frame,relief=tk.GROOVE,text="Start", bd=8,command=self.start_process)
        self.start_button.pack(pady=10)

        self.selected_folders = [None, None]

        # Right Frame for displaying DataFrame
        self.right_frame = tk.Frame(main_frame, height=left_frame.winfo_reqheight())
        self.right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        result_label=tk.Label(self.root,text="Table will show files paths of duplicate  files ")
        result_label.pack()         
            

        
        
 
        

        def on_configure(event):
            self.canvas.configure(scrollregion=self.canvas.bbox('all'))

        # Create a canvas and add a frame to it
        self.canvas = tk.Canvas(root, width=400, height=300, scrollregion=(0, 0, 500, 500))
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)


        self.frame = tk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.frame, anchor='nw')
        #

 
                        

        # Add scrollbars to the canvas
        x_scrollbar = tk.Scrollbar(self.canvas, orient=tk.HORIZONTAL, command=self.canvas.xview)
        x_scrollbar.pack(side=tk.TOP, fill=tk.X)
        y_scrollbar = tk.Scrollbar(self.canvas, orient=tk.VERTICAL, command=self.canvas.yview)
        y_scrollbar.pack(side=tk.LEFT, fill=tk.Y)

        self.canvas.configure(xscrollcommand=x_scrollbar.set, yscrollcommand=y_scrollbar.set)
        self.canvas.bind('<Configure>', on_configure)
        
        
       #button to delete all double copies
        btn  = tk.Button(self.canvas,text="delete all copies",bd=5,command=self.delete_all_copies(self.result)) 
        btn.pack()              
        

        root.mainloop()
        
    def delete_all_copies(self,resultss):
       for results in resultss:
           deleted_file_path=[]
           for result in results:
               reault=list(result)
               if len(result)==1:
                   break 
               else :
                   os.remove(result)
                   deleted_file_path.append(result)
           tk.messagebox.showinfo('deleted',deleted_file_path)
                   
                
       

    def choose_folder(self, index):
        folder_path = filedialog.askdirectory()
        if folder_path:
            self.selected_folders[index - 1] = folder_path
            label_text = f"Selected Folder {index}: {self.selected_folders[index - 1]}"
            if index == 1:
                self.label2.config(text=label_text)
            else:
                self.label3.config(text=label_text)

    def start_process(self):
        if all(self.selected_folders):
            df = df_get(self.selected_folders)
            self.display_dataframe(df)
            self.result = fd(df["File Paths"].tolist())
            self.display_result_buttons(self.result)
            
        else:
            tk.messagebox.showinfo("Error", "Please choose both folders first.")

    def display_dataframe(self, df):

        for widget in self.right_frame.winfo_children():
            widget.destroy()
        tree = ttk.Treeview(self.right_frame)
        tree["columns"] = ("#",) + tuple(df.columns[:-1]) + ("File Path",)
        for col in tree["columns"]:
            if col == "#":
                tree.column(col, anchor="c", width=50)
            if col==None:
                tree.column(col,width=5)
            elif col == "File Path":
                tree.column(col, anchor="w", width=10000)
            else:
                tree.column(col, anchor="c", width=150)
            tree.heading(col, text=col)
        df_label=tk.Label(self.right_frame,text="files paths of file having same characters count")
        df_label.pack()

        y_scrollbar = ttk.Scrollbar(self.right_frame, orient="vertical", command=tree.yview)
        y_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        tree.configure(yscrollcommand=y_scrollbar.set)

        x_scrollbar = ttk.Scrollbar(self.right_frame, orient="horizontal", command=tree.xview)
        x_scrollbar.pack(side="bottom", fill="x")

        tree.configure(xscrollcommand=x_scrollbar.set)

        for i, (index, row) in enumerate(df.iterrows()):
            values = (i + 1,) + tuple(row[:-1]) + (", ".join(map(str, row[-1])),)
            tree.insert('', i, values=values)

        tree.pack(expand=True, fill="both")

        # Bind the on_treeview_select function to the Treeview widget
        tree.bind("<ButtonRelease-1>", lambda event, tree=tree: self.on_treeview_select(event, tree))

    def on_treeview_select(self, event, tree):
        selected_item = tree.selection()
        if selected_item:
            item_values = tree.item(selected_item, "values")
            tk.messagebox.showinfo("File_paths having same number of characters", f"file_paths:\n {item_values}")

    def display_result_buttons(self, result):
        for widget in self.frame.winfo_children():
            widget.destroy()
        for path in result:
            button = tk.Button(self.frame, text=path, command=lambda p=path: display_content(p), padx=30, anchor="w", justify="left")
            button.pack(fill="x", padx=5, pady=5, expand=True)


if __name__ == "__main__":
    app = FolderApp(tk.Tk())
    app.root.mainloop()