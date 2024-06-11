import os
import csv
import random
from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with your actual secret key
IMAGES_FOLDER = 'static/images'

categories = {
    'quality': ['poor', 'fair', 'excellent'],
    'ethnicity': ['asian', 'caucasian', 'black', 'unintelligible'],
    'gender': ['feminine', 'neutral', 'masculine', 'unintelligible']
}

def load_images(user_id):
    user_folder = os.path.join('experiment', 'sample', user_id)
    images_file = os.path.join(user_folder, 'images.txt')

    if os.path.exists(images_file):
        with open(images_file, 'r') as f:
            images = [line.strip() for line in f]
    else:
        images = os.listdir(IMAGES_FOLDER)
        random.shuffle(images)
        with open(images_file, 'w') as f:
            for image in images:
                f.write(image + '\n')

    return images

def save_progress(user_id, index):
    progress_file = os.path.join('experiment', 'sample', user_id, 'progress.txt')
    with open(progress_file, 'w') as f:
        f.write(str(index))

def load_progress(user_id):
    progress_file = os.path.join('experiment', 'sample', user_id, 'progress.txt')
    if os.path.exists(progress_file):
        with open(progress_file, 'r') as f:
            return int(f.read())
    return 0

def save_labels(user_id, data):
    user_folder = os.path.join('experiment', 'sample', user_id)
    os.makedirs(user_folder, exist_ok=True)
    csv_file = os.path.join(user_folder, 'image_labels.csv')
    file_exists = os.path.isfile(csv_file)
    with open(csv_file, 'a', newline='') as csvfile:
        fieldnames = ['image', 'quality', 'ethnicity', 'gender']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()
        writer.writerow(data)

@app.route('/', methods=['GET', 'POST'])
def index():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user_id = session['user_id']
    
    if 'images' not in session:
        session['images'] = load_images(user_id)
        session['index'] = load_progress(user_id)
    
    images = session['images']
    index = session['index']

    if request.method == 'POST':
        if 'next' in request.form:
            quality = request.form.get('quality')
            ethnicity = request.form.get('ethnicity')
            gender = request.form.get('gender')
            image = images[index]
            save_labels(user_id, {'image': image, 'quality': quality, 'ethnicity': ethnicity, 'gender': gender})
            index += 1
            session['index'] = index
            save_progress(user_id, index)
            if index >= len(images):
                return redirect(url_for('complete'))

    if index < len(images):
        current_image = images[index]
        return render_template('index.html', image=current_image, categories=categories)
    else:
        return redirect(url_for('complete'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user_id = request.form.get('user_id')
        user_folder = os.path.join('experiment', 'sample', user_id)
        os.makedirs(user_folder, exist_ok=True)
        session['user_id'] = user_id
        return redirect(url_for('index'))
    return render_template('login.html')

@app.route('/complete')
def complete():
    return "All images have been categorized!"

if __name__ == '__main__':
    app.run(debug=True)


# import os
# import csv
# import random
# from flask import Flask, render_template, request, redirect, url_for, session

# app = Flask(__name__)
# app.secret_key = 'your_secret_key'  # Replace with your actual secret key
# IMAGES_FOLDER = 'static/images'

# categories = {
#     'quality': ['poor', 'fair', 'excellent'],
#     'ethnicity': ['asian', 'caucasian', 'black', 'unintelligible'],
#     'gender': ['feminine', 'neutral', 'masculine', 'unintelligible']
# }

# def load_images(user_id):
#     user_folder = os.path.join('experiment', 'sample', user_id)
#     images_file = os.path.join(user_folder, 'images.txt')

#     if os.path.exists(images_file):
#         with open(images_file, 'r') as f:
#             images = [line.strip() for line in f]
#     else:
#         images = os.listdir(IMAGES_FOLDER)
#         random.shuffle(images)
#         with open(images_file, 'w') as f:
#             for image in images:
#                 f.write(image + '\n')

#     return images

# def save_progress(user_id, index):
#     progress_file = os.path.join('experiment', 'sample', user_id, 'progress.txt')
#     with open(progress_file, 'w') as f:
#         f.write(str(index))

# def load_progress(user_id):
#     progress_file = os.path.join('experiment', 'sample', user_id, 'progress.txt')
#     if os.path.exists(progress_file):
#         with open(progress_file, 'r') as f:
#             return int(f.read())
#     return 0

# def save_labels(user_id, data):
#     user_folder = os.path.join('experiment', 'sample', user_id)
#     os.makedirs(user_folder, exist_ok=True)
#     csv_file = os.path.join(user_folder, 'image_labels.csv')
#     file_exists = os.path.isfile(csv_file)
#     with open(csv_file, 'a', newline='') as csvfile:
#         fieldnames = ['image', 'quality', 'ethnicity', 'gender']
#         writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
#         if not file_exists:
#             writer.writeheader()
#         writer.writerow(data)

# @app.route('/', methods=['GET', 'POST'])
# def index():
#     if 'user_id' not in session:
#         return redirect(url_for('login'))
    
#     user_id = session['user_id']
    
#     if 'images' not in session:
#         session['images'] = load_images(user_id)
#         session['index'] = load_progress(user_id)
    
#     images = session['images']
#     index = session['index']

#     if request.method == 'POST':
#         if 'next' in request.form:
#             quality = request.form.get('quality')
#             ethnicity = request.form.get('ethnicity')
#             gender = request.form.get('gender')
#             image = images[index]
#             if quality == 'intelligible' or ethnicity == 'intelligible' or gender == 'intelligible':
#                 save_labels(user_id, {'image': image, 'quality': 'NaN', 'ethnicity': 'NaN', 'gender': 'NaN'})
#             else:
#                 save_labels(user_id, {'image': image, 'quality': quality, 'ethnicity': ethnicity, 'gender': gender})
#             index += 1
#             session['index'] = index
#             save_progress(user_id, index)
#             if index >= len(images):
#                 return redirect(url_for('complete'))

#     if index < len(images):
#         current_image = images[index]
#         return render_template('index.html', image=current_image, categories=categories)
#     else:
#         return redirect(url_for('complete'))

# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         user_id = request.form.get('user_id')
#         user_folder = os.path.join('experiment', 'sample', user_id)
#         os.makedirs(user_folder, exist_ok=True)
#         session['user_id'] = user_id
#         return redirect(url_for('index'))
#     return render_template('login.html')

# @app.route('/complete')
# def complete():
#     return "All images have been categorized!"

# if __name__ == '__main__':
#     app.run(debug=True)
