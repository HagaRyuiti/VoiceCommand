import tkinter as tk
from tkinter import ttk
import sqlite3
import webbrowser
import speech_recognition as sr
import os
import subprocess

# SQLite データベースの作成
conn = sqlite3.connect("commands.db")
cursor = conn.cursor()

# データベースのテーブル作成（command_typeカラムを追加）
cursor.execute("""
CREATE TABLE IF NOT EXISTS commands (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    voice_command TEXT UNIQUE NOT NULL,
    command_type TEXT NOT NULL,
    command_value TEXT NOT NULL
)
""")
conn.commit()

# Tkinter ウィンドウの作成
root = tk.Tk()
root.title("音声コマンド管理システム")
root.geometry("500x450")

# タブ作成
notebook = ttk.Notebook(root)
notebook.pack(expand=True, fill="both")

# 各タブのフレーム
url_tab = ttk.Frame(notebook)
app_tab = ttk.Frame(notebook)
shell_tab = ttk.Frame(notebook)

notebook.add(url_tab, text="URL")
notebook.add(app_tab, text="アプリ実行")
notebook.add(shell_tab, text="シェルコマンド")

# コマンドと入力欄
tk.Label(root, text="音声コマンド").pack()
command_entry = tk.Entry(root, width=50)
command_entry.pack()

# タブごとの入力欄
tk.Label(url_tab, text="開くURL").pack()
url_entry = tk.Entry(url_tab, width=50)
url_entry.pack()

tk.Label(app_tab, text="実行するアプリのパス").pack()
app_entry = tk.Entry(app_tab, width=50)
app_entry.pack()

tk.Label(shell_tab, text="実行するシェルコマンド").pack()
shell_entry = tk.Entry(shell_tab, width=50)
shell_entry.pack()

# データベースに登録
def save_command(command_type):
    command = command_entry.get()
    
    if command_type == "url":
        value = url_entry.get()
    elif command_type == "app":
        value = app_entry.get()
    elif command_type == "shell":
        value = shell_entry.get()
    
    if command and value:
        try:
            cursor.execute("INSERT INTO commands (voice_command, command_type, command_value) VALUES (?, ?, ?)", 
                           (command, command_type, value))
            conn.commit()
            status_label.config(text="登録完了！")
            command_entry.delete(0, tk.END)
            url_entry.delete(0, tk.END)
            app_entry.delete(0, tk.END)
            shell_entry.delete(0, tk.END)
            load_commands()
        except sqlite3.IntegrityError:
            status_label.config(text="エラー: 同じコマンドが既に存在します。")
    else:
        status_label.config(text="エラー: コマンドと値を入力してください。")

tk.Button(url_tab, text="URLを登録", command=lambda: save_command("url")).pack()
tk.Button(app_tab, text="アプリを登録", command=lambda: save_command("app")).pack()
tk.Button(shell_tab, text="シェルコマンドを登録", command=lambda: save_command("shell")).pack()

# コマンドリスト表示
commands_listbox = tk.Listbox(root, width=50)
commands_listbox.pack()

def load_commands():
    commands_listbox.delete(0, tk.END)
    cursor.execute("SELECT voice_command, command_type, command_value FROM commands")
    for row in cursor.fetchall():
        commands_listbox.insert(tk.END, f"{row[0]} ({row[1]}) -> {row[2]}")

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
    cursor.execute("SELECT command_type, command_value FROM commands WHERE voice_command=?", (command,))
    result = cursor.fetchone()
    
    if result:
        command_type, command_value = result
        if command_type == "url":
            print(f"URLを開きます: {command_value}")
            webbrowser.open(command_value)
        elif command_type == "app":
            print(f"アプリを起動します: {command_value}")
            try:
                os.startfile(command_value)
            except Exception as e:
                print(f"アプリ実行エラー: {e}")
        elif command_type == "shell":
            print(f"シェルコマンドを実行します: {command_value}")
            try:
                subprocess.run(command_value, shell=True)
            except Exception as e:
                print(f"シェルコマンド実行エラー: {e}")
    elif "終了" in command:
        print("プログラムを終了します。")
        root.quit()
    else:
        print("コマンドが認識されませんでした。")

# 音声認識ボタン
tk.Button(root, text="音声認識開始", command=recognize_speech).pack()

# メインループ開始
root.mainloop()
