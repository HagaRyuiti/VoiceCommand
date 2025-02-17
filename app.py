import tkinter as tk
import sqlite3
import webbrowser
import speech_recognition as sr
import os


# SQLite データベースの作成
conn = sqlite3.connect("commands.db")
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS commands (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    voice_command TEXT UNIQUE NOT NULL,
    url TEXT
)
""")
conn.commit()

# Tkinter ウィンドウの作成
root = tk.Tk()
root.title("音声コマンド登録システム")
root.geometry("500x400")

# URL と 音声コマンドの入力欄
tk.Label(root, text="音声コマンド").pack()
command_entry = tk.Entry(root, width=50)
command_entry.pack()

tk.Label(root, text="URL").pack()
url_entry = tk.Entry(root, width=50)
url_entry.pack()

# データベースに登録
def save_command():
    command = command_entry.get()
    url = url_entry.get()
    
    if command and url:
        try:
            cursor.execute("INSERT INTO commands (voice_command, url) VALUES (?, ?)", (command, url))
            conn.commit()
            status_label.config(text="登録完了！")
            command_entry.delete(0, tk.END)
            url_entry.delete(0, tk.END)
            load_commands()
        except sqlite3.IntegrityError:
            status_label.config(text="エラー: 同じコマンドが既に存在します。")
    else:
        status_label.config(text="エラー: コマンドとURLを入力してください。")

tk.Button(root, text="登録", command=save_command).pack()

# 登録されたコマンドのリスト表示
commands_listbox = tk.Listbox(root, width=50)
commands_listbox.pack()

def load_commands():
    commands_listbox.delete(0, tk.END)
    cursor.execute("SELECT voice_command, url FROM commands")
    for row in cursor.fetchall():
        commands_listbox.insert(tk.END, f"{row[0]} -> {row[1]}")

load_commands()

# ステータス表示
status_label = tk.Label(root, text="")
status_label.pack()

# 音声認識でコマンド実行
def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("音声コマンドを話してください...")
        try:
            audio = recognizer.listen(source)
            command = recognizer.recognize_google(audio, language='ja-JP')
            print(f"認識されたコマンド: {command}")
            execute_command(command)
        except sr.UnknownValueError:
            print("音声を認識できませんでした。")
        except sr.RequestError as e:
            print(f"Google Speech Recognition API エラー: {e}")

# コマンド実行
def execute_command(command):
    cursor.execute("SELECT url FROM commands WHERE voice_command=?", (command,))
    result = cursor.fetchone()
    
    if result:
        print(f"登録されたURLを開きます: {result[0]}")
        webbrowser.open(result[0])
    elif "終了" in command:
        print("プログラムを終了します。")
        root.quit()
    else:
        print("コマンドが認識されませんでした。")

# 音声認識ボタン
tk.Button(root, text="音声認識開始", command=recognize_speech).pack()

# メインループ開始
root.mainloop()
