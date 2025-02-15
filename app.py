import speech_recognition as sr
import pyautogui
import os
import keyboard

# 音声を認識してテキストに変換
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

# コマンドに基づいて操作を実行
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
        return "終了"
    else:
        print("コマンドが認識されませんでした。")
    return None

# メインループ
if __name__ == "__main__":
    while True:
        command = recognize_speech()
        if command:
            result = execute_command(command)
            if result == "終了":
                break
