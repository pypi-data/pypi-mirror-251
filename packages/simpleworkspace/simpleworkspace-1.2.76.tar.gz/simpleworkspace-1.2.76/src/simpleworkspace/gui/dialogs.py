from tkinter import filedialog as _filedialog
import tkinter as _tk

class _TK_BaseDialog():
    _styles_colors_background = "#E9ECED"
    _styles_colors_foreground = "black"
    _styles_colors_button_foreground = _styles_colors_foreground
    _styles_colors_button_background = "#CFD4D9"
    _styles_fonts_helvetica_9 = "Helvetica 9"
    _styles_fonts_helvetica_10 = "Helvetica 10"
    _styles_fonts_text = _styles_fonts_helvetica_10
    _styles_fonts_button = _styles_fonts_helvetica_9

    def __init__(self, topmost=False, title: str = None):
        self._state_ClosedByTK = False
        self.root = _tk.Tk()
        if topmost:
            self.root.wm_attributes("-topmost", 1)
        if title:
            self.root.title(title)
        self.root.bind("<Destroy>", self._OnDestroyed_Window)  # it might get destroyed by tk itself when closing from taskbar etc
        self.root.configure(background=self._styles_colors_background)

    def Show(self):
        self._CenterWindow()
        self.root.mainloop()

    def _CenterWindow(self):
        self.root.withdraw() # Remain invisible while we figure out the geometry
        self.root.update_idletasks() # Actualize geometry information

        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"+{x}+{y}")

        self.root.deiconify() # Become visible at the desired location

    def _OnDestroyed_Window(self, *args):
        self._state_ClosedByTK = True

    def __enter__(self):
        return self
    
    def __exit__(self, *args):
        if not self._state_ClosedByTK:
            self.root.destroy()

class _MessageBox(_TK_BaseDialog):
    def __init__(self, message: str, title="MessageBox", topmost=False):
        super().__init__(topmost=topmost, title=title)

        frame = _tk.Frame(self.root)
        textbox = _tk.Text(
            frame,
            borderwidth=0,
            height=4,
            width=60,
            wrap=_tk.WORD,
            bg=self._styles_colors_background,
            fg=self._styles_colors_foreground,
            font=self._styles_fonts_text,
        )
        textbox.tag_configure("center", justify="center")
        textbox.insert(1.0, message, "center")

        def OnMap_Textbox(event: _tk.Event):
            widget: _tk.Text = event.widget
            displayLines = widget.count("1.0", "end", "displaylines")[0]
            if displayLines > 5:
                displayLines = 5
                scrollbar = _tk.Scrollbar(widget.master)
                scrollbar.pack(side=_tk.RIGHT, fill=_tk.Y)
                widget.configure(yscrollcommand=scrollbar.set)

            widget.configure(height=displayLines)
            return

        textbox.bind("<Map>", OnMap_Textbox)
        textbox.configure(state="disabled")
        textbox.pack(side=_tk.LEFT, fill=_tk.BOTH, expand=True)
        frame.pack(padx=10, pady=5, fill=_tk.BOTH, expand=True)

        frame_belowMessage = _tk.Frame(self.root)
        self._MapControls(frame_belowMessage)
        frame_belowMessage.pack(side=_tk.BOTTOM, fill=_tk.BOTH, expand=True)

    def _MapControls(self, frame: _tk.Frame):
        ok_button = _tk.Button(
            frame,
            text="OK",
            font=self._styles_fonts_button,
            bg=self._styles_colors_button_background,
            fg=self._styles_colors_button_foreground,
            padx=35,
            command=self.root.destroy,
        )
        ok_button.pack(pady=(5, 10))

class _MessageBox_YesOrNo(_MessageBox):
    def __init__(self, message: str, title="MessageBox", topmost=False):
        self.state_answer = False
        super().__init__(message=message, title=title, topmost=topmost)
        """defaults to false, is only true if yes button is pressed"""

    def _MapControls(self, frame: _tk.Frame):
        def OnClick_AnswerBtn(answer: bool):
            self.state_answer = answer
            self.root.destroy()

        yes_button = _tk.Button(
            frame,
            text="Yes",
            font=self._styles_fonts_button,
            bg=self._styles_colors_button_background,
            fg=self._styles_colors_button_foreground,
            padx=35,
            command=lambda: OnClick_AnswerBtn(True),
        )
        no_button = _tk.Button(
            frame,
            text="No",
            font=self._styles_fonts_button,
            bg=self._styles_colors_button_background,
            fg=self._styles_colors_button_foreground,
            padx=35,
            command=lambda: OnClick_AnswerBtn(False),
        )

        no_button.pack(side=_tk.LEFT, anchor=_tk.E, expand=True, pady=(5, 10), padx=5)
        yes_button.pack(side=_tk.RIGHT, anchor=_tk.W, expand=True, pady=(5, 10), padx=5)

class _MessageBox_TextInput(_MessageBox):
    def __init__(self, message: str, initialValue: str = None, title="MessageBox", topmost=False):
        self.state_answer: None | str = None
        self._state_initialValue = initialValue
        super().__init__(message=message, title=title, topmost=topmost)

    def _MapControls(self, frame: _tk.Frame):
        textBox = _tk.Entry(
            frame,
            font=self._styles_fonts_text,
        )
        if self._state_initialValue:
            textBox.insert(0, self._state_initialValue)

        def OnClick_BtnOk(*args):
            self.state_answer = textBox.get()
            self.root.destroy()

        btn_ok = _tk.Button(
            frame,
            text="Ok",
            font=self._styles_fonts_button,
            bg=self._styles_colors_button_background,
            fg=self._styles_colors_button_foreground,
            padx=35,
            command=OnClick_BtnOk,
        )

        textBox.pack(side=_tk.LEFT, fill=_tk.BOTH, expand=True, pady=(5, 10), padx=5)
        btn_ok.pack(side=_tk.RIGHT, fill=_tk.Y, pady=(5, 10), padx=5)
        textBox.focus()
        textBox.bind("<Return>", OnClick_BtnOk)

def ShowInputBox(message: str, title: str = None, topmost=False, initialValue:str = None):
    '''
    Asks user for a string input
    :param initalValue: A preentered default input text visible to user when prompt is displayed
    :returns: the input string, if window is closed then None
    '''
    with _MessageBox_TextInput(message, title=title, topmost=topmost, initialValue=initialValue) as msgBox:
        msgBox.Show()
        return msgBox.state_answer

def ShowQuestionBox(message: str, title: str = None, topmost=False):
    '''Displays a messagebox containing a question with a yes or no button'''
    with _MessageBox_YesOrNo(message, title=title, topmost=topmost) as msgBox:
        msgBox.Show()
        return msgBox.state_answer

def ShowMessageBox(message: str, title: str = None, topmost=False):
    with _MessageBox(message, title=title, topmost=topmost) as msgBox:
        msgBox.Show()

#only reason to use parent as custom tkdialog is to add icon to taskbar and being able to set topmost attribute
def ShowFileDialog(multiple=False, initialDir:str=None, title:str=None, topmost=False):
    with _TK_BaseDialog(topmost=topmost) as tkdialog:
        tkdialog.root.attributes('-alpha', 0.0)  #makes the root windows invisible if it were to be reopened
        tkdialog.root.iconify()                  #minimizes the root windows
        if(multiple):
            res = tuple(_filedialog.askopenfilenames(initialdir=initialDir, title=title, parent=tkdialog.root))
        else:
            res = _filedialog.askopenfilename(initialdir=initialDir, title=title, parent=tkdialog.root)
        return res if res != '' else None


def ShowDirectoryDialog(initialDir:str=None, title:str=None, topmost=False):
    with _TK_BaseDialog(topmost=topmost) as tkdialog:
        tkdialog.root.attributes('-alpha', 0.0)  #makes the root windows invisible if it were to be reopened
        tkdialog.root.iconify()                  #minimizes the root windows
        res = _filedialog.askdirectory(initialdir=initialDir, title=title, parent=tkdialog.root)
        return res if res != '' else None
