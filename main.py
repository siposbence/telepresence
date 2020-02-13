from flask import Flask, render_template, Response, request
#from camera import VideoCamera
import cv2
x = None
y = None

class VideoCamera(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0)

    
    def __del__(self):
        self.video.release()
    
    def get_frame(self):
        global x,y
        success, image = self.video.read()

        if x!=None or y!=None:
            image = cv2.circle(image, (x-8, y-8), 10, (0, 0, 255), -1)
        ret, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()
		
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

#@app.route('/test', methods=['POST'])
#def test():
#    data = request.data
#    print(data)
#    #return jsonify(data)


def gen(VideoCamera):
    while True:
        frame = VideoCamera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/json-pos', methods=['POST']) 
def json_example():
    req_data = request.get_json()
    print(req_data)
    global x, y
    x = req_data['x']
    y = req_data['y']
    #print(req_data['x'], req_data['y'])
    return 'Todo...'

@app.route('/video_feed')
def video_feed():
    return Response(gen(VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
