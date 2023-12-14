import tkinter as tk
from gui_factory import GUIFactory

class BotContainerComponent:
    def __init__(self, parent: tk.Canvas, coordinates: tuple, bot) -> None:
        self.parent = parent
        self.width = 763.0
        self.height = 70.0
        self.x_coordinate , self.y_coordinate = coordinates
        
        self.shadow_offset = 3.0
        
        self.bot = bot
        self.bot.set_status_changed_callback(callback=self.set_status)
        self.buttons_dict = {}
        
        self.create_buttons()
        self.place_rectangles()
        self.place_information()
        self.place_buttons()
    
    def place_rectangles(self) -> None:
        shadow_id = self.parent.create_rectangle(
            self.x_coordinate+self.shadow_offset,
            self.y_coordinate+self.shadow_offset,
            self.width+self.shadow_offset+self.x_coordinate, 
            self.height+self.shadow_offset+self.y_coordinate,
            fill="#010C1A",
            outline="")

        container_id = self.parent.create_rectangle(
            self.x_coordinate, self.y_coordinate,
            self.width+self.x_coordinate, self.height+self.y_coordinate,
            fill="#577190",
            outline="")
        
    def place_information(self) -> None:
        bot_name_id = self.parent.create_text(
            self.x_coordinate + 20,
            self.y_coordinate+23,
            anchor="nw",
            text=self.bot.bot_name,
            fill="#FFFFFF",
            font=("RobotoRoman ExtraBold", 20 * -1)
        )

        text_id = self.parent.create_text(
            self.x_coordinate + 250,
            self.y_coordinate+27,
            anchor="nw",
            text="STATUS:",
            fill="#FFFFFF",
            font=("RobotoRoman Bold", 14 * -1)
        )

        self.bot_status_id = self.parent.create_text(
            self.x_coordinate + 320,
            self.y_coordinate+27,
            anchor="nw",
            text=self.bot.status,
            fill="#FFFFFF",
            font=("RobotoRoman Regular", 16 * -1)
        )
        
    def set_status(self, new_status: str):
        self.parent.itemconfig(self.bot_status_id, text=new_status)
        if(new_status == 'RUNNING'):
            self.change_enable_buttons(buttons=['play', 'settings', 'delete'], isEnabled=False)
            self.remove_buttons()
            self.change_enable_buttons(buttons=['pause', 'stop'], isEnabled=True)
            self.place_buttons()

        '''
        elif(new_status == 'READY'):
            self.change_enable_buttons(buttons=['pause', 'stop'], isEnabled=False)
            self.remove_buttons()
            self.change_enable_buttons(buttons=['play', 'settings', 'delete'], isEnabled=True)
  
        '''
            
        
    def create_buttons(self) -> None:
        for button in ['play', 'pause', 'stop', 'settings', 'delete']:
            self.buttons_dict[button] = {}
            self.buttons_dict[button]['object'] = GUIFactory.get_button(parent=self.parent, icon=button)
            self.buttons_dict[button]['window_id'] = None
            
        self.change_enable_buttons(buttons=['play', 'settings', 'delete'], isEnabled=True)
        
    def change_enable_buttons(self, buttons: list[str], isEnabled: bool):
        for button in buttons:
            self.buttons_dict[button]['object'].isEnabled = isEnabled
        
    def place_buttons(self) -> None:                
        icon_x_coordinate = 580.0
        margin = 62.0
        
        for button in self.buttons_dict:
            if(self.buttons_dict[button]['object'].isEnabled):
                self.buttons_dict[button]['window_id'] = self.parent.create_window(icon_x_coordinate + self.x_coordinate, 
                                        self.y_coordinate+30,
                                        width=45.0,
                                        height=45.0,
                                        window=self.buttons_dict[button]['object'])
          
                icon_x_coordinate += margin
                
    def remove_buttons(self) -> None:
        for button in self.buttons_dict:
            if(not self.buttons_dict[button]['object'].isEnabled):
                self.parent.delete(self.buttons_dict[button]['window_id']) 
                self.buttons_dict[button]['window_id'] = None 

        
    def change_button_event(self, button: str, event) -> None:
        self.buttons_dict[button]['object'].config(command=event)