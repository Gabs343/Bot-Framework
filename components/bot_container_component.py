import tkinter as tk

class BotContainerComponent:
    def __init__(self, parent: tk.Canvas, coordinates: tuple, buttons: list[tk.Button], bot) -> None:
        self.parent = parent
        self.width = 763.0
        self.height = 70.0
        self.x_coordinate , self.y_coordinate = coordinates
        
        self.shadow_offset = 3.0
        
        self.bot = bot
        self.buttons = buttons
        self.gui_elements = []
        
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
        
        self.gui_elements.append(shadow_id)
        self.gui_elements.append(container_id)
        
    def place_information(self) -> None:
        bot_name_id = self.parent.create_text(
            100.0,
            self.y_coordinate+23,
            anchor="nw",
            text=self.bot.bot_name,
            fill="#FFFFFF",
            font=("RobotoRoman ExtraBold", 20 * -1)
        )

        text_id = self.parent.create_text(
            278.0,
            self.y_coordinate+27,
            anchor="nw",
            text="STATUS:",
            fill="#FFFFFF",
            font=("RobotoRoman Bold", 14 * -1)
        )

        bot_status_id = self.parent.create_text(
            350.0,
            self.y_coordinate+27,
            anchor="nw",
            text=self.bot.status,
            fill="#FFFFFF",
            font=("RobotoRoman Regular", 16 * -1)
        )
        
        self.gui_elements.append(bot_name_id)
        self.gui_elements.append(text_id)
        self.gui_elements.append(bot_status_id)
        
    def place_buttons(self) -> None:                
        icon_x_coordinate = 661.0
        margin = 62.0
        for button in self.buttons:
            window = self.parent.create_window(icon_x_coordinate, 
                                    self.y_coordinate+30,
                                    width=45.0,
                                    height=45.0,
                                    window=button)
            
            self.gui_elements.append(button)
            self.gui_elements.append(window)
          
            icon_x_coordinate += margin
            
    def remove_gui_elements(self) -> None:
        for element in self.gui_elements:
            if(type(element) is int):
                self.parent.delete(element)
            else:
                element.destroy() 
            
    def set_button_event(self, button: int, event) -> None:
        self.buttons[button].config(command=event)