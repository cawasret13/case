import random
from datetime import datetime

from asgiref.sync import sync_to_async

from chat.models import Users, cases
import json
import codecs

from test.settings import url_server
def Case_script(token, id_case):
    case = cases.objects.get(id_case=id_case)
    items_in_case = []
    _money = _loss = 0
    for item in case.items:
        for index in item:
            items_in_case.append(item[index])
    items_in_case = sorted(items_in_case, key=lambda student: student['coef'])
    max_coef = float(items_in_case[::-1][0]['coef']) + 0.01
    for cell in case.history:
        if (cell != {}):
            _money += case.price
            _loss += cell['price']
    print(_money, _loss)
    if case.applayRules == False:
        if not (_money <= _loss):
            subCoef = 0
            items_in_case = sorted(items_in_case, key=lambda student: student['price'])[::-1]
            for item in items_in_case:
                if (_loss + item['price']) <= ((_money * (float(100 - case.coef_profit) / 100)) + case.coef_compensation) and \
                        item['coef'] != 0:
                    subCoef = float(item['coef'])
                    break
            if subCoef == 0:
                subCoef = 0.8
            coef = random.uniform(subCoef, max_coef)
            win_item = None
            items_in_case = sorted(items_in_case, key=lambda student: student['coef'])[::-1]
            for item in items_in_case:
                if coef > float(item['coef']):
                    win_item = item
                    break
            return {'name': win_item['name'], 'id': win_item['id'], 'price': win_item['price'], 'sub': coef,
                    'coef': item['coef']}
        else:
            coef = random.uniform(0.5, max_coef)
            items_in_case = sorted(items_in_case, key=lambda student: student['coef'])[::-1]
            for item in items_in_case:
                if coef > float(item['coef']):
                    win_item = item
                    break
            return {'name': win_item['name'], 'id': win_item['id'], 'price': win_item['price'], 'sub': coef,
                    'coef': item['coef']}
    else:
        rules = sorted(case.rules, key=lambda student: int(student['money']))
        for rule in rules:
            if _money <= int(rule['money']):
                if not (_money <= _loss):
                    subCoef = 0
                    items_in_case = sorted(items_in_case, key=lambda student: student['price'])[::-1]
                    for item in items_in_case:
                        if (_loss + item['price']) <= (
                                (_money * (float(100 - float(rule['coef'])) / 100)) + float(
                            rule['coef_compensation'])) and item['coef'] != 0:
                            subCoef = float(item['coef'])
                            break
                    if subCoef == 0:
                        subCoef = 0.8
                    coef = random.uniform(subCoef, max_coef)
                    print(subCoef, coef, '-------', _money, rule['coef'])
                    win_item = None
                    items_in_case = sorted(items_in_case, key=lambda student: student['coef'])[::-1]
                    for item in items_in_case:
                        if coef > float(item['coef']):
                            win_item = item
                            break
                    return {'name': win_item['name'], 'id': win_item['id'], 'price': win_item['price'], 'sub': coef,
                            'coef': item['coef']}
                else:
                    coef = random.uniform(0.5, max_coef)
                    print(coef, '========', _money)
                    items_in_case = sorted(items_in_case, key=lambda student: student['coef'])[::-1]
                    for item in items_in_case:
                        if coef > float(item['coef']):
                            win_item = item
                            break
                    return {'name': win_item['name'], 'id': win_item['id'], 'price': win_item['price'], 'sub': coef,
                            'coef': item['coef']}

@sync_to_async
def Script_testing(coef_compensation, coef_profit, id_case, history, applay_Rules, rules):
    case = cases.objects.get(id_case=id_case)
    items_in_case = []
    _money = _loss = 0
    for item in case.items:
        for index in item:
            items_in_case.append(item[index])
    items_in_case = sorted(items_in_case, key=lambda student: student['coef'])
    max_coef = float(items_in_case[::-1][0]['coef']) + 0.01
    for cell in history:
        if (cell != {}):
            _money += case.price
            _loss += cell['price']
    if applay_Rules == False:
        if not (_money <= _loss):
            subCoef = 0
            items_in_case = sorted(items_in_case, key=lambda student: student['price'])[::-1]
            for item in items_in_case:
                if (_loss + item['price']) <= ((_money * (float(100 - coef_profit) / 100)) + coef_compensation) and item['coef'] != 0:
                    subCoef = float(item['coef'])
                    break
            if subCoef == 0:
                subCoef = 0.8
            coef = random.uniform(subCoef, max_coef)
            win_item = None
            items_in_case = sorted(items_in_case, key=lambda student: student['coef'])[::-1]
            for item in items_in_case:
                if coef > float(item['coef']):
                    win_item = item
                    break
            return {'name': win_item['name'], 'id':win_item['id'], 'price':win_item['price'], 'sub':coef, 'coef':item['coef']}
        else:
            coef = random.uniform(0.5, max_coef)
            items_in_case = sorted(items_in_case, key=lambda student: student['coef'])[::-1]
            for item in items_in_case:
                if coef > float(item['coef']):
                    win_item = item
                    break
            return {'name': win_item['name'], 'id':win_item['id'], 'price':win_item['price'], 'sub':coef, 'coef':item['coef']}
    else:
        rules = sorted(rules, key=lambda student: int(student['money']))
        for rule in rules:
            if _money <= int(rule['money']):
                if not (_money <= _loss):
                    subCoef = 0
                    items_in_case = sorted(items_in_case, key=lambda student: student['price'])[::-1]
                    for item in items_in_case:
                        if (_loss + item['price']) <= (
                                (_money * (float(100 - float(rule['coef'])) / 100)) + float(rule['coef_compensation'])) and item['coef'] != 0:
                            subCoef = float(item['coef'])
                            break
                    if subCoef == 0:
                        subCoef = 0.8
                    coef = random.uniform(subCoef, max_coef)
                    print(subCoef, coef, '-------',_money, rule['coef'])
                    win_item = None
                    items_in_case = sorted(items_in_case, key=lambda student: student['coef'])[::-1]
                    for item in items_in_case:
                        if coef > float(item['coef']):
                            win_item = item
                            break
                    return {'name': win_item['name'], 'id': win_item['id'], 'price': win_item['price'], 'sub': coef,
                            'coef': item['coef']}
                else:
                    coef = random.uniform(0.5, max_coef)
                    print(coef, '========',_money)
                    items_in_case = sorted(items_in_case, key=lambda student: student['coef'])[::-1]
                    for item in items_in_case:
                        if coef > float(item['coef']):
                            win_item = item
                            break
                    return {'name': win_item['name'], 'id': win_item['id'], 'price': win_item['price'], 'sub': coef,
                            'coef': item['coef']}

