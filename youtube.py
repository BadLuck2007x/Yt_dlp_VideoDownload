from urllib.parse import urlparse, parse_qs
import yt_dlp
import os


def clear_console()->None:
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')


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

 


def main()->None:
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
    clear_console()
    print("Your urls are:")
    for url in urls:
        print(url)
    conform =input("Hit 'enter' to conform or press '0' to stop: ")
    clear_console()
    if conform =='0':
        return
    else:
        videos =Downloader(urls)
        videos.YT_Download()
        print("\tNow check the 'Downloads' folder for results")

    
if __name__ =="__main__":
    print("~~Starting~~")
    main()


