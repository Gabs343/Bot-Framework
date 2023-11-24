import tkinter as tk
import time
import os

class MainApp(tk.Tk):
    def __init__(self, *args, **kwargs) -> None:
        tk.Tk.__init__(self, *args, **kwargs) 
        
        self.title("App")
        self.geometry("1036x565")
        self.resizable(False, False)
        self.configure(bg = "#112C5F")
        
def main():
    app = MainApp()
    app.mainloop()
     
if __name__ == "__main__":
    st = time.time()
    main()
    et = time.time()
    elapsed_time = et - st
    print("Exceution time:", elapsed_time, "seconds")
        