import tkinter as tk
from tkinter.scrolledtext import ScrolledText
from tkinter.messagebox import Message
import os


    
def delete_file(file_path,window):
    try:
        os.remove(file_path)
        window.destroy()
        display_content(file_paths)        
        return tk.messagebox.showinfo("deleted successful",f"File deleted: {file_path}")

        
    except FileNotFoundError:
        return tk.messagebox.showinfo("error",f"File not found: {file_path}")
        pass
    except Exception as e:
        return tk.messagebox.showinfo("error",f"Error deleting file: {e}")
        pass



def display_content(file_paths):
    # Create main window
    window = tk.Tk()
    window.title("File Content Viewer")
    for file_path in file_paths:
        try:
            with open(file_path, 'r') as file:
                content = file.read()
                frame=tk.Frame(window)
                frame.pack(side=tk.TOP,padx=40)
                btn=tk.Button(frame,bd=5,command=lambda path=file_path: delete_file(path,window),text='delete')
                btn.pack(side=tk.LEFT)
                lbl=tk.Label(frame,text=file_path)
                lbl.pack()
                
                text = ScrolledText(window, wrap=tk.WORD, width=10, height=10)
                text.pack(fill=tk.BOTH, expand=True)

                # Insert content into the text box
                text.insert(tk.END, content)
        except FileNotFoundError:
            tk.messagebox.showinfo('Error' ,'file not found')
            #window.destroy()
    # Start the Tkinter event loop
    window.mainloop()


