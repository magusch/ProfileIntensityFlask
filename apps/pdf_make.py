from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.utils import ImageReader

import matplotlib.pyplot as plt

import matplotlib
matplotlib.use('agg')

def plot_graph(info, upload_folder):
    plt.clf()
    plt.plot(range(len(info['Y'])), info['Y'])
    plt.ylabel('Intensity')
    plt.xlabel('Pixels')
    plt.savefig(upload_folder+info['name'])
    return info['name']+'.png'

class MakeReport():
    def __init__(self, name, informations, root_folder):
        self.path = root_folder
        self.filename = name+'.pdf'
        self.filepath = '/uploads/reports/'
        c = canvas.Canvas(self.path + self.filepath + name+'.pdf', pagesize=A4)

        for info in informations:
            pdfmetrics.registerFont(TTFont('FreeSans', self.path + '/static/FreeSans.ttf'))
            c.setFont('FreeSans', 14)
            self.head(c)
            self.footer(c)
            self.general(c, info)

            c.showPage()
        c.save()

    def return_filename(self):
        return self.filepath, self.filename


    def head(self, c):
        c.drawString(170, 800, "Измерительный прибор «Хемилюминометр»")

    def footer(self, c):
        image = ImageReader(self.path+'/static/image/itmo_logo.png')
        c.drawImage(image, 150, 25, 100, 50)
        c.drawString(250, 50, "Физика Наноструктур")

    def general(self, c, info):
        upload_folder = self.path + '/uploads/'
        image = ImageReader(upload_folder + info['image'])
        height, width = image.getSize()
        correlation = width/height
        c.drawImage(image, 160, 80, 300, 300*correlation)

        plot_image = plot_graph(info, upload_folder)
        image = ImageReader(upload_folder + plot_image)
        height, width = image.getSize()
        correlation = width / height
        c.drawImage(image, 160, 305, 300, 300 * correlation)

        c.drawString(200, 770, info['name'])
        if info['I1_I0']==True:
            answer = 'Ответ положительный'
        else:
            answer = 'Ответ отрицательный'
        c.drawString(200, 720, answer)





