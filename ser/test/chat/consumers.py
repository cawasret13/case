import ast
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

from test.settings import url_server
api_key_tm = 'a6Eg5gF0ge38F9Pvc70YpPN091Yu3M7'
db_items = item
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
    @action()
    async def addMoney(self, pk, **kwargs):
        await self.add(pk)

    @database_sync_to_async
    def add(self, token):
        user = Users.objects.get(token=token)
        user.money += 1000
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
            itema = db_items.objects.get(id_item=item_inv)
            list.append({'name':itema.name, 'price':itema.price, 'id':itema.id_item, 'img': (f'http://{url_server}/media/' + itema.icon.name)})
        return list

    @database_sync_to_async
    def setDBItem(self, id_user, id_item):
        user = Users.objects.get(token=id_user)
        inventory = ast.literal_eval(user.inventory)
        for itemq in inventory:
            if itemq == id_item:
                itemdb = db_items.objects.get(id_item=id_item)
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
        items__ = db_items.objects.get(id_item=id_item)
        hash_name = items__.hash_name
        price = int((float(items__.price)+(float(items__.price)*2))*1000)
        all_instances = parse.urlparse(user.tradeLink)
        url = f'https://market.csgo.com/api/v2/buy-for?key={api_key_tm}&hash_name={hash_name}&price={price}&{all_instances.query}'
        exp = requests.get(url)
        print(exp.text)
