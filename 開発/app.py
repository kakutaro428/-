from flask import Flask, render_template, request, jsonify

import json
import os

DATA_FILE = 'anime_list.json'

# アニメリストをファイルから読み込む
def load_anime_list():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

# アニメリストをファイルに保存する
def save_anime_list():
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(anime_list, f, ensure_ascii=False, indent=4)

anime_list = load_anime_list()

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/add', methods=['POST'])
def add_anime():
    data = request.get_json()
    title = data.get('title')
    genre = data.get('genre')
    
    if title and genre:
        anime = {'title': title, 'genre': genre}
        anime_list.append(anime)
        save_anime_list()  # 追加後にファイルに保存
        return jsonify(anime)
    return jsonify({'error': 'Invalid input'}), 400

@app.route('/anime')
def get_anime_list():
    return jsonify(anime_list)  # 現在のアニメリストを返す

# アニメを削除する機能
@app.route('/delete', methods=['POST'])
def delete_anime():
    data = request.get_json()
    title = data.get('title')
    
    if title:
        global anime_list
        anime_list = [anime for anime in anime_list if anime['title'] != title]
        save_anime_list()  # 削除後にファイルに保存
        return jsonify({'message': f"'{title}' has been deleted."})
    return jsonify({'error': 'Invalid input or title not found'}), 400

if __name__ == "__main__":
    app.run(port=8080)

