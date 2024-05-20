from flask import Flask, request, jsonify, send_file
import cv2 as cv
import matplotlib.pyplot as plt
import numpy as np
import os
from flask_cors import CORS
app = Flask(__name__)
CORS(app, origins=["*"])


plt.figure()
plt.title('Colour Histogram')
plt.xlabel('Bins')
plt.ylabel('# of pixels')
colors = ('r','g','b')



hist_data = []
color_count_array_r = []
color_count_array_g = []
color_count_array_b = []
res = ''
# max_number_r, max_number_g, max_number_b =[]
bin_Data = []
def Check_image(file):
    img = cv.imread(f'./{file}')
    
    blank = np.zeros(img.shape[:2], dtype='uint8')
    mask = cv.circle(blank, (img.shape[1]//2,img.shape[0]//2), 100, 255, -1)
    for i, col in enumerate(colors):
            hist = cv.calcHist([img], [i], mask, [256], [0, 256])
            hist_data.append(hist)
        # print(hist_data)
        
    for i, col in enumerate(colors):
        for bin_value, count in enumerate(hist_data[i]):
            if col == 'r':
                color_count_array_r.append(count[0])
            elif col == 'g':
                color_count_array_g.append(count[0])
            elif col == 'b':
                color_count_array_b.append(count[0])
            bin_Data.append(bin_value)

    if max(color_count_array_r)  > max(color_count_array_b) and max(color_count_array_g) > max(color_count_array_b):
        res = "Analizlərimizə əsasən, təbriklər sizdə şüphəli hal görmədik"
    elif max(color_count_array_r)  < max(color_count_array_b) and max(color_count_array_g) < max(color_count_array_b):
        res = "Analizlərimizə əsasən, sizin anemiya olma ehtimalınız var"

    return res
    for i,col in enumerate(colors):
            hist = cv.calcHist([img], [i], mask, [256], [0,256])
    plt.plot(hist, color=col)
    plt.xlim([0,256])

@app.route("/")
def hello_world():
    return "Hello, World!"


UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/process', methods=['POST'])
def process_image():
    try:
        if 'file' not in request.files:
            print(request.files)
            return jsonify({"error": "No file part"})

        file = request.files['file']
        if file.filename == '':
            return jsonify({"error": "No selected file"})
    
        if file:
            filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            print(filename)
            print(file)
            file.save(filename)
            res = Check_image(filename)
            os.remove(f'./{file}')
        return res

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)




