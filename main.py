from flask import Flask, request, jsonify, send_from_directory
import db
app = Flask(__name__)

url = "https://aldermann.serveo.net"

@app.route('/hook')
def hook():
    data = {
        "data": {
            "metadata": {
                "app_name": "EatUp",
                "app_id": 123804,
                "title": "Đăng ký đi ăn",
                "submit_button": {
                    "label": "Gửi",
                    "background_color": "#6666ff",
                    "cta": "request",
                    "url": "{}/submit".format(url),
                },
                "elements": [
                    {
                        "type": "text",
                        "style": "heading",
                        "content": "Đi ăn chia tay anh Hà",
                    },
                    {
                        "type": "text",
                        "style": "paragraph",
                        "content": "Tại nhà hàng Minh Mường.\nĐịa chỉ 32 Hoàng Cầu, Ô Chợ Dừa, Đống Đa\nThời gian: 19h tối thứ 4 ngày 12/9"
                    },
                    {
                        "type": "text",
                        "style": "paragraph",
                        "content": ""
                    },
                    {
                        "type": "web",
                        "content": '<div style= "text-align: center"><img style="width: 100%" src="{}/map_image" alt="map"/></div>'.format(url),
                    },
                    {
                        "type": "input",
                        "input_type": "text",
                        "required": True,
                        "label": "Tên người tham gia",
                        "placeholder": "Nguyễn Văn A",
                        "name": "name",
                        "error": "Hãy nhập tên của mình",
                    },
                    {
                        "type": "radio",
                        "display_type": "inline",
                        "required": True,
                        "label": "Tham gia?",
                        "name": "agreement",
                        "error": "Chọn một trong hai lựa chọn đi",
                        "options": [
                            {
                                "label": "Có",
                                "value": "yes",
                            },
                            {
                                "label": "Không",
                                "value": "no",
                            },
                        ],
                    },
                ],
            },
        },
    };

    return jsonify(data)

@app.route("/map_image")
def map():
    return send_from_directory(".", "map.png")

@app.route('/submit', methods=["POST"])
def submit():

    user_id = request.headers["User-Id"]
    name = request.json["name"]
    agreement = request.json["agreement"]
    db.update(user_id, name, agreement)

    participants = db.participant_list()
    elements = [{
        "type": "text",
        "style": "heading",
        "content": "Danh sách người tham gia",
    }]
    cnt = 0
    for p in participants:
        cnt += 1
        elements.append({"type": "text", "style": "paragraph", "content": str(cnt) + ": " + p["name"]})
    data = {
        "data": {
            "metadata": {
                "app_name": "EatUp",
                "app_id": 123804,
                "title": "Thanks",
                "submit_button": {
                    "label": "Mở bản đồ",
                    "background_color": "#6666ff",
                    "cta": "url",
                    "url": "https://www.google.com/maps/place/Nh%C3%A0+H%C3%A0ng+Minh+M%C6%B0%E1%BB%9Dng/@21.0169767,105.8196396,16.69z/data=!4m5!3m4!1s0x0:0xf41fca1eec2f12d9!8m2!3d21.0163358!4d105.8220676"
                },
                "elements": elements,
            },
        },
    };
    return jsonify(data)

@app.route("/list")
def list():
    participants = db.participant_list()
    res = "<html><body><h1>Danh sách người tham gia</h1><ol>";
    for p in participants:
        res += f"<h3><li>{p['name']}</li></h3>"
    res +="</ol></body></html>"
    return res

app.run(port=3000)
