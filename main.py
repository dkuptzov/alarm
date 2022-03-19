import pandas


def load_csv():
    # Получаем данные из файла tab3.csv
    try:
        data = pandas.read_csv('tab3.csv')
        data_csv = data.to_dict(orient='records')
    except FileNotFoundError:
        print('File not found!')
    return data_csv


def change_time(data):
    # Исправляем дату
    for i in data:
        i['Метка времени'] = i['Метка времени'].split()[0]
    return data


def new_csv(data):
    # Преобразуем данные из исходной таблицы
    csv_ready = []

    def ring():
        # Если данные содержат звонок
        if len(csv_ready) == 0:
            csv_ready.append({'Абонент': i['id абонента'],
                              'Дата': i['Метка времени'],
                              'Потрачено минут': i['Объем затраченных единиц'],
                              'Потрачено смс': 0,
                              'Потрачено трафика': 0.0
                              })
        else:
            for j in range(len(csv_ready)):
                if csv_ready[j]['Абонент'] == i['id абонента'] and\
                        csv_ready[j]['Дата'] == i['Метка времени']:
                    csv_ready[j]['Потрачено минут'] += i['Объем затраченных единиц']
                    return csv_ready
            csv_ready.append({'Абонент': i['id абонента'],
                              'Дата': i['Метка времени'],
                              'Потрачено минут': i['Объем затраченных единиц'],
                              'Потрачено смс': 0,
                              'Потрачено трафика': 0.0
                              })

    def sms():
        # Если данные содержат смс
        if len(csv_ready) == 0:
            csv_ready.append({'Абонент': i['id абонента'],
                              'Дата': i['Метка времени'],
                              'Потрачено минут': 0,
                              'Потрачено смс': i['Объем затраченных единиц'],
                              'Потрачено трафика': 0.0
                              })
        else:
            for j in range(len(csv_ready)):
                if csv_ready[j]['Абонент'] == i['id абонента'] and \
                        csv_ready[j]['Дата'] == i['Метка времени']:
                    csv_ready[j]['Потрачено смс'] += i['Объем затраченных единиц']
                    return csv_ready
            csv_ready.append({'Абонент': i['id абонента'],
                              'Дата': i['Метка времени'],
                              'Потрачено минут': 0,
                              'Потрачено смс': i['Объем затраченных единиц'],
                              'Потрачено трафика': 0.0
                              })

    def traffic():
        # Если данные содержат интренте трафик
        if len(csv_ready) == 0:
            csv_ready.append({'Абонент': i['id абонента'],
                              'Дата': i['Метка времени'],
                              'Потрачено минут': 0,
                              'Потрачено смс': 0,
                              'Потрачено трафика': i['Объем затраченных единиц']
                              })
        else:
            for j in range(len(csv_ready)):
                if csv_ready[j]['Абонент'] == i['id абонента'] and \
                        csv_ready[j]['Дата'] == i['Метка времени']:
                    csv_ready[j]['Потрачено трафика'] += i['Объем затраченных единиц']
                    return csv_ready
            csv_ready.append({'Абонент': i['id абонента'],
                              'Дата': i['Метка времени'],
                              'Потрачено минут': 0,
                              'Потрачено смс': 0,
                              'Потрачено трафика': i['Объем затраченных единиц']
                              })

    for i in data:
        if i['Тип услуги (звонок смс трафик)'] == 'Звонок':
            ring()
        elif i['Тип услуги (звонок смс трафик)'] == 'смс':
            sms()
        elif i['Тип услуги (звонок смс трафик)'] == 'трафик':
            traffic()
    # Сортировка по абоненту и дате
    csv_ready = sorted(sorted(csv_ready, key=lambda x: x['Дата']), key=lambda z: z['Абонент'])
    data_frame = pandas.DataFrame(csv_ready)
    data_frame.to_csv('result.csv')


if __name__ == '__main__':
    data_from_csv = load_csv()
    data_csv_correct_time = change_time(data_from_csv)
    new_csv(data_csv_correct_time)
