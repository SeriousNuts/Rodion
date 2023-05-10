import calendar
import os
import random
import string
import time
from datetime import datetime
from pathlib import Path

import matplotlib.pyplot as plt
from docx.shared import Mm
from docxtpl import DocxTemplate, InlineImage
from flask_login import current_user

from app import db_models, db, models
from app.models import ModelTreat

#   каталог для загружаемых файлов
folder_name_in = str(Path(Path.cwd(), 'filestorage'))
#   каталог для скачиваемых файлов
folder_name_out = str(Path(Path.cwd(), 'filestorageOUT'))


def handle_values_R_nadezh(values):
    threat_models = {}
    count = 1
    # print('value handle : ', values)
    for v in values:
        model = ModelTreat()
        model.consruct_from_dir(v)
        key = str(count)
        threat_models.update({key + " элем.": model.r_nadezh()})
        count = count + 1
    # print('threat_models', threat_models)
    threat_models.update({'За все действия': sum(threat_models.values())})
    return threat_models


def handle_values_R_integral(values_risks, value_without_risks):
    threat_models = {}
    threat_models.update({'R интегр': models.r_integral(values_risks["За все действия"],
                                                        value_without_risks["За все действия"])})
    return threat_models


def graph_maker(handled_values_r_nad, handled_values_r_risks):
    r_nad_name = ''.join(random.choices(string.ascii_lowercase, k=7)) + 'r_nad.png'
    r_nad_graph = plt.figure()
    plt.bar(handled_values_r_nad.keys(), handled_values_r_nad.values())
    r_nad_graph.savefig(str(Path(Path.cwd(), 'filestorage', r_nad_name)), dpi=100)

    r_risk_name = ''.join(random.choices(string.ascii_lowercase, k=7)) + 'r_risk.png'
    r_risk_graph = plt.figure()

    plt.bar(handled_values_r_risks.keys(), handled_values_r_risks.values())
    r_risk_graph.savefig(str(Path(Path.cwd(), 'filestorage', r_risk_name)), dpi=100)

    return {'r_nad': r_nad_name, 'r_risk': r_risk_name}


def document_maker(r_risk, r_int, r_nad, graphs):
    folder_in_nad = str(Path(Path.cwd(), 'filestorage', graphs['r_nad']))
    folder_in_risk = str(Path(Path.cwd(), 'filestorage', graphs['r_risk']))

    report = DocxTemplate(str(Path(Path.cwd(), 'app', 'template.docx')))
    r_nad_graph = InlineImage(report, image_descriptor=folder_in_nad, width=Mm(150), height=Mm(100))
    r_risk_graph = InlineImage(report, image_descriptor=folder_in_risk, width=Mm(150), height=Mm(100))

    context = {'r_risk': r_risk, 'r_int': r_int['R интегр'], 'r_nad': r_nad,
               'r_nad_graph': r_nad_graph, 'r_risk_graph': r_risk_graph,
               'r_nad_last': r_nad["За все действия"], 'r_risk_last': r_risk["За все действия"]}
    report.render(context)
    report_name = ''.join(random.choices(string.ascii_lowercase, k=8)) + '_report.docx'
    report.save(str(Path(Path.cwd(), 'filestorage', report_name)))

    return report_name


#   сохраняем отчёт в БД
def save_report(filename):
    timestamp = calendar.timegm(time.gmtime())
    with open(str(Path(folder_name_in, filename)), 'rb') as file:
        # записываем в формат blob
        blob_file = file.read()
    try:
        f = db_models.Report(name=filename,
                             desc='потом будем его формировать',
                             owner=current_user.name,
                             date=datetime.fromtimestamp(timestamp),
                             file=blob_file
                             )
        db.session.add(f)
        db.session.commit()
        print('файл ' + filename + ' сохранён успешно')
    except Exception as e:
        print(e)
        db.session.rollback()
    finally:
        db.session.close()
        os.remove(str(Path(folder_name_in, filename)))


def readreport(data, filename):
    with open(str(Path(folder_name_out, filename)), 'wb') as file:
        file.write(data)
    return folder_name_out
