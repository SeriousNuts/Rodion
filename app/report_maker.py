import os
import random

import openpyxl
from flask_login import current_user
from openpyxl import Workbook
from openpyxl.chart import BarChart, Reference
from app import models, db_models, db
import calendar
import time
from datetime import datetime
from pathlib import Path
from app.models import ModelTreat
import string
import matplotlib.pyplot as plt

#   каталог для загружаемых файлов
folder_name_in = str(Path(Path.cwd(), 'filestorage'))
#   каталог для скачиваемых файлов
folder_name_out = str(Path(Path.cwd(), 'filestorageOUT'))


def handle_values_R_nadezh(values):
    threat_models = []
    count = 0
    # print('value handle : ', values)
    for v in values:
        model = ModelTreat()
        model.consruct_from_dir(v)
        key = "R надёжное эл. : " + str(count)
        threat_models.append({key: model.r_nadezh()})
        count = count + 1
    # print('threat_models', threat_models)
    return threat_models


def handle_values_R_integral(values):
    threat_models = []
    count = 0
    # print('value handle : ', values)
    for v in values:
        model = ModelTreat()
        model.consruct_from_dir(v)
        key = "R интегральное эл. : " + str(count)
        threat_models.append({key: model.r_integral()})
        count = count + 1
    # print('threat_models', threat_models)
    return threat_models


def excelmaker(handled_values_r_nad, graph_place_r_nad, handled_values_r_int, graph_place_r_int):
    wb = Workbook()
    ws = wb.active
    #   добавляем записи в таблицу excel
    r_nad_list = []

    for dict_values in handled_values_r_nad:
        r_nad_some_list = []  # переоходный лист для добавлени эллементов
        for value in dict_values:
            r_nad_some_list.append(value)
            r_nad_some_list.append(dict_values[value])
            r_nad_list.append(r_nad_some_list)

    for row in r_nad_list:
        ws.append(row)
    #   инициализиуем график
    chart = BarChart()
    #   Инициализируем оси графика
    chart.y_axis.title = 'R_nadezhnoe'
    chart.x_axis.title = 'model'
    # сообщаем графику на основе каких значений строиться
    exc_value = Reference(worksheet=ws, min_row=1, max_row=len(r_nad_list), min_col=2, max_col=2)
    #   добавляем график в excel
    chart.add_data(exc_value, titles_from_data=False)
    #   добавляем названия столбцам графика
    categor = Reference(worksheet=ws, min_col=1, min_row=1, max_row=6)
    chart.set_categories(categor)
    #   добавляем график в лист excel
    ws.add_chart(chart, graph_place_r_nad)
    #   добавляем записи в таблицу excel

    r_int_list = []

    for dict_values in handled_values_r_int:
        r_int_some_list = [] # Промежуточный список
        for value in dict_values:
            r_int_some_list.append(value)
            r_int_some_list.append(dict_values[value])
            r_int_list.append(r_int_some_list)

    for row in r_int_list:
        ws.append(row)
    #   инициализиуем график
    chart = BarChart()
    #   Инициализируем оси графика
    chart.y_axis.title = 'R_inegralnoe'
    chart.x_axis.title = 'model'
    # сообщаем графику на основе каких значений строиться
    exc_value = Reference(worksheet=ws, min_row=len(r_nad_list) + 1, max_row=len(r_int_list) + len(r_nad_list), min_col=2, max_col=2)
    #   добавляем график в excel
    chart.add_data(exc_value, titles_from_data=False)
    #   добавляем названия столбцам графика
    categor = Reference(worksheet=ws, min_col=1, min_row=1, max_row=6)
    chart.set_categories(categor)
    #   добавляем график в лист excel
    ws.add_chart(chart, graph_place_r_int)
    #   генерируем уникальное имя файла
    report_name = ''.join(random.choices(string.ascii_lowercase, k=8)) + '_report.xlsx'
    # сохраняем отчёт в память
    wb.save(str(Path(folder_name_in, report_name)))
    print(str(folder_name_in) + report_name, '  : is saved')
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



