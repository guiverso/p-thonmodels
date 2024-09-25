from tkinter.constants import NORMAL
from typing import Any, Callable, Tuple
import customtkinter as ctk

class App(ctk.CTk):
    def __init__(self,title:str,geometry:str,resizable:bool=False):
        super().__init__()
        self.title(title)
        self.resizable(resizable,resizable)
        self.geometry(geometry)
        self.windowslist = [] #uma lista de janelas 

    def add_window(self,window:ctk.CTkFrame):#adiciona uma janela
        self.windowslist.append(window)
        window.grid(row=0,column=0,sticky='nsew')
        self.change_window(0)
    
    def change_window(self,index):
        if(type(index)==int): return self.windowslist[index].tkraise()
        for window in self.windowslist:
            if(window.name==index):
                return window.tkraise()
            
class Window(ctk.CTkFrame):
    def __init__(self, master:App,name:str):
        super().__init__(master)
        self.name=name
    
    def add_element(self,element,row=0,column=0,padx=0,pady=0,expandTo='w'):
        element.grid(row=row,column=column,padx=padx,pady=pady,sticky=expandTo)

class Button(ctk.CTkButton):
    def __init__(self, master: Any, width: int = 140, height: int = 28, corner_radius: int | None = None, border_width: int | None = None, border_spacing: int = 2, bg_color: str | Tuple[str] = "transparent", fg_color: str | Tuple[str] | None = None, hover_color: str | Tuple[str] | None = None, border_color: str | Tuple[str] | None = None, text_color: str | Tuple[str] | None = None, text_color_disabled: str | Tuple[str] | None = None, background_corner_colors: Tuple[str | Tuple[str]] | None = None, round_width_to_even_numbers: bool = True, round_height_to_even_numbers: bool = True, text: str = "CTkButton", font: Tuple | ctk.CTkFont | None = None, textvariable: ctk.Variable | None = None, image: ctk.CTkImage | Any | None = None, state: str = "normal", hover: bool = True, command: Callable[[], Any] | None = None, compound: str = "left", anchor: str = "center", **kwargs):
        super().__init__(master, width, height, corner_radius, border_width, border_spacing, bg_color, fg_color, hover_color, border_color, text_color, text_color_disabled, background_corner_colors, round_width_to_even_numbers, round_height_to_even_numbers, text, font, textvariable, image, state, hover, command, compound, anchor, **kwargs)

class Entry(ctk.CTkEntry):
    def __init__(self, master: Any, width: int = 140, height: int = 28, corner_radius: int | None = None, border_width: int | None = None, bg_color: str | Tuple[str] = "transparent", fg_color: str | Tuple[str] | None = None, border_color: str | Tuple[str] | None = None, text_color: str | Tuple[str] | None = None, placeholder_text_color: str | Tuple[str] | None = None, textvariable: ctk.Variable | None = None, placeholder_text: str | None = None, font: Tuple | ctk.CTkFont | None = None, state: str = NORMAL, **kwargs):
        super().__init__(master, width, height, corner_radius, border_width, bg_color, fg_color, border_color, text_color, placeholder_text_color, textvariable, placeholder_text, font, state, **kwargs)

class Text(ctk.CTkLabel):
    def __init__(self,window,placeHolder=None,password=False,width=140,height=28,corner=7,color='#343638',textColor='white',borderColor='#565b5e',border=2,justify='center',limitChar=13):
        self.limitChar = limitChar
        show = '●' if password == True else ''
        super().__init__(window,width,height,corner,border,'transparent',color,borderColor,textColor,'#808587',None,placeHolder,justify=justify,show=show)
        self.configure(validate='key',validatecommand=(window.register(self.validate),'%P'))

    def changeViewPassword(self):
        if self.cget('show') == '●':
            self.configure(show='')
        else:
            self.configure(show='●')

    def validate(self,currentEntry):
        return len(currentEntry) < self.limitChar

class shoupassbutt(Button):
    def __init__(self,window,passwordInput:Text):
        super().__init__(window,'',self.changeView,0,0,0,'transparent',hover=False)
        self.passwordInput = passwordInput
        
    def changeView(self):
        self.passwordInput.changeViewPassword()