import tkinter
import sys
from time import sleep
import webbrowser
import speech_recognition as sr
import os

root = tkinter.Tk()
root.title("Quick Bookmark")
root.geometry("400x550")
root.resizable(0, 0)

def open_google():
    sleep(0.5)
    webbrowser.open("https://www.google.co.jp/")

def open_youtube():
    sleep(0.5)
    webbrowser.open("https://www.youtube.com/")

def open_qiita():
    sleep(0.5)
    webbrowser.open("https://qiita.com/")

def open_twitter():
    sleep(0.5)
    webbrowser.open("https://twitter.com/")

def open_yahoo():
    sleep(0.5)
    webbrowser.open("https://www.yahoo.co.jp/")

def exit_app():
    root.destroy()
    sys.exit()

# 音声認識
def recognize_speech():
    recognizer = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            print("操作コマンドを話してください...")
            audio = recognizer.listen(source)
            try:
                command = recognizer.recognize_google(audio, language='ja-JP')
                print(f"認識されたコマンド: {command}")
                return command
            except sr.UnknownValueError:
                print("音声を認識できませんでした。")
            except sr.RequestError as e:
                print(f"Google Speech Recognition API エラー: {e}")
    except OSError as e:
        print(f"マイクが使用できません: {e}")
    return None

# コマンド処理
def execute_command(command):
    if "ブラウザ" in command:
        print("ブラウザを開きます...")
        os.system("start chrome")  # Chromeを起動
    elif "音量を上げて" in command:
        print("音量を上げます...")
        for _ in range(5):
            keyboard.press_and_release("volumeup")  # 音量アップ
    elif "音量を下げて" in command:
        print("音量を下げます...")
        for _ in range(5):
            keyboard.press_and_release("volumedown")  # 音量ダウン
    elif "スクリーンショット" in command:
        print("スクリーンショットを撮影します...")
        pyautogui.screenshot("screenshot.png")
    elif "終了" in command:
        print("プログラムを終了します。")
        exit_app()
    else:
        print("コマンドが認識されませんでした。")

# GUI
label = tkinter.Label(text="ブックマーク", background='#7fffd4', font=("MSゴシック", "30", "bold"), foreground='#000000')
label.pack()

button1 = tkinter.Button(text='Googleを開く', width=50, command=open_google)
button1.pack()

button2 = tkinter.Button(text='YouTubeを開く', width=50, command=open_youtube)
button2.pack()

button3 = tkinter.Button(text='Qiitaを開く', width=50, foreground="#00ff00", command=open_qiita)
button3.pack()

button4 = tkinter.Button(text='Twitterを開く', width=50, foreground="#00ffff", command=open_twitter)
button4.pack()

button5 = tkinter.Button(text='YahooJapanを開く', width=50, command=open_yahoo)
button5.pack()

button6 = tkinter.Button(text='終了', width=50, command=exit_app)
button6.pack()

root.mainloop()

# 音声認識ループ
if __name__ == "__main__":
    while True:
        command = recognize_speech()
        if command:
            execute_command(command())
