import tkinter as tk
import os
import subprocess
from tkinter import messagebox
from gui_factory import GUIFactory

class SettingCanvas(tk.Canvas): 
    def __init__(self, parent: tk.Tk, **kwargs) -> None:
        super().__init__(parent, **kwargs)
        
        self.__parent: tk.Tk = parent
        self.__gui_factory: GUIFactory = parent.gui_factory
        
        self.create_gui_elements()
              
    def create_gui_elements(self):
        self.subcanvas: tk.Canvas = self.__gui_factory.get_subcanvas(parent=self, dimensions=(897, 385))
        self.subcanvas.place(x=70, y=75)
        
        self.scrollbar = tk.Scrollbar(self, orient=tk.VERTICAL, command=self.subcanvas.yview)
        
        self.subcanvas.configure(yscrollcommand=self.scrollbar.set)
        
        self.scrollbar.place(x=70 + 897, y=75, height=385)
        
        self.subcanvas.bind_all("<MouseWheel>", self.on_mousewheel)
        self.subcanvas.bind("<Configure>", self.on_configure)
        
        back_btn: tk.Button = self.__gui_factory.get_button(parent=self, 
                                                icon='back', 
                                                event= lambda: self.go_back())
        
        back_btn.place(
            x=64.0, y=40.0,
            width=45.0, height=35.0
        )
        
        self.__gui_factory.set_text_in_canvas(parent=self,
                                              text="Settings",
                                              coordinates=(480.0, 40.0),
                                              size=32)
           
    def on_configure(self, event=None) -> None:
        self.subcanvas.configure(scrollregion=self.subcanvas.bbox("all"))

    def on_mousewheel(self, event) -> None:
        if event.delta:
            self.subcanvas.yview_scroll(-1 * (event.delta // 120), "units")
                
    def show_settings(self, bot_folder: str, settings: list) -> None:
        y_title: float = 10.0
        for service in settings:
            
            self.__gui_factory.set_text_in_canvas(parent=self.subcanvas,
                                              text=service,
                                              coordinates=(400.0, y_title),
                                              size=27)
            
            settings_count: int = 1

            y_key: float = y_title + 50.0
            y_entry: float = y_key + 10.0

            for key, value in service.settings.items():
                if(settings_count > 4):
                    settings_count = 1
                    y_key = y_entry + 70 
                    y_entry = y_key+10

                x_position = self.calculate_x_position(settings_quantity=len(service.settings), settings_count=settings_count)
                
                input = self.__gui_factory.get_custom_input(parent=self.subcanvas)
                input.set_label(text=key, coordinates=(x_position-80, y_key))                
                input.set_entry(coordinates=(x_position, y_entry+35))
                
                input.insert(0, str(value))
                
                settings_count += 1  
   
            y_title = y_entry + 80
                
        script_path = os.path.abspath(f'{self.__parent.bots_folder_path}\\{bot_folder}\\main.py')
        self.on_configure()
        #self.create_scheduled_task(task_name=settings[0].settings["task_name"], script_path=script_path, start_time="17:01")
    
    def calculate_x_position(self, settings_quantity: int, settings_count: int) -> float:
        subcanvas_division: float = self.get_canvas_division(slices=settings_quantity)
        return (settings_count * subcanvas_division) - (subcanvas_division / 2)
        
    def get_canvas_division(self, slices: int) -> float:
        return self.subcanvas.winfo_width()/(slices if slices <= 4 else 4)
        
    def go_back(self) -> None:
        self.remove_gui_elements()
        self.__parent.show_canvas("PrincipalCanvas")
        
    def remove_gui_elements(self) -> None:
        self.subcanvas.delete("all")
        
    def get_python_path(self) -> str:
        command = 'where python'
        return subprocess.run(command, 
                              shell=True, 
                              stdout=subprocess.PIPE, 
                              stderr=subprocess.PIPE).stdout.decode("utf-8").strip()
        
    def task_exists(self, task_name: str) -> bool:
        command = f'schtasks /query /tn {task_name}'
        result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return result.returncode == 0
    
    def create_scheduled_task(self, task_name: str, script_path: str, start_time: str) -> None:
        if (self.task_exists(task_name)):
            messagebox.showinfo(message=f'Task "{task_name}" already exists. Please choose a different name.')
        else:
            task_run = f'cmd /c cd {script_path[:-8]} && {self.get_python_path()} main.py'
            command = f'schtasks /create /sc daily /tn {task_name} /tr "{task_run}" /st {start_time}'
            subprocess.run(command, shell=True)
            messagebox.showwarning(message=f"Scheduled task '{task_name}' created successfully.")
            
    def edit_scheduled_task(self, task_name: str, script_path: str, start_time: str):
        if (self.task_exists(task_name)):
            task_run = f'cmd /c cd {script_path[:-8]} && {self.get_python_path()} main.py'
            command = f'schtasks /change /tn {task_name} /tr "{task_run}" /st {start_time}'
            subprocess.run(command, shell=True)
            messagebox.showinfo(message=f"Scheduled task '{task_name}' edited successfully.")
        else:
            messagebox.showwarning(message=f'Task {task_name} does not exist. Cannot edit.')
            
    def delete_scheduled_task(self, task_name: str):
        if (self.task_exists(task_name)):
            command = f"schtasks /delete /tn {task_name} /f"
            subprocess.run(command, shell=True)
            messagebox.showinfo(f"Scheduled task '{task_name}' deleted successfully.")
        else:
            messagebox.showwarning(message=f"Task '{task_name}' does not exist. Cannot delete.")
            
            