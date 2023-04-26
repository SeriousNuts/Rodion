import os
import random

from flask_login import current_user
from openpyxl import Workbook
from openpyxl.chart import BarChart, Reference
from app import models, db_models, db
import calendar
import time
from datetime import datetime

from app.models import ModelTreat
import string

#   каталог для загружаемых файлов
folder_name_in = os.getcwd() + '\\app\\filestorage\\'
#   каталог для скачиваемых файлов
folder_name_out = os.getcwd() + '\\app\\filestorageOUT\\'


def handle_values(values):
    threat_models = []
    count = 0
    print('value handle : ', values)
    for v in values:
        model = ModelTreat()
        model.consruct_from_dir(v)
        threat_models.append({count: model.r_nadezh()})
        count = count + 1
    print('threat_models', threat_models)
    return threat_models


def excelmaker(handled_values):

    wb = Workbook()
    ws = wb.active
    #   добавляем записи в таблицу excel
    somelist = []
    for dict_values in handled_values:
        for value in dict_values:
            somelist.append(value)
            somelist.append(dict_values[value])
        #somelist = [v, handled_values[v]]
        ws.append(somelist)
    #   инициализиуем график
    chart = BarChart()
    #   Инициализируем оси графика
    chart.y_axis.title = 'model'
    chart.x_axis.title = 'Index'
    # сообщаем графику на основе каких значений строиться
    exc_value = Reference(worksheet=ws, min_row=1, max_row=6, min_col=1, max_col=2)
    #   добавляем график в excel
    chart.add_data(exc_value, titles_from_data=False)
    #   добавляем названия столбцам графика
    categor = Reference(worksheet=ws, min_col=1, min_row=1, max_row=6)
    chart.set_categories(categor)
    #   добавляем график в лист excel
    ws.add_chart(chart, 'A10')
    #   генерируем уникальное имя файла
    report_name = ''.join(random.choices(string.ascii_lowercase, k=8)) + '_report.xlsx'
    # сохраняем отчёт в память
    wb.save(folder_name_in + report_name)
    print(folder_name_in + report_name, '  : is saved')
    return report_name


#   сохраняем отчёт в БД
def savereport(filename):
    timestamp = calendar.timegm(time.gmtime())
    with open(folder_name_in + filename, 'rb') as file:
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
        os.remove(folder_name_in + filename)


def readreport(data, filename):
    with open(folder_name_out + filename, 'wb') as file:
        file.write(data)
    return folder_name_out
