import ast
import json
import random
import time

from channels.db import database_sync_to_async
from djangochannelsrestframework.decorators import action
from djangochannelsrestframework.generics import GenericAsyncAPIConsumer
from datetime import datetime

from case.script import Script_testing
from chat.models import cases, HistoryCase, Users, item

from case.script import Case_script

from test.settings import url_server
api_key_tm = 'a6Eg5gF0ge38F9Pvc70YpPN091Yu3M7'
db_items = item


class Case(GenericAsyncAPIConsumer):

    async def connect(self):
        await self.accept()

    @action()
    async def join_case(self, pk, **kwargs):
        await self.send_json(json.dumps(await self.get_case(pk)))

    @action()
    async def open_case(self, pk, **kwargs):
        items = await self.op_case(pk[0], pk[1], pk[2])
        if items != 'err':
            await self.send_json(json.dumps(items))
            await self.add_inventory(items['items'][39]['id'], pk[1])
            await self.create_history(items['items'][39])
        else:
            await self.send_json(json.dumps({'err': '100'}))

    @database_sync_to_async
    def op_case(self, case, token, mode):
        case = cases.objects.get(id_case=case)
        __items = case.items
        user = Users.objects.get(token=token)
        if user.money >= case.price:
            history = case.history
            case.money += case.price
            user.money -= case.price
            items_case = []
            items = []
            for item_ in __items:
                for a in item_:
                    _item_ = item_[a]
                    _item = db_items.objects.get(id_item=a)
                    items_case.append(
                        {'name': _item_['name'], 'img': (f'http://{url_server}/media/' + _item.icon.name),
                         'id': _item_['id'],
                         'price': _item_['price'], 'coef': float(_item_['coef'])})
            items_case = sorted(items_case, key=lambda student: student['coef'])[::-1]
            for item in range(66):
                coef = random.random()
                for item_ in items_case:
                    if coef < item_['coef']:
                        items.append(item_)
            user.save()
            items[39] = Case_script(token, case.id_case)
            case.loss += int(items[39]['price'])
            item_win_DB = db_items.objects.get(id_item=items[39]['id'])
            items[39]['img'] = (f'http://{url_server}/media/' + item_win_DB.icon.name)
            history.append({'date': json.dumps((datetime.now().date()), indent=4, sort_keys=True, default=str),
                            'id_item': items[39]['id'], 'id_user': token, 'price': items[39]['price']})
            case.history = history
            case.save()
            res = False
            if case.price <= items[39]['price']:
                res = True
            return ({'items': items, 'result': res, 'mode': mode})
        else:
            return 'err'

    @database_sync_to_async
    def get_case(self, id):
        case = cases.objects.get(id_case=id)
        items_case = case.items
        items = []
        for __item in items_case:
            for a in __item:
                info_item = __item[a]
                _item = db_items.objects.get(id_item=a)
                items.append(
                    {'name': info_item['name'], 'img': (f'http://{url_server}/media/' + _item.icon.name), 'id': a,
                     'price': info_item['price']})
        return {'name': case.name, 'img': (f'http://{url_server}/media/' + case.icon.name), 'price': case.price,
                'items': json.dumps(items)}

    @database_sync_to_async
    def create_history(self, data):
        history = HistoryCase(
            name=data['name'],
            img=data['img']
        )
        history.save()

    @database_sync_to_async
    def add_inventory(self, item, token):
        user = Users.objects.get(token=token)
        inv = []
        inventory = user.inventory
        for ite in ast.literal_eval(inventory):
            inv.append(ite)
        inv.append(item)
        user.inventory = inv
        user.save()


class TestingCase(GenericAsyncAPIConsumer):
    @action()
    async def testing_case(self, pk, **kwargs):
        spins = int(pk[0])
        applay_Rules = pk[4]
        if not applay_Rules:
            coef_compensation = float(pk[1])
            coef_profit = float(pk[2])
        else:
            coef_compensation = 0
            coef_profit = 0
        id_case = pk[3]
        rules = pk[5]
        res = []
        history = []
        prog_value = 0
        for i in range(spins + 1):
            item = await Script_testing(coef_compensation, coef_profit, id_case, history, applay_Rules, rules)
            res.append(item)
            history.append({'id_item': item['id'], 'price': item['price'], 'sub':item['sub'], 'coef':item['coef']})
            prog_value += 1
            await self.send_json(json.dumps({'action': 'progress', 'value': int((prog_value/spins)*100), 'load':prog_value, 'allLoad':spins}))

        price_case = int(await self.price_case(id_case))
        money = len(history) * price_case
        loss = 0
        frequency = 0
        loss_grath = []
        for cell in history:
            loss += float(cell['price'])
            loss_grath.append(loss)
            if float(cell['price']) >= price_case:
                frequency+=1
        profit = money - loss
        labels = []
        money_grath = []
        for index in range(spins + 1):
            labels.append(index)
            money_grath.append(price_case * index)
        items = []
        black_list=[]
        for item in res:
            if item['id'] not in black_list:
                items.append({'id':item['id'],'name':item['name'],'price':item['price'], 'count':0, 'sub':item['sub'], 'coef':item['coef']})
                black_list.append(item['id'])
        for item in items:
            for item_ in res:
                if item_['id'] == item['id']:
                    item['count']+=1
        items_case = await self.items_case(id_case)
        for item_ in items_case:
            for item in item_:
                if item not in black_list and item_[item]['coef'] != 0:
                    items.append({'id': item_[item]['id'], 'name': item_[item]['name'], 'price': item_[item]['price'], 'count': 0, 'coef':item_[item]['coef']})
        data = {
            'spins':spins,
            'coef_com': coef_compensation,
            'coef_prof': coef_profit,
            'coef': (1-(loss / money)),
            'money':round(money),
            'loss':round(loss),
            'profit':round(profit),
            'frequency':frequency,
            'items':json.dumps(items),
            'applay_Rules':applay_Rules,
            'rules':rules,
        }
        grath = {'labels':json.dumps(labels), 'money':json.dumps(money_grath) ,'loss':json.dumps(loss_grath)}
        await self.send_json(json.dumps({'action':'result', 'data':json.dumps(data), 'grath':json.dumps(grath), 'spins':spins, 'coef_com':coef_compensation, 'coef_prof':coef_profit, 'money':round(money), 'loss':round(loss), 'profit':round(profit), 'frequency':frequency}))

    @database_sync_to_async
    def price_case(self, id_case):
        case = cases.objects.get(id_case=id_case)
        return case.price

    @database_sync_to_async
    def items_case(self, id_case):
        case = cases.objects.get(id_case=id_case)
        return case.items

    @action()
    async def applaySettings(self, pk, **kwargs):
        print('HHHHHHHHHH')
        id_case = pk[0]
        applayRules = pk[1]
        if not applayRules:
            coef = pk[2]
            coef_com = pk[3]
        else:
            coef = 0
            coef_com = 0
        rules = pk[4]
        await self.saveSettings(id_case, applayRules, coef, coef_com, rules)

    @database_sync_to_async
    def saveSettings(self, id_case, applayRules, coef, coef_com, rules):
        case = cases.objects.get(id_case=id_case)
        print('CCC',id_case, applayRules, coef, coef_com, rules)
        case.applayRules = applayRules
        if not applayRules:
            case.coef_profit = coef
            case.coef_compensation = coef_com
        else:
            case.rules = rules
        case.save()
