import os,json, csv

from flask import Flask, render_template, request,send_file, url_for, redirect, session, send_from_directory
from flask_dropzone import Dropzone
from werkzeug.utils import secure_filename

from apps.image_an import line_intensity

from apps.forms import UploadForm, DownloadFile

from apps import pdf_make


app = Flask(__name__, static_folder="static")


dropzone = Dropzone(app)

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))

app.config.update(
    UPLOAD_FOLDER=os.path.join(PROJECT_ROOT, 'uploads'),
    UPLOAD_EXTENSIONS = ['.jpg', 'jpeg', '.png', '.gif'],
    STATIC_FOLDER = 'static/',
    STATICFILES_DIRS = (os.path.join(PROJECT_ROOT, "static")),
)

# UPLOAD_FOLDER = os.path.join(basedir, 'uploads')
ALLOWED_EXTENSIONS = ['png', 'jpg', 'jpeg', 'gif']
# #app.config['UPLOAD_EXTENSIONS'] = ['.jpg', 'jpeg', '.png', '.gif']
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# app.config['STATIC_FOLDER'] = 'static/'
#
# app.config['STATICFILES_DIRS'] = (os.path.join(PROJECT_ROOT, "static"))


app.secret_key = b'_5#fwwdss"F4Q8z\n\xec]/'


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/index', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        f = request.files.get('file')
        path = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(f.filename))
        f.save(path)
        # if session.get('filename'):
        #     try:
        #         os.remove(session.get('filename'))
        #     except:
        #         pass
        session['filename'] = path

    return render_template('index.html')

@app.route('/', methods=['GET', 'POST'])
def index_forms():
    forms = [UploadForm(prefix="form%s" %(i)) for i in range(5)]

    if request.method == 'POST':
        session['datas'] =[]
        for form in forms:
            samplename = form.data['samplename']
            f = form.data['filename']
            if (not f) or (not allowed_file(f.filename)): continue
            #if not allowed_file(f.filename): continue
            filename = secure_filename(f.filename)

            path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            f.save(path)
            session['datas'].append({'filename':path, 'samplename':samplename})
        return redirect(url_for('completed'))

    return render_template('index_upload.html', forms=forms)


@app.route('/completed')
def completed():
    #file = session.get('filename')
    datas = session.get('datas')
    if datas:
        form = DownloadFile()
        intensities = {}
        pixels = {}
        filenames = {}
        I1_I0 = {}
        for data in datas:
            samplename = data['samplename']
            file = data['filename']
            Y, I1_I0[samplename] = line_intensity(file)
            intensities[samplename] = list(Y)
            filenames[samplename] = file.split('/')[-1]
            X = (list(range(len(Y))))
            save_csv(X, intensities)
            #filename = 'static/uploads/' + file.split('/')[-1] #change
            #os.path.join(app.config['UPLOADED_PATH'], secure_filename(file))
        return render_template('output.html', X=X, Y=intensities, I1_I0=I1_I0, form=form, filenames=filenames)
    else:
        return redirect (url_for('index_forms'))


@app.route('/description', methods=['GET', 'POST'])
def description():
    return render_template('description.html')


@app.route('/instruction', methods=['GET', 'POST'])
def instruction():
    return render_template('instruction.html')

def get_information(info_post):
    Y = ((json.loads(info_post['Y_values'].replace("'", "\""))))
    filenames = ((json.loads(info_post['filenames'].replace("'", "\""))))
    limit = float(info_post['limit'])
    X = ((json.loads(info_post['X_values'].replace("'", "\""))))
    I1_I0 = ((json.loads(info_post['I1_I0'].replace("'", "\""))))

    informations = []
    for label, intensity in Y.items():
        # if I1_I0[label]>limit:
        #     I1_I0_answer = True
        # else:
        #     I1_I0_answer = False
        informations.append(
            {
                'image': filenames[label], 'name': label, 'X': X, 'Y': intensity, 'I1_I0': I1_I0[label]
             }
        )
    return informations, limit

def save_csv(X,intensities):
    path_to_files = {}
    for filename, Y in intensities.items():
        path_to_file = f"{app.config['UPLOAD_FOLDER']}/reports/{filename}.csv"
        with open(path_to_file, 'w') as f:
            wr = csv.writer(f)
            Q=[(X[i], Y[i]) for i in range(len(X))]
            wr.writerows(Q)
        #path_to_files['filename']=path_to_file

@app.route('/uploads/<filename>')
def upload_csv(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], f"reports/{filename}.csv")

@app.route('/report', methods=['POST'])
def get_pdf():
    info_post = request.values

    informations, limit = get_information(info_post)
    filename = '_'.join(q['name'] for q in informations)

    f = pdf_make.MakeReport(filename, informations,limit, PROJECT_ROOT)
    directory, filename = f.return_filename()
    return send_from_directory(PROJECT_ROOT+directory, filename)

if __name__ == '__main__':
    app.run(debug=True)