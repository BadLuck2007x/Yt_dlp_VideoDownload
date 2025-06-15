from urllib.parse import urlparse, parse_qs
import yt_dlp
import os
import platform
import tkinter as tk
from tkinter import font

def SystemConfig():
    system =platform.system()
    if 'android' in platform.platform().lower():
        return False
    else:
        return  True

class Downloader:
    def __init__(self, urls):
        self.downloads_path = os.path.join(os.path.expanduser("~"), "Downloads/Yt-dlp-media")
        outtmpl_path = os.path.join(self.downloads_path, '%(title)s.%(ext)s')
        self.urls = urls
        self.format = {
                'format': 'best',
                'outtmpl': outtmpl_path,
            }
    
    def __UrlConfig(self)->None:
        fixed_urls = []
        for url in self.urls:
            parsed = urlparse(url)
            if 'youtu.be' in parsed.netloc:
                video_id = parsed.path.lstrip('/')
            elif 'youtube.com' in parsed.netloc:
                query = parse_qs(parsed.query)
                video_id = query.get("v", [None])[0]
            else:
                video_id = None
            if video_id:
                fixed_urls.append(f"https://www.youtube.com/watch?v={video_id}")
        self.urls = fixed_urls

    def YT_Download(self)->None:
        try:
            self.__UrlConfig()
            with yt_dlp.YoutubeDL(self.format) as video:
                video.download(self.urls)
            if os.name =='posix':
                self.ReScanMedia()
        except yt_dlp.utils.DownloadError as e:
            print(f"Error :{e}")
    
    def ReScanMedia(self):
        for filename in os.listdir(self.downloads_path):
            file_path = os.path.join(self.downloads_path, filename)
            if os.path.isfile(file_path):
                os.system(f"am broadcast -a android.intent.action.MEDIA_SCANNER_SCAN_FILE -d file://{file_path}")
                print(f"Scanned: {file_path}")


def Logic_Caller(urls):
    videos =Downloader(urls)
    videos.YT_Download()
    print("\tNow check the 'Downloads/Yt-dlp-media' folder for results")

def CUI_Main()->None:
    urls = []
    print("Enter YouTube URLs (type '0' to finish):" )
    i=1
    while True:
        user_inp= input(f"Enter no-{i} url: ")
        if user_inp =="0":
            break
        elif user_inp.startswith("https://"):
            urls.append(user_inp)
        else:
            print("Url is not valid.Only 'https:// will valid'")
        i+=1
    print("Your urls are:")
    for url in urls:
        print(url)
    conform =input("Hit 'enter' to conform or press '0' to stop: ")
    if conform =='0':
        return
    else:
        Logic_Caller(urls)


class GUI_Downloader:
    def __init__(self, root):
        self.root = root
        self.root.title("YT Downloader Pro")
        self.root.geometry("650x500")
        self.root.configure(bg="#2d2d2d")
        self.root.resizable(0, 0)
        
        self.i = 1
        self.entries = []
        
        self.title_font = font.Font(family="Arial", size=14, weight="bold")
        self.button_font = font.Font(family="Arial", size=10)
        
        self.setup_header()
        self.setup_form()
        self.setup_buttons()
        self.setup_status()
        
        self.canvas.bind_all("<MouseWheel>", self.scroll_action)

    def setup_header(self):
        header = tk.Frame(self.root, bg="#252525", height=50)
        header.pack(fill="x")
        tk.Label(header, text="YouTube Downloader", fg="#4fc3f7", bg="#252525", font=self.title_font).pack(side="left", padx=20)

    def setup_form(self):
        form_frame = tk.Frame(self.root, bg="#2d2d2d")
        form_frame.pack(fill="both", expand=1, padx=20, pady=10)
        
        first_frame = tk.Frame(form_frame, bg="#2d2d2d", pady=5)
        first_frame.pack(fill="x")
        
        tk.Label(first_frame, text="URL 1:", bg="#2d2d2d", fg="#e0e0e0").pack(side="left")
        self.first_entry = tk.Entry(first_frame, bg="#3d3d3d", fg="white", width=50)
        self.first_entry.pack(side="left", fill="x", expand=1, padx=10)
        
        scroll_border = tk.Frame(form_frame, bg="#3d3d3d")
        scroll_border.pack(fill="both", expand=1)
        
        scroll_container = tk.Frame(scroll_border, bg="#2d2d2d")
        scroll_container.pack(fill="both", expand=1, padx=1, pady=1)
        
        self.canvas = tk.Canvas(scroll_container, bg="#2d2d2d", highlightthickness=0)
        self.scrollbar = tk.Scrollbar(scroll_container, command=self.canvas.yview)
        self.scroll_frame = tk.Frame(self.canvas, bg="#2d2d2d")
        
        self.scroll_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.create_window((0, 0), window=self.scroll_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        self.scrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=1)

    def setup_buttons(self):
        btn_frame = tk.Frame(self.root, bg="#2d2d2d")
        btn_frame.pack(fill="x", padx=20, pady=10)
        
        tk.Button(btn_frame, text="+ Add URL", command=self.add_url, 
                 bg="#3d3d3d", fg="white", width=12).pack(side="left", padx=5)
        
        tk.Button(btn_frame, text="Download All", command=self.get_urls, 
                 bg="#1565c0", fg="white", width=12).pack(side="left", padx=5)

    def setup_status(self):
        self.status = tk.Label(self.root, text="Ready", fg="#b0bec5", bg="#252525", anchor="w")
        self.status.pack(fill="x", side="bottom")

    def add_url(self):
        self.i += 1
        frame = tk.Frame(self.scroll_frame, bg="#2d2d2d")
        frame.pack(fill="x", padx=5, pady=3)
        
        tk.Label(frame, text=f"URL {self.i}:", bg="#2d2d2d", fg="#e0e0e0").pack(side="left")
        entry = tk.Entry(frame, bg="#3d3d3d", fg="white", width=50)
        entry.pack(side="left", fill="x", expand=1, padx=10)
        self.entries.append(entry)
        
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        self.canvas.yview_moveto(1.0)

    def get_urls(self):
        urls = [self.first_entry.get().strip()]
        urls += [e.get().strip() for e in self.entries]
        urls = [u for u in urls if u]
        
        if urls:
            self.status.config(text=f"Downloading {len(urls)} videos...")
            Logic_Caller(urls=urls)
        else:
            self.status.config(text="No URLs entered!")

    def scroll_action(self, event):
        self.canvas.yview_scroll(-1 * (event.delta // 120), "units")



system = platform.system().lower()
if system =='windows' or system =="linux" or system=="darwin":
    root = tk.Tk()
    GUI_Downloader(root)
    root.mainloop()
else:
    CUI_Main()

