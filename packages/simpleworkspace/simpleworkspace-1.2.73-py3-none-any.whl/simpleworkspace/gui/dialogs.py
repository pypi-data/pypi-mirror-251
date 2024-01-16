from tkinter import \
    messagebox as _messagebox, \
    simpledialog as _simpledialog, \
    filedialog as _filedialog, \
    Tk as _Tk


class _TempRootDialog(_Tk):
    def __init__(self, topmost = False):
        super().__init__()
        self.attributes('-alpha', 0.0)  #makes the root windows invisible if it were to be reopened
        self.iconify()                  #minimizes the root windows
        if(topmost):
            self.wm_attributes("-topmost", 1)
        self.bind('<Destroy>', self._destroy_callback) #it might get destroyed by tk itself when closing from taskbar etc
        self._closed_by_tk = False
    
    def _destroy_callback(self, *args):
        self._closed_by_tk = True

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if(not self._closed_by_tk):
            self.destroy()

def Prompt_YesOrNo(message:str, title:str = None, topmost=False):
    with _TempRootDialog(topmost=topmost) as root:
        return _messagebox.askyesno(title=title, message=message, parent=root)

def Prompt_Input(message:str, title:str = None, initalValue=None, topmost=False):
    '''
    Asks user for a string input
    :param initalValue: A preentered default input text visible to user when prompt is displayed
    :returns: the input string, if window is closed or cancelled then None
    '''
    with _TempRootDialog(topmost=topmost) as root:
        return _simpledialog.askstring(title=title, prompt=message, initialvalue=initalValue, parent=root)

def ShowFileDialog(multiple=False, initialDir:str=None, title:str=None, topmost=False):
    with _TempRootDialog(topmost=topmost) as root:
        if(multiple):
            res = tuple(_filedialog.askopenfilenames(initialdir=initialDir, title=title, parent=root))
        else:
            res = _filedialog.askopenfilename(initialdir=initialDir, title=title, parent=root)
        return res if res != '' else None


def ShowDirectoryDialog(initialDir:str=None, title:str=None, topmost=False):
    with _TempRootDialog(topmost=topmost) as root:
        res = _filedialog.askdirectory(initialdir=initialDir, title=title, parent=root)
        return res if res != '' else None

def ShowMessageBox(message:str, title:str=None, topmost = False):
    with _TempRootDialog(topmost=topmost) as root:
        _messagebox.showinfo(title, message, parent=root)
    
