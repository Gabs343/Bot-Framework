import tkinter as tk
from gui_factory import GUIFactory

class BotContainerComponent(tk.Canvas):
    def __init__(self, parent: tk.Canvas, bot, **kwargs) -> None:
        super().__init__(parent,
                        width = kwargs['width'],
                        height = kwargs['height'],
                        bg = 'black',
                        bd = 0,
                        highlightthickness = 0,
                        relief = 'ridge')
        self.place(x=kwargs['x'], y=kwargs['y'])
        self.background: str = '#577190'
        
        self.x_coordinate: float = kwargs['x']
        self.y_coordinate: float = kwargs['y']
        
        self.width: float = kwargs['width']
        self.height: float = kwargs['height']
        
        self.subcanvas_base_width: float = self.width/3
        self.subcanvas_base_height: float = self.height-12
        
        self.base_x_coordinate: float = 10.0
        
        self.bot = bot
        self.bot.set_status_changed_callback(callback=self.set_status)
        self.buttons_dict: dict = {}
        
        self.place_rectangle()
        self.create_and_place_subcanvas()
        self.create_buttons()
        self.place_information()
        self.place_buttons()
    
    def place_rectangle(self) -> None:
        shadow_offset: float = 4.0
        self.create_rectangle(
            shadow_offset,
            shadow_offset,
            self.width+shadow_offset+self.x_coordinate, 
            self.height+shadow_offset+self.y_coordinate,
            fill=self.background,
            outline="")
        
    def create_and_place_subcanvas(self) -> None:
        margin_subcanvas: float = 10.0
        self.title_canvas: tk.Canvas = GUIFactory.get_subcanvas(parent=self, 
                                                                width=self.subcanvas_base_width, 
                                                                height=self.subcanvas_base_height, 
                                                                bg=self.background)
    
        self.status_canvas: tk.Canvas = GUIFactory.get_subcanvas(parent=self, 
                                                                 width=self.subcanvas_base_width, 
                                                                 height=self.subcanvas_base_height, 
                                                                 bg=self.background)
        
        self.buttons_canvas: tk.Canvas = GUIFactory.get_subcanvas(parent=self, 
                                                                  width=self.subcanvas_base_width/1.2, 
                                                                  height=self.subcanvas_base_height, 
                                                                  bg=self.background)
        
        self.title_canvas.place(x=self.base_x_coordinate, y=7)
        self.status_canvas.place(x=self.base_x_coordinate + self.subcanvas_base_width + margin_subcanvas, y=7)
        self.buttons_canvas.place(x=(self.base_x_coordinate + self.subcanvas_base_width)*2 + margin_subcanvas, y=7)
        
    def place_information(self) -> None:

        bot_name_id: int = GUIFactory.set_text_in_canvas(parent=self.title_canvas,
                                                    text=self.bot.bot_name,
                                                    coordinates=(self.base_x_coordinate,20),
                                                    size=20)
        
        text_id: int = GUIFactory.set_text_in_canvas(parent=self.status_canvas,
                                                text='STATUS:',
                                                coordinates=(self.base_x_coordinate*2,20),
                                                size=14)
        
        self.bot_status_id: int = GUIFactory.set_text_in_canvas(parent=self.status_canvas,
                                                text=self.bot.status,
                                                coordinates=((self.base_x_coordinate*2)+65,20),
                                                size=16)
            
    def set_status(self, new_status: str) -> None:
        self.status_canvas.itemconfig(self.bot_status_id, text=new_status)
        if(new_status == 'RUNNING'):
            self.change_enable_buttons(buttons=['play', 'settings', 'delete'], isEnabled=False)
            self.remove_buttons()
            self.change_enable_buttons(buttons=['pause', 'stop'], isEnabled=True)
            self.place_buttons()
            
        elif(new_status == 'READY'):
            self.change_enable_buttons(buttons=['pause', 'stop'], isEnabled=False)
            self.remove_buttons()
            self.change_enable_buttons(buttons=['play', 'settings', 'delete'], isEnabled=True)
            self.place_buttons()
             
    def create_buttons(self) -> None:
        for button in ['play', 'pause', 'stop', 'settings', 'delete']:
            self.buttons_dict[button] = {}
            self.buttons_dict[button]['object'] = GUIFactory.get_button(parent=self.buttons_canvas, icon=button)
            self.buttons_dict[button]['window_id'] = None
            
        self.change_enable_buttons(buttons=['play', 'settings', 'delete'], isEnabled=True)
        
    def change_enable_buttons(self, buttons: list[str], isEnabled: bool) -> None:
        for button in buttons:
            self.buttons_dict[button]['object'].isEnabled = isEnabled
        
    def place_buttons(self) -> None:                
        icon_x_coordinate: float = 40.0
        margin: float = 62.0
        
        for button in self.buttons_dict:
            if(self.buttons_dict[button]['object'].isEnabled):
                self.buttons_dict[button]['window_id'] = self.buttons_canvas.create_window(icon_x_coordinate, 
                                        26,
                                        width=45.0,
                                        height=45.0,
                                        window=self.buttons_dict[button]['object'])
          
                icon_x_coordinate += margin
                
    def remove_buttons(self) -> None:
        self.buttons_canvas.delete('all')

    def change_button_event(self, button: str, event) -> None:
        self.buttons_dict[button]['object'].config(command=event)
        
    def __str__(self) -> str:
        return f'Container for bot {self.bot.bot_name}'