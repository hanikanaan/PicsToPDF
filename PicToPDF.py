from PIL import Image
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox

root = tk.Tk()


class ResizingCanvas(tk.Canvas):
    def __init__(self, parent, **kwargs):
        tk.Canvas.__init__(self, parent, **kwargs)
        self.bind("<Configure>", self.on_resize)
        self.height = self.winfo_reqheight()
        self.width = self.winfo_reqwidth()

    def on_resize(self, event):
        # determine the ratio of old width/height to new width/height
        wscale = float(event.width)/self.width
        hscale = float(event.height)/self.height
        self.width = event.width
        self.height = event.height
        self.scale("all", 0, 0, wscale, hscale)


myframe = tk.Frame(root)
myframe.pack(fill=tk.BOTH, expand=tk.YES)
canvas = ResizingCanvas(myframe, width=800, height=600, bg='grey')
canvas.pack(fill=tk.BOTH, expand=tk.YES)

header = tk.Label(root, text='File Conversion Tool', bg='grey', fg='white')
header.config(font=('calibri', 30))
canvas.create_window(400, 120, window=header)

imagelist = []


def getFile():
    global im1

    import_file_path = filedialog.askopenfilename()
    image1 = Image.open(import_file_path)
    im1 = image1.convert('RGB')
    msgBox = tk.messagebox.askquestion('Exit Application?', 'Would you like to scan more pictures?', icon='question')

    while msgBox == 'yes':
        import_file_path = filedialog.askopenfilename()
        image = Image.open(import_file_path)
        im = image.convert('RGB')
        imagelist.append(im)
        msgBox = tk.messagebox.askquestion('Exit Application?', 'Would you like to scan more pictures?',
                                           icon='question')
        if msgBox == 'no':
            break


browseButton = tk.Button(text="     Select File     ", command=getFile, bg='green', fg='white',
                         font=('calibri', 11, 'bold'))
canvas.create_window(400, 260, window=browseButton)


def convertToPdf():
    export_file_path = filedialog.asksaveasfilename(defaultextension='.pdf')
    im1.save(export_file_path, save_all=True, append_images=imagelist)
    confirm = tk.messagebox.showinfo('Confirmation', f'Your PDF has been saved to {export_file_path}. Thank you for'
                                                     ' using the pics to PDF tool!', icon='info')


saveAsButton = tk.Button(text='Convert to PDF', command=convertToPdf, bg='blue', fg='white',
                         font=('calibri', 11, 'bold'))

canvas.create_window(400, 360, window=saveAsButton)


def exitApplication():
    msgBox = tk.messagebox.askquestion('Exit Application', 'Are you sure you want to exit the application',
                                       icon='warning')
    if msgBox == 'yes':
        root.destroy()


exitButton = tk.Button(root, text='Exit Application', command=exitApplication, bg='brown', fg='white',
                       font=('calibri', 11, 'bold'))
canvas.create_window(400, 460, window=exitButton)

root.mainloop()
