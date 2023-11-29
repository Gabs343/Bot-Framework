import tkinter as tk
import os
import subprocess
from tkinter import messagebox
from gui_factory import GUIFactory

class SettingCanvas(tk.Canvas): 
    def __init__(self, parent: tk.Tk, **kwargs) -> None:
        super().__init__(parent, **kwargs)
        
        self.parent = parent
        self.gui_factory: GUIFactory = parent.gui_factory
        
        self.subcanvas = self.gui_factory.get_subcanvas(parent=self)
        self.subcanvas.place(x=75, y=75)
        
        back_btn = self.gui_factory.get_button(parent=self, 
                                                icon='back', 
                                                event= lambda: self.parent.show_canvas("PrincipalCanvas"))
        
        back_btn.place(
            x=64.0, y=50.0,
            width=45.0, height=35.0
        )
        
        self.create_text(
            396.0, 40.0,
            anchor="nw",
            text="Settings",
            fill="#FFFFFF",
            font=("RobotoRoman ExtraBold", 32 * -1)
        )
        
    def show_settings(self, bot_folder: str, settings: list) -> None:
        for service in settings:
            print(service)
            for key, value in service.settings.items():
                print(key, value)
                
        script_path = os.path.abspath(f'{self.parent.bots_folder_path}\\{bot_folder}\\main.py')
        #self.create_scheduled_task(task_name=settings[0].settings["task_name"], script_path=script_path, start_time="17:01")
    
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
            
            