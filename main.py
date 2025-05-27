from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinterdnd2 import DND_FILES, TkinterDnD  
from tkinter import messagebox
from Compressing_window import running


BG_COLOR = "#1a1a2e"
PRIMARY_COLOR = "#4cc9f0"
SECONDARY_COLOR = "#f72585"
TEXT_COLOR = "#ffffff"
HOVER_COLOR = "#3a86ff"

file_input_path = None

def check():
    if file_input_path is None:
        messagebox.showerror("Error", "Please select a video file first")
    else:
        running(app, file_input_path.replace("/", "\\"))

def browse_file():
    global file_input_path
    file_input_path = filedialog.askopenfilename(
        filetypes=[("Video Files", "*.mp4 *.avi *.mov *.mkv")]
    )
    if file_input_path:
        update_file_preview()

def drop_file(event):
    global file_input_path
    file_input_path = event.data.strip("{}")
    if file_input_path:
        update_file_preview()

def update_file_preview():
    file_name = file_input_path.split("/")[-1]
    preview_label.config(text=f"Selected: {file_name}")
    continue_btn.config(state=NORMAL, bg=HOVER_COLOR)

app = TkinterDnD.Tk() 
app.title("VideoCompressor Pro")
app.geometry("700x500")
app.config(bg=BG_COLOR)

title_label = Label(app, text="Video Compressor Pro", 
                fg=PRIMARY_COLOR, bg=BG_COLOR, 
                font=("Montserrat", 20, "bold"))
title_label.pack(pady=(20,10))


upload_label = Label(app, text="Upload your video file to start compression", 
                    fg=TEXT_COLOR, bg=BG_COLOR, 
                    font=("Roboto", 12))
upload_label.pack(pady=5)


preview_frame = Frame(app, bg=BG_COLOR)
preview_frame.pack(pady=20)

preview_label = Label(preview_frame, text="No file selected", 
                    fg=TEXT_COLOR, bg=BG_COLOR, 
                    font=("Roboto", 10))
preview_label.pack()


upload_frame = Frame(app, bg=BG_COLOR)
upload_frame.pack(pady=20)


browse_btn = Button(upload_frame, text="📁 Browse Files", 
                command=browse_file,
                bg=PRIMARY_COLOR, fg="white",
                font=("Roboto", 12), 
                padx=20, pady=10,
                relief=FLAT, bd=0,
                activebackground=HOVER_COLOR)
browse_btn.grid(row=0, column=0, padx=10)


or_label = Label(upload_frame, text="OR", 
                fg=TEXT_COLOR, bg=BG_COLOR,
                font=("Roboto", 12))
or_label.grid(row=0, column=1, padx=10)


drag_frame = Label(upload_frame, text="📤 Drag & Drop Here", 
                bg=SECONDARY_COLOR, fg="white",
                font=("Roboto", 12), 
                padx=40, pady=30,
                relief="groove")
drag_frame.grid(row=0, column=2, padx=10)

drag_frame.drop_target_register(DND_FILES)
drag_frame.dnd_bind("<<Drop>>", drop_file)


continue_btn = Button(app, text="🚀 Start Compression", 
                    command=check,
                    bg=SECONDARY_COLOR, fg="white",
                    font=("Roboto", 14, "bold"), 
                    padx=30, pady=10,
                    state=DISABLED,
                    relief=FLAT, bd=0,
                    activebackground=HOVER_COLOR)
continue_btn.pack(pady=30)


footer = Label(app, text="VideoCompressor Pro © 2023 | v1.0", 
            fg=TEXT_COLOR, bg=BG_COLOR,
            font=("Roboto", 8))
footer.pack(side=BOTTOM, pady=10)

def on_enter(e):
    e.widget['background'] = HOVER_COLOR

def on_leave(e):
    if e.widget != continue_btn:
        e.widget['background'] = PRIMARY_COLOR if e.widget == browse_btn else SECONDARY_COLOR

browse_btn.bind("<Enter>", on_enter)
browse_btn.bind("<Leave>", on_leave)
drag_frame.bind("<Enter>", on_enter)
drag_frame.bind("<Leave>", on_leave)
continue_btn.bind("<Enter>", on_enter)
continue_btn.bind("<Leave>", on_leave)

app.resizable(0, 0)
app.mainloop()