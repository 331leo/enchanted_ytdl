import youtube_dl
import os
import datetime
import time
import wget
import shutil
import psutil
import math
import platform
versionnum="CLI_1.1.6"
_ = os.system("title Youtube Downloader (Made By Leok.kr)")
run_time=str(datetime.datetime.now())[:19].replace(":","_")
isWindows=False
isMac=False
isLinux=False
if platform.system() == 'Windows':
    isWindows = True
elif platform.system() == "Darwin":
    isMac = True
elif platform.system() == "Linux":
    isLinux = True

def clear():
    if isWindows:
        _ = os.system('cls')

    else:
        _ = os.system('clear')

def bar_custom(current, total, width=80):
    width=30
    avail_dots = width-2
    shaded_dots = int(math.floor(float(current) / total * avail_dots))
    percent_bar = '[' + '■'*shaded_dots + ' '*(avail_dots-shaded_dots) + ']'
    progress = "%d%% %s [%d / %d]" % (current / total * 100, percent_bar, current, total)
    return progress

def checkffmpeg():
    if isWindows:
        if not os.path.isfile("ffmpeg.exe"):
            print("필수요소 ffmpeg 다운로드..")
            wget.download("https://leok.kr/file/windows/ffmpeg.exe",bar=bar_custom)
            print("")
        if not os.path.isfile("ffprobe.exe"):
            print("필수요소 ffprobe 다운로드..")
            wget.download("https://leok.kr/file/windows/ffprobe.exe",bar=bar_custom)
            print("")
    elif isMac:
        if not os.path.isfile("ffmpeg"):
            print("필수요소 ffmpeg 다운로드..")
            wget.download("https://leok.kr/file/macos/ffmpeg",bar=bar_custom)
            print("")
        if not os.path.isfile("ffprobe"):
            print("필수요소 ffprobe 다운로드..")
            wget.download("https://leok.kr/file/macos/ffprobe",bar=bar_custom)
            print("")
    elif isLinux:
        if not os.path.isfile("ffmpeg"):
            print("필수요소 ffmpeg 다운로드..")
            wget.download("https://leok.kr/file/linux/ffmpeg",bar=bar_custom)
            print("")
        if not os.path.isfile("ffprobe"):
            print("필수요소 ffprobe 다운로드..")
            wget.download("https://leok.kr/file/linux/ffprobe",bar=bar_custom)
            print("")
    clear()

def download(o_type,linkinputmode):
    links = []
    if o_type == "mp3":
        o_type_human = "음악파일(mp3)"
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': f"./downloaded_{o_type}/{run_time}/%(title)s.%(ext)s",
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            },{'key': 'FFmpegMetadata'},],
        }
    elif o_type == "mp4":
        o_type_human = "mp4"
        ydl_opts = {
            'format': 'bestvideo+bestaudio',
            'outtmpl': f"./downloaded_{o_type}/{run_time}/%(title)s.%(ext)s",
            'postprocessors': [{
                'key': 'FFmpegVideoConvertor',
                'preferedformat': 'mp4',
            },
        {'key': 'FFmpegMetadata'},],
        }
    elif o_type == "ori_video":
        o_type_human = "원본영상으"
        ydl_opts = {
            'format': 'bestvideo+bestaudio',
            'outtmpl': f"./downloaded_{o_type}/{run_time}/%(title)s.%(ext)s",
            'postprocessors': [{'key': 'FFmpegMetadata'},],
        }
    if linkinputmode == "1":
        linput_type="download.txt"
        if not os.path.isfile(f"download.txt"):
            f = open(f"download.txt", "w")
            f.close()
            input(f"download.txt 파일이 존재하지 않습니다.\n해당 파일을 생성하였으니, 해당 파일에 {o_type_human}로 다운받고 싶은 유튜브 영상들의 링크를 넣으신후 다시 실행해 주세요.\n\n> 엔터를 누르시면 메뉴로 돌아갑니다. ")
            return
        else:
            f=open(f"download.txt","r",encoding="UTF-8")
            links = f.readlines()
            f.close()
    elif linkinputmode == "2":
        linput_type = "사용자 입력 링크"
        links.append(input(f"> {o_type_human}로 다운받을 영상의 링크를 입력하세요: "))

    if len(links) >= 1:
        if len(links[0]) >= 5:
            print(f"{linput_type} 를 읽어와, {o_type_human}로 다운로드를 시작합니다.")
            time.sleep(1)
            os.makedirs(f"./downloaded_{o_type}/{run_time}",exist_ok=True)
            try:
                with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                    ydl.download(links)
            except Exception as e:
                clear()
                print(f"다운로드가 불가능 합니다.\n{e}\n")
                input("> 엔터를 누르시면 메뉴로 돌아갑니다. ")
                return
            if linput_type == "download.txt":
                shutil.move(f"./download.txt",f"./downloaded_{o_type}/{run_time}/!downloaded_{o_type}_links.txt")
                f = open(f"download.txt", "w")
                f.close()
            clear()
            print(f"다운로드가 완료되었습니다.\n./downloaded_{o_type}/{run_time} 에 저장하였습니다!\n{linput_type} 를 초기화 하였습니다!")
            if isWindows:
                os.system(f"explorer downloaded_{o_type}\{run_time}")
                print("\n다운로드된 폴더를 열었습니다!")
            input("> 엔터를 누르시면 메뉴로 돌아갑니다. ")
            return
        else:
            input(f"{linput_type} 이(가) 비어있거나, 올바르지 않습니다.\n해당 파일에 {o_type_human}로 다운받고 싶은 유튜브 영상들의 링크를 넣어주세요.\n\n> 엔터를 누르시면 메뉴로 돌아갑니다. ")
            return
    else:
        input(f"{linput_type} 이(가) 비어있거나, 올바르지 않습니다.\n해당 파일에 {o_type_human}로 다운받고 싶은 유튜브 영상들의 링크를 넣어주세요.\n\n> 엔터를 누르시면 메뉴로 돌아갑니다. ")
        return


def menu():
    def isfilemode():
        ok = True
        while ok:
            print("다운로드 방식을 선택하세요.")
            print("[1] 파일로 부터 링크 가져오기(많은 영상 동시 다운로드)")
            print("[2] 영상 링크 직접 입력(하나씩 다운로드)")
            print("[q] 메인메뉴")
            c = input("> ")
            clear()
            if c == "1" or c == "2" or c == "q":
                ok = False
        return c
    if not isWindows:
        print("윈도우 환경이 아닙니다. 올바르게 작동하지 않을 가능성이 높습니다.")
    print("프로그램 동작 모드를 선택하세요.")
    print("[1] 음악 다운로드 모드")
    print("[2] 영상 다운로드 모드(포멧: mkv)")
    print("[3] 영상 다운로드 모드(강제 mp4변환, 오래걸림)")
    print("[q] 종료")
    c = input("> ")
    clear()

    if c == "1":
        r=isfilemode()
        if r == "q":
            return 1
        download("mp3",r)

    elif c == "2":
        r = isfilemode()
        if r == "q":
            return 1
        download("ori_video",r)
    elif c == "3":
        r = isfilemode()
        if r == "q":
            return 1
        download("mp4",r)
    elif c == "i":
        clear()
        infotext = f"**INFO**\n\nMade by: LeoK (leok.kr)\nSpecial Thanks to: Youtube_Dl, FFMPEG\nPlatform: {platform.platform()}, {psutil.Process(os.getppid()).name()}\nVersion: {versionnum}\nSupport: support@leok.kr"
        print(infotext)
        input("\n> 엔터를 누르면 메인화면으로 돌아갑니다.")
        clear()
    elif c == "q":
        return 0
    clear()

checkffmpeg()
clear()
while True:
    if menu() == 0:
        break