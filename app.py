import streamlit as st
import csv
import os
from datetime import datetime, date

# CSV 保存先（Streamlit Cloud 永続フォルダ）
FILE_NAME = "/mnt/data/log.csv"

# フォルダがなければ作る（ここが重要）
os.makedirs(os.path.dirname(FILE_NAME), exist_ok=True)

# CSV読み込み
def load_logs():
    if not os.path.exists(FILE_NAME):
        return []
    with open(FILE_NAME, "r", encoding="utf-8") as f:
        return list(csv.reader(f))

# 今日・端末名で既に入力済みか確認
def already_input(device_name):
    today = date.today().strftime("%Y-%m-%d")
    for r in load_logs():
        if r[0] == today and r[1] == device_name:
            return True
    return False

# 保存
def save_log(device_name, status):
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    rows = load_logs()
    new_rows = []
    found = False
    for r in rows:
        if r[0] == date.today().strftime("%Y-%m-%d") and r[1] == device_name:
            new_rows.append([r[0], r[1], status, now])
            found = True
        else:
            new_rows.append(r)
    if not found:
        new_rows.append([date.today().strftime("%Y-%m-%d"), device_name, status, now])
    with open(FILE_NAME, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerows(new_rows)

# Streamlit画面
st.title("生活見守りアプリ（複数端末対応）")

device_name = st.text_input("端末名（または名前）を入力してください")

if device_name:
    if already_input(device_name):
        st.warning(f"{device_name} は今日はすでに入力済みです。")
    else:
        col1, col2, col3 = st.columns(3)

        if col1.button("元気"):
            save_log(device_name, "元気")
            st.success(f"{device_name} の記録「元気」を保存しました")

        if col2.button("普通"):
            save_log(device_name, "普通")
            st.success(f"{device_name} の記録「普通」を保存しました")

        if col3.button("不調"):
            save_log(device_name, "不調")
            st.success(f"{device_name} の記録「不調」を保存しました")

# 今日の入力一覧を確認（任意）
if st.checkbox("今日の全端末の入力を確認する"):
    today_str = date.today().strftime("%Y-%m-%d")
    logs = [r for r in load_logs() if r[0] == today_str]
    if logs:
        st.table(logs)
    else:
        st.info("今日の入力はまだありません")

