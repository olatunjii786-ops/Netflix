from flask import Flask, jsonify, request
import os

app = Flask(__name__)
COUNTER_FILE = "user_count.txt"

def get_next_id():
    # Check if the file exists to keep the count consistent
    if not os.path.exists(COUNTER_FILE):
        count = 0
    else:
        with open(COUNTER_FILE, "r") as f:
            count = int(f.read().strip())
    
    count += 1
    
    # Save the new total count back to the file
    with open(COUNTER_FILE, "w") as f:
        f.write(str(count))
    
    return "{:02d}".format(count)

@app.route('/register')
def register():
    # 'request.args.get' captures ANY name the user sent from the app
    user_name = request.args.get('name', 'user') 
    new_id = get_next_id()
    
    print(f"New Registration: {user_name} assigned ID {new_id}")
    
    # We return just the number; the Android app combines Name + Number
    return new_id

@app.route('/movies')
def movies():
    return jsonify([
        {"name": "Avatar", "url": "https://example.com/vid1.mp4"},
        {"name": "Inception", "url": "https://example.com/vid2.mp4"}
    ])

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
