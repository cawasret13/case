import ast
import asyncio
import json
import random
from urllib import parse
import requests
from channels.db import database_sync_to_async
from djangochannelsrestframework.decorators import action
from djangochannelsrestframework.generics import GenericAsyncAPIConsumer
from datetime import datetime

from chat.models import cases, HistoryCase, Users, item
from djangochannelsrestframework.observer import model_observer

from chat.script import Case_script

url_server = '192.168.1.68:8000'
api_key_tm = 'a6Eg5gF0ge38F9Pvc70YpPN091Yu3M7'

class consumersTest(GenericAsyncAPIConsumer):

    async def connect(self):
        await self.accept()
        await self.send_json(json.dumps(await self.get_name()))
        await self.send_mas_his.subscribe()
        await self.SendMoney.subscribe()

    @database_sync_to_async
    def get_name(self):
        name = []
        for i in cases.objects.all():
            name.append(
                {'name': i.name, 'img': (f'http://{url_server}/media/' + i.icon.name), 'price': i.price, 'items': 22,
                 'id_case': i.id_case}
            )
        return name

    @model_observer(HistoryCase)
    async def send_mas_his(self, message, observer=None, **kwargs):
        await self.send_all_mas()

    @action()
    async def send_all_mas(self):
        # await self.send_json(json.dumps(await self.get_last_history()))
        print('dksksd')

    @database_sync_to_async
    def get_last_history(self):
        name = []
        fin = []
        step = 0
        for i in HistoryCase.objects.all():
                name.append({
                    'name': i.name,
                    'img': i.img
                })
        name = name[::-1]
        for item in name:
            if(step < 20 and step > 5):
                fin.append(item)
            else:
                if step >= 20:
                    break
            step+=1
        return fin

    @model_observer(Users)
    async def SendMoney(self, message, observer=None, **kwargs):
        await self.SendMoneyFun()

    @action()
    async def SendMoneyFun(self):
        await self.send_json({'action':'money'})


class Case(GenericAsyncAPIConsumer):

    async def connect(self):
        await self.accept()

    @action()
    async def join_case(self, pk, **kwargs):
        await self.send_json(json.dumps(await self.get_case(pk)))

    @action()
    async def open_case(self, pk, **kwargs):
        num = 0
        for i in range(1000):
            num+=1
            items = await self.op_case(pk[0], pk[1], pk[2], num)
            if items != 'err':
                await self.send_json(json.dumps(items))
                await self.add_inventory(items['items'][39]['id'], pk[1])
                await self.create_history(items['items'][39])
            else:
                await self.send_json(json.dumps({'err':'100'}))

    @database_sync_to_async
    def op_case(self, case, token, mode, num):
        case = cases.objects.get(id_case=case)
        __items = case.items
        user = Users.objects.get(token=token)
        if user.money >= case.price:
            history = case.history
            case.money += case.price
            user.money -= case.price
            items_case = []
            items = []
            for item_ in  __items:
                for a in item_:
                    item = item_[a]
                    items_case.append(
                        {'name': item['name'], 'img': item['img'], 'id': item['id'],
                         'price': item['price'], 'coef':float(item['coef'])})
            items_case = sorted(items_case, key=lambda student: student['coef'])[::-1]
            for item in range(66):
                coef = random.random()
                for item_ in items_case:
                   if coef < item_['coef']:
                       items.append(item_)
            user.save()
            items[39]=Case_script(token , case.id_case, num)
            case.loss += int(items[39]['price'])

            history.append({'date':json.dumps((datetime.now().date()), indent=4, sort_keys=True, default=str), 'id_item':items[39]['id'], 'id_user':token, 'price':items[39]['price']})
            case.history = history
            case.save()
            res = False
            if case.price <= items[39]['price']:
                res = True
            return ({'items': items, 'result': res, 'mode':mode})
        else:
            return 'err'

    @database_sync_to_async
    def get_case(self, id):
        case = cases.objects.get(id_case=id)
        items_case = case.items
        items = []
        for item in items_case:
            for a in item:
                info_item = item[a]
                items.append({'name': info_item['name'], 'img': info_item['img'], 'id':item, 'price':info_item['price']})
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

class UserWeb(GenericAsyncAPIConsumer):

    async def connect(self):
        await self.accept()

    @action()
    async def getInventory(self, pk, **kwargs):
        await self.send_json({'action':'inventory', 'data':json.dumps(await self.getUserInventory(pk))})

    @action()
    async def saleItem(self, pk, **kwargs):
        await self.setDBItem(pk[0], pk[1])
        await self.send_json({'action': 'inventory', 'data': json.dumps(await self.getUserInventory(pk[0]))})
    @action()
    async def exportItem(self, pk, **kwargs):
        await self.exportItemDB(pk[0], pk[1])
        await self.send_json({'action': 'inventory', 'data': json.dumps(await self.getUserInventory(pk[0]))})

    @database_sync_to_async
    def getUserInventory(self, id):
        user = Users.objects.get(token=id)
        inventory = ast.literal_eval(user.inventory)
        list = []
        for item_inv in inventory:
            itema = item.objects.get(id_item=item_inv)
            list.append({'name':itema.name, 'price':itema.price, 'id':itema.id_item, 'img': (f'http://{url_server}/media/' + itema.icon.name)})
        return list

    @database_sync_to_async
    def setDBItem(self, id_user, id_item):
        user = Users.objects.get(token=id_user)
        inventory = ast.literal_eval(user.inventory)
        for itemq in inventory:
            if itemq == id_item:
                itemdb = item.objects.get(id_item=id_item)
                user.money+=float(itemdb.price)
                inventory.remove(id_item)
                break
        user.inventory = inventory
        user.save()

    @database_sync_to_async
    def exportItemDB(self, id_user, id_item):
        user = Users.objects.get(token=id_user)
        inventory = ast.literal_eval(user.inventory)
        for itemq in inventory:
            if itemq == id_item:
                inventory.remove(id_item)
                break
        user.inventory = inventory
        # user.save()
        items__ = item.objects.get(id_item=id_item)
        hash_name = items__.hash_name
        price = int((float(items__.price)+(float(items__.price)*2))*1000)
        all_instances = parse.urlparse(user.tradeLink)
        url = f'https://market.csgo.com/api/v2/buy-for?key={api_key_tm}&hash_name={hash_name}&price={price}&{all_instances.query}'
        exp = requests.get(url)
        print(exp.text)
