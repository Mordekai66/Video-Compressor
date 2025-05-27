from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
from get_video_info import get_video_metadata
import cv2
import random
from PIL import Image, ImageTk
import os
import datetime
from run import run

image_ref = []

def running(app, input_file_path):
    for widget in app.winfo_children():
        widget.destroy()
        
    input_file_path = input_file_path
    input_file_name = input_file_path.split("\\")[-1]
    input_file_extension = input_file_name.split(".")[-1]
    
    output_file_path = os.path.join(os.path.expanduser("~"), "Videos")
    
    def get_frames():
        vidcap = cv2.VideoCapture(input_file_path)
        totalFrames = vidcap.get(cv2.CAP_PROP_FRAME_COUNT)
        randomFrameNumber=random.randint(0, int(totalFrames)-1)
        
        vidcap.set(cv2.CAP_PROP_POS_FRAMES,randomFrameNumber)
        success, image = vidcap.read()
        if success:
            image = cv2.resize(image, (200, 280))
            image = Image.fromarray(image)
            image = ImageTk.PhotoImage(image)
            image_ref.append(image)


    def run_command():
        if output_file_path is None:
            messagebox.showerror("Error", "Please enter output file path")
            return 
        else:
            tansform_video_encoder = {"H.264": "libx264", "H.265": "libx265", "VP9": "libvpx-vp9"}
            video_encoder = tansform_video_encoder[video_encoder_combobox.get()]
            video_fps = video_fbs_combobox.get()
            
            video_preset = video_preset_combobox.get()
            video_encoder_level = video_encoder_level_combobox.get()
            video_quality = video_quality_scale_scale.get() 
            audio_encoder = audio_encode_combobox.get().lower()
            audio_bitrate = audio_bitrate_combobox.get()
            audio_channels = audio_channels_combobox.get()
            audio_volume = audio_volume_combobox.get()
            final_path = file_path_entry.get()

            output_file = os.path.join(final_path, f"compressed-{input_file_name.split(".")[0]}-at-{datetime.datetime.now().strftime("%H-%M-%S")}.mp4")

            command = f'ffmpeg -i {input_file_path} -c:v libx264 -preset {video_preset} -crf {video_quality} -level {video_encoder_level} -r {video_fps} -c:a {audio_encoder} -b:a {audio_bitrate} -ac 2 -af volume={audio_volume} -movflags +faststart {output_file}'
            run(command, video_fps, data['format']['duration'])

    def show_menu(event):
        menu.post(event.x_root, event.y_root)
        file_btn.config(state="disabled")

    def hide_menu(event):
        menu.unpost()
        file_btn.config(state="normal", fg="white")

    def select_path():
        global output_file_path
        output_file_path = filedialog.askdirectory()
        file_path_entry.delete(0, END)
        file_path_entry.insert(0, output_file_path)

    def show_frame(frame):
        video_info_frame.place_forget()
        audio_info_frame.place_forget()
        preview_info_frame.place_forget()
        frame.place(relx=0.5, rely=0.48, anchor="center", width=560, height=310)


    if input_file_extension.lower() not in ["mp4", "avi", "mov", "mkv", "flv", "wmv"]:
        raise ValueError("Unsupported file format. Please select a video file.")


    data = get_video_metadata(input_file_path)

    if data['streams'][0]['codec_type'] == 'audio':
        # Video data
        video_duration = round(float(data['format']['duration']), 2)
        video_size = round(float(data['format']['size']) / (1024 * 1024), 2)
        video_bitrate = data['format']['bit_rate']
        video_format = data['format']['format_name']
        video_width = data['streams'][1]['width']
        video_height = data['streams'][1]['height']
        video_framerate = data['streams'][1]['r_frame_rate'].split("/")[0]
        video_codec = data['streams'][1]['codec_name']
        video_codec_type = data['streams'][1]['codec_type']

        # Audio data
        audio_codec = data['streams'][0]['codec_name']
        audio_codec_type = data['streams'][0]['codec_type']
        audio_simple_rate = data['streams'][0]['sample_rate']
        audio_channels = data['streams'][0]['channels']
        audio_bitrate = data['streams'][0]['bit_rate']

    else:
        # Video data
        video_duration = round(float(data['format']['duration']), 2)
        video_size = round(float(data['format']['size']) / (1024 * 1024), 2)
        video_bitrate = data['format']['bit_rate']
        video_format = data['format']['format_name']
        video_width = data['streams'][0]['width']
        video_height = data['streams'][0]['height']
        video_framerate = data['streams'][0]['r_frame_rate'].split("/")[0]
        video_codec = data['streams'][0]['codec_name']
        video_codec_type = data['streams'][0]['codec_type']

        # Audio data
        audio_codec = data['streams'][1]['codec_name']
        audio_codec_type = data['streams'][1]['codec_type']
        audio_simple_rate = data['streams'][1]['sample_rate']
        audio_channels = data['streams'][1]['channels']
        audio_bitrate = data['streams'][1]['bit_rate']


    BG_COLOR = "#1a1a2e"
    PRIMARY_COLOR = "#4cc9f0"
    SECONDARY_COLOR = "#f72585"
    TEXT_COLOR = "#ffffff"
    HOVER_COLOR = "#3a86ff"

    app.title("Video Compressor")
    app.geometry("620x440+300+100")
    app.resizable(False, False)
    app.configure(bg=BG_COLOR)

    # ======= Menu Bar ========
    menu_bar = Frame(app, bg=PRIMARY_COLOR, height=22, bd=0, relief=FLAT)
    menu_bar.pack(fill=X)

    menu = Menu(app, tearoff=0, bg=PRIMARY_COLOR, fg=TEXT_COLOR, activebackground=HOVER_COLOR, activeforeground=TEXT_COLOR)
    menu.add_command(label="Exit", command=app.quit)

    def on_enter(e): e.widget.config(bg=HOVER_COLOR)
    def on_leave(e): e.widget.config(bg=PRIMARY_COLOR)

    file_btn = Button(menu_bar, text="File", bg=PRIMARY_COLOR, fg=TEXT_COLOR, font=("Inter", 10, "bold"), relief=FLAT)
    file_btn.place(x=2, y=0, width=45, height=22)
    file_btn.bind("<Button-1>", show_menu)
    file_btn.bind("<Enter>", on_enter)
    file_btn.bind("<Leave>", on_leave)

    preview_btn = Button(menu_bar, text="Summary", bg=PRIMARY_COLOR, fg=TEXT_COLOR, font=("Inter", 10, "bold"), relief=FLAT, command=lambda: show_frame(preview_info_frame))
    preview_btn.place(x=50, y=0, width=70, height=22)
    preview_btn.bind("<Enter>", on_enter)
    preview_btn.bind("<Leave>", on_leave)

    video_btn = Button(menu_bar, text="Video", bg=PRIMARY_COLOR, fg=TEXT_COLOR, font=("Inter", 10, "bold"), relief=FLAT, command=lambda: show_frame(video_info_frame))
    video_btn.place(x=125, y=0, width=55, height=22)
    video_btn.bind("<Enter>", on_enter)
    video_btn.bind("<Leave>", on_leave)

    audio_btn = Button(menu_bar, text="Audio", bg=PRIMARY_COLOR, fg=TEXT_COLOR, font=("Inter", 10, "bold"), relief=FLAT, command=lambda: show_frame(audio_info_frame))
    audio_btn.place(x=185, y=0, width=55, height=22)
    audio_btn.bind("<Enter>", on_enter)
    audio_btn.bind("<Leave>", on_leave)

    settings_btn = Button(menu_bar, text="Settings", bg=PRIMARY_COLOR, fg=TEXT_COLOR, font=("Inter", 10, "bold"), relief=FLAT)
    settings_btn.place(x=245, y=0, width=70, height=22)
    settings_btn.bind("<Enter>", on_enter)
    settings_btn.bind("<Leave>", on_leave)

    help_btn = Button(menu_bar, text="Help", bg=PRIMARY_COLOR, fg=TEXT_COLOR, font=("Inter", 10, "bold"), relief=FLAT)
    help_btn.place(x=320, y=0, width=55, height=22)
    help_btn.bind("<Enter>", on_enter)
    help_btn.bind("<Leave>", on_leave)

    run_btn = Button(menu_bar, text="Run", bg=SECONDARY_COLOR, fg=TEXT_COLOR, font=("Inter", 10, "bold"), relief=FLAT, command=run_command, activebackground=HOVER_COLOR)
    run_btn.place(x=380, y=0, width=55, height=22)
    run_btn.bind("<Enter>", lambda e: run_btn.config(bg=HOVER_COLOR))
    run_btn.bind("<Leave>", lambda e: run_btn.config(bg=SECONDARY_COLOR))

    # ====== Frames ======
    video_info_frame = Frame(app, bg=PRIMARY_COLOR, bd=0, relief=FLAT)
    audio_info_frame = Frame(app, bg=SECONDARY_COLOR, bd=0, relief=FLAT)
    preview_info_frame = Frame(app, bg=HOVER_COLOR, bd=0, relief=FLAT)

    audio_info_frame.place(relx=0.5, rely=0.48, anchor="center", width=580, height=320)

    # ====== File Path Frame ====
    file_path_label = Label(app, text="File Path:", bg=BG_COLOR, fg=TEXT_COLOR, font=("Inter", 11, "bold"))
    file_path_label.place(relx=0.07, rely=0.93, anchor="center")

    file_path_entry = Entry(app, bg=PRIMARY_COLOR, fg=TEXT_COLOR, font=("Inter", 13), relief=FLAT, insertbackground=TEXT_COLOR)
    file_path_entry.place(relx=0.48, rely=0.93, anchor="center", width=420)
    file_path_entry.insert(END, output_file_path)

    file_path_btn = Button(app, text="Browse", bg=SECONDARY_COLOR, fg=TEXT_COLOR, font=("Inter", 9, "bold"), relief=FLAT, command=select_path, activebackground=HOVER_COLOR)
    file_path_btn.place(relx=0.91, rely=0.93, anchor="center")
    file_path_btn.bind("<Enter>", lambda e: file_path_btn.config(bg=HOVER_COLOR))
    file_path_btn.bind("<Leave>", lambda e: file_path_btn.config(bg=SECONDARY_COLOR))

    get_frames()

    # ====== Preview Info Frame ====
    preview_label = Label(preview_info_frame, image=image_ref[0], bg=HOVER_COLOR)
    preview_label.place(relx=0.8, rely=0.5, anchor="center")

    file_name_label = Label(preview_info_frame, text=f"File Name: {input_file_name}", bg=HOVER_COLOR, fg=TEXT_COLOR, font=("Inter", 11, "bold"))
    file_name_label.place(relx=0.01, rely=0.1, anchor="w")

    file_size_label = Label(preview_info_frame, text=f"File Size: {video_size} MB", bg=HOVER_COLOR, fg=TEXT_COLOR, font=("Inter", 11))
    file_size_label.place(relx=0.01, rely=0.2, anchor="w")

    file_encoder_label = Label(preview_info_frame, text=f"Video Encoder: {video_codec}", bg=HOVER_COLOR, fg=TEXT_COLOR, font=("Inter", 11))
    file_encoder_label.place(relx=0.01, rely=0.3, anchor="w")

    file_dimensions_label = Label(preview_info_frame, text=f"Video Dimensions: {video_width}x{video_height}", bg=HOVER_COLOR, fg=TEXT_COLOR, font=("Inter", 11))
    file_dimensions_label.place(relx=0.01, rely=0.4, anchor="w")

    file_framerate_label = Label(preview_info_frame, text=f"Video Frame Rate: {video_framerate}", bg=HOVER_COLOR, fg=TEXT_COLOR, font=("Inter", 11))
    file_framerate_label.place(relx=0.01, rely=0.5, anchor="w")

    file_duration_label = Label(preview_info_frame, text=f"Video Duration: {video_duration} seconds", bg=HOVER_COLOR, fg=TEXT_COLOR, font=("Inter", 11))
    file_duration_label.place(relx=0.01, rely=0.6, anchor="w")

    file_format_label = Label(preview_info_frame, text=f"File Format: {input_file_extension}", bg=HOVER_COLOR, fg=TEXT_COLOR, font=("Inter", 11))
    file_format_label.place(relx=0.01, rely=0.7, anchor="w")

    file_bitrate_label = Label(preview_info_frame, text=f"Video Bitrate: {video_bitrate} bps", bg=HOVER_COLOR, fg=TEXT_COLOR, font=("Inter", 11))
    file_bitrate_label.place(relx=0.01, rely=0.8, anchor="w")

    audio_bitrate_label = Label(preview_info_frame, text=f"Audio Bitrate: {audio_bitrate} bps", bg=HOVER_COLOR, fg=TEXT_COLOR, font=("Inter", 11))
    audio_bitrate_label.place(relx=0.01, rely=0.9, anchor="w")

    # ====== Video Info Frame ====
    video_label = Label(video_info_frame, text="Video", bg=PRIMARY_COLOR, fg=BG_COLOR, font=("Inter", 14, "bold"))
    video_label.place(relx=0.01, rely=0.05, anchor="w")

    video_encoder_label = Label(video_info_frame, text="Video Encoder:", bg=PRIMARY_COLOR, fg=TEXT_COLOR, font=("Inter", 11))
    video_encoder_label.place(relx=0.01, rely=0.15, anchor="w")

    video_encoder_combobox = ttk.Combobox(video_info_frame, values=["H.264", "H.265", "VP9"], state="readonly")
    video_encoder_combobox.set("H.264")
    video_encoder_combobox.place(relx=0.22, rely=0.15, anchor="w")

    video_fbs_label = Label(video_info_frame, text="Video FPS:", bg=PRIMARY_COLOR, fg=TEXT_COLOR, font=("Inter", 11))
    video_fbs_label.place(relx=0.01, rely=0.25, anchor="w")

    video_fbs_combobox = ttk.Combobox(video_info_frame, values=[
        "23.976", "24", "25", "29.97", "30", "50", "59.94", "60", "120", "144", "240"], state="readonly")
    video_fbs_combobox.set("30")
    video_fbs_combobox.place(relx=0.22, rely=0.25, anchor="w")

    video_encoder_option_label = Label(video_info_frame, text="Video Options:", bg=PRIMARY_COLOR, fg=BG_COLOR, font=("Inter", 14, "bold"))
    video_encoder_option_label.place(relx=0.01, rely=0.35, anchor="w")

    video_present_label = Label(video_info_frame, text="Video Preset:", bg=PRIMARY_COLOR, fg=TEXT_COLOR, font=("Inter", 11))
    video_present_label.place(relx=0.01, rely=0.45, anchor="w")

    video_preset_combobox = ttk.Combobox(video_info_frame, values=["ultrafast", "superfast", "veryfast", "faster", "fast", "medium", "slow", "veryslow"], state="readonly")
    video_preset_combobox.set("medium")
    video_preset_combobox.place(relx=0.22, rely=0.45, anchor="w")

    video_encoder_level_label = Label(video_info_frame, text="Encoder Level:", bg=PRIMARY_COLOR, fg=TEXT_COLOR, font=("Inter", 11))
    video_encoder_level_label.place(relx=0.01, rely=0.55, anchor="w")

    video_encoder_level_combobox = ttk.Combobox(video_info_frame, values=[1, 1.1, 1.2, 1.3, 2, 2.1, 2.2, 3, 3.1, 3.2, 4, 4.1, 4.2, 5, 5.1, 5.2, 6, 6.1, 6.2], state="readonly")
    video_encoder_level_combobox.set("4")
    video_encoder_level_combobox.place(relx=0.22, rely=0.55, anchor="w")

    video_quality_scale_label = Label(video_info_frame, text="Quality:", bg=PRIMARY_COLOR, fg=BG_COLOR, font=("Inter", 14, "bold"))
    video_quality_scale_label.place(relx=0.01, rely=0.65, anchor="w")

    video_quality_scale_scale = Scale(video_info_frame, from_=0, to=51, orient="horizontal", bg=PRIMARY_COLOR, fg=TEXT_COLOR, width=20, length=200, sliderlength=20, troughcolor=SECONDARY_COLOR, activebackground=HOVER_COLOR, highlightbackground=PRIMARY_COLOR, highlightcolor=SECONDARY_COLOR)
    video_quality_scale_scale.set(23)
    video_quality_scale_scale.place(relx=0.22, rely=0.75, anchor="w")

    video_quality_high_label = Label(video_info_frame, text="High Quality", bg=PRIMARY_COLOR, fg=TEXT_COLOR, font=("Inter", 11))
    video_quality_high_label.place(relx=0.16, rely=0.9, anchor="w")

    video_quality_low_label = Label(video_info_frame, text="Low Quality", bg=PRIMARY_COLOR, fg=TEXT_COLOR, font=("Inter", 11))
    video_quality_low_label.place(relx=0.5, rely=0.9, anchor="w")

    # ====== Audio Info Frame ====
    audio_label = Label(audio_info_frame, text="Audio", bg=SECONDARY_COLOR, fg=BG_COLOR, font=("Inter", 14, "bold"))
    audio_label.place(relx=0.01, rely=0.05, anchor="w")

    audio_encoder_label = Label(audio_info_frame, text="Audio Encoder:", bg=SECONDARY_COLOR, fg=TEXT_COLOR, font=("Inter", 11))
    audio_encoder_label.place(relx=0.01, rely=0.15, anchor="w")

    audio_encode_combobox = ttk.Combobox(audio_info_frame, values=["aac", "libmp3lame", "flac", "ac3", "opus", "vorbis", "pcm_s16le", "alac"], state="readonly")
    audio_encode_combobox.set("AAC")
    audio_encode_combobox.place(relx=0.22, rely=0.15, anchor="w")

    audio_bitrate_label = Label(audio_info_frame, text="Audio Bitrate:", bg=SECONDARY_COLOR, fg=TEXT_COLOR, font=("Inter", 11))
    audio_bitrate_label.place(relx=0.01, rely=0.25, anchor="w")

    audio_bitrate_combobox = ttk.Combobox(audio_info_frame, values=["64k", "128k", "192k", "256k"], state="readonly")
    audio_bitrate_combobox.set("128k")
    audio_bitrate_combobox.place(relx=0.22, rely=0.25, anchor="w")

    audio_channels_label = Label(audio_info_frame, text="Audio Channels:", bg=SECONDARY_COLOR, fg=TEXT_COLOR, font=("Inter", 11))
    audio_channels_label.place(relx=0.01, rely=0.35, anchor="w")

    audio_channels_combobox = ttk.Combobox(audio_info_frame, values=["Mono", "Stereo"], state="readonly")
    audio_channels_combobox.set("Stereo")
    audio_channels_combobox.place(relx=0.22, rely=0.35, anchor="w")

    audio_volume_label = Label(audio_info_frame, text="Volume:", bg=SECONDARY_COLOR, fg=TEXT_COLOR, font=("Inter", 11))
    audio_volume_label.place(relx=0.01, rely=0.45, anchor="w")

    audio_volume_combobox = ttk.Combobox(audio_info_frame, values=["0.5", "1.0", "1.5", "2.0"], state="readonly")
    audio_volume_combobox.set("1.0")
    audio_volume_combobox.place(relx=0.22, rely=0.45, anchor="w")



    app.mainloop()