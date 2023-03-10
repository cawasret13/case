import random
from datetime import datetime
from chat.models import Users, cases
import json
import codecs

from test.settings import url_server
def Case_script(token, id_case):
    with open('static/settings.json') as file:
        settings = json.load(file)[0]
    f = codecs.open('static/log.txt', 'a', "utf-8")
    gr = codecs.open('static/grath.txt', 'a', "utf-8")
    # user = Users.objects.get(token=token)
    case = cases.objects.get(id_case=id_case)
    items_in_case = []
    history = case.history
    date = datetime.now().date()
    _money = _loss = 0
    loss = True
    for item in case.items:
        for index in item:
            items_in_case.append(item[index])
    items_in_case = sorted(items_in_case, key=lambda student: student['coef'])
    max_coef = float(items_in_case[::-1][0]['coef'])
    for cell in history:
        if(cell!={}):
            if json.loads(cell['date']) == str(date):
                _money += case.price
                _loss += cell['price']
    print(f'-------{_loss}, {_money} === {_money-_loss}')
    f.write(f'-------{_loss}, {_money} === {_money-_loss}\n')
    if _loss < _money:
        loss = False
    print('-------',loss)
    if _money!=_loss:
        print('-------%',100-(_loss*100)/_money)
        f.write(f'-------% {100-(_loss*100)/_money} \n')
    backspin = False
    year = random.random()
    for user_spin in settings['backspin']:
        if user_spin['id_user'] == token:
            if year > 0.5:
                backspin = True
                if user_spin['numSpin'] > 0:
                    user_spin['numSpin']-=1
                    if user_spin['numSpin'] == 0:
                        settings['backspin'].remove(user_spin)
    if not (_money == _loss):
        subCoef = 0
        items_in_case = sorted(items_in_case, key=lambda student: student['price'])[::-1]
        for item in items_in_case:
            print(f'+++ {_loss + item["price"]}  <  {_money * (float(100 - settings["profit"]) / 100)}')
            f.write(f'+++ {_loss + item["price"]}  <  {_money * (float(100 - settings["profit"]) / 100)} \n')
            if _loss + item['price'] <= _money * (float(100 - settings['profit']) / 100) and item['coef'] != 0:
                subCoef = float(item['coef'])
                break
        if subCoef == 0:
            subCoef = 0.8
        print('------??????',subCoef)
        f.write(f'------?????? {subCoef} \n')
        coef = random.uniform(subCoef, max_coef)
        print(coef, '???? ????????????????')
        win_item = None
        items_in_case = sorted(items_in_case, key=lambda student: student['coef'])[::-1]
        for item in items_in_case:
            if coef > float(item['coef']):
                win_item = item
                f.write('--------end\n\n')
                if _money != _loss:
                    gr.write(f'{round(100 - (_loss * 100) / _money)}	    {round(_money)}	    {round(_loss)}\n')
                    gr.close()
                f.close()
                break
        return win_item
    else:
        coef = random.uniform(0.5, max_coef)
        items_in_case = sorted(items_in_case, key=lambda student: student['coef'])[::-1]
        for item in items_in_case:
            if coef > float(item['coef']):
                win_item = item
                f.write('--------end\n\n')
                if _money != _loss:
                    gr.write(f'{round(100 - (_loss * 100) / _money)}	    {round(_money)}	    {round(_loss)}\n')
                    gr.close()
                f.close()
                break
        return win_item


def Upgrade_script(id_user, id_to_item, id_from_item):
    print('hello')