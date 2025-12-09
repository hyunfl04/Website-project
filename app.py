from flask import Flask, render_template, request, jsonify
import json
import os

app = Flask(__name__)
DATA_FILE = 'data.json'

def load_data():
    if not os.path.exists(DATA_FILE):
        # Dữ liệu mẫu ban đầu (Cập nhật để có nhiều ảnh)
        initial_data = {
            "cars": [
                {
                    "id": "c_porsche_911", 
                    "brand": "Porsche",
                    "name": "911 GT3 RS", 
                    "price": 223800, 
                    "description": "Road-legal motorsport technology. The quintessential sports car.", 
                    # LƯU Ý: Giờ là một danh sách các link ảnh (imageUrls)
                    "imageUrls": [
                        "https://files.porsche.com/filestore/image/multimedia/none/992-gt3-rs-modelimage-sideshot/model/cfbb8ed3-1a15-11ed-80f5-005056bbdc38/porsche-model.png",
                        "https://newsroom.porsche.com/.imaging/mte/porsche-newsroom/image_original/dam/pnr/2022/Products_NP/911-GT3-RS/gallery/P22_0436_a4_rgb.jpg/jcr:content/P22_0436_a4_rgb.jpg",
                        "https://newsroom.porsche.com/.imaging/mte/porsche-newsroom/image_original/dam/pnr/2022/Products_NP/911-GT3-RS/gallery/P22_0439_a4_rgb.jpg/jcr:content/P22_0439_a4_rgb.jpg",
                        "https://newsroom.porsche.com/.imaging/mte/porsche-newsroom/image_original/dam/pnr/2022/Products_NP/911-GT3-RS/gallery/P22_0442_a4_rgb.jpg/jcr:content/P22_0442_a4_rgb.jpg"
                    ],
                    "specs": {"accel": "3.2s", "power": "518 HP", "speed": "296 km/h"} 
                }
            ],
            "users": []
        }
        save_data(initial_data)
        return initial_data
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

@app.route('/')
def index(): return render_template('index.html')

@app.route('/api/cars', methods=['GET'])
def get_cars(): return jsonify(load_data()['cars'])

@app.route('/api/add-car', methods=['POST'])
def add_car():
    new_car = request.json
    data = load_data()
    # Thêm xe mới vào đầu danh sách
    data['cars'].insert(0, new_car)
    save_data(data)
    return jsonify({"message": "Car added!", "car": new_car})

@app.route('/api/auth', methods=['POST'])
def auth():
    req = request.json
    mode, u, p = req.get('mode'), req.get('username'), req.get('password')
    data = load_data()
    users = data.get('users', [])
    if mode == 'register':
        if any(x['username'] == u for x in users): return jsonify({"success": False, "message": "Existed!"})
        users.append({"username": u, "password": p})
        data['users'] = users; save_data(data)
        return jsonify({"success": True})
    elif mode == 'login':
        if any(x['username'] == u and x['password'] == p for x in users): return jsonify({"success": True})
        return jsonify({"success": False, "message": "Fail!"})

if __name__ == '__main__': app.run(debug=True)