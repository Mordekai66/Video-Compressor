from tkinter import *
from tkinter.scrolledtext import ScrolledText
from tkinter import messagebox
import subprocess

def run(command, total_frames, duration):
    total_frames = int(total_frames)
    duration = float(duration)
    def run_ffmpeg(command):
        run_button.config(state=DISABLED, bg="#222831", fg="#EEEEEE")
        process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT, 
            universal_newlines=True,    
            shell=True,                
            bufsize=1                 
        )
        
        while True:
            line = process.stdout.readline()
            if not line and process.poll() is not None:
                break
            if line:
                frame_number = line.split("frame=")[-1].split()[0]
                if frame_number.isdigit():
                    frame_number = int(frame_number)
                else:
                    frame_number = 0
                    
                progress_label.config(
                    text=f"Frame number {frame_number} of {int(total_frames * duration)} | "
                        f"{int((int(frame_number) / int(total_frames * duration)) * 100)}%"
                )
                text_box.insert(END, line)
                text_box.see(END)          
                text_box.update()
        
        progress_label.config(text=f"Compression completed! Total frames: {int(total_frames * duration)}")
        messagebox.showinfo("Info", "Compression completed successfully!")
        text_box.insert(END, "=====================================\n")
        text_box.insert(END, "Compression completed successfully!\n")
        text_box.insert(END, "=====================================\n")
        run_button.config(state=NORMAL, bg="#FFD369", fg="#222831")

    root = Tk()
    root.title("Compressing Video Stream")

    text_box = ScrolledText(
        root,
        width=80,
        height=20,
        font=("Consolas", 11),
        bg="#393E46",         
        fg="#EEEEEE",         
        insertbackground="#FFD369",
        borderwidth=0,
        highlightthickness=2,
        highlightbackground="#FFD369"
    )
    text_box.pack(padx=20, pady=20)
    
    progress_label = Label(
        root,
        text=f"Frame number 0 of {int(total_frames) * int(duration)} | 0%",
        font=("Segoe UI", 12, "bold"),
        bg="#222831",
        fg="#FFD369"
    )
    progress_label.pack(pady=(0, 10))

    run_button = Button(
        root,
        text="Start Compressing",
        font=("Segoe UI", 12, "bold"),
        bg="#FFD369",
        fg="#222831",
        activebackground="#FFA502",
        activeforeground="#222831",
        relief="flat",
        padx=20,
        pady=8,
        command=lambda: run_ffmpeg(command)
    )
    run_button.pack(pady=(0, 20))

    root.mainloop()