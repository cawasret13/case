import ast
import json
import random

from chat.models import Users, item
from djangochannelsrestframework.decorators import action
from djangochannelsrestframework.generics import GenericAsyncAPIConsumer
from channels.db import database_sync_to_async

from test.settings import url_server
DB_ITEMS = item


class Upgrade(GenericAsyncAPIConsumer):
    async def connect(self):
        await self.accept()

    @action()
    async def user_items(self, pk, **kwargs):
        token = pk
        await self.send_json(await self.get_items_user(token))

    @action()
    async def get_items(self, pk, **kwargs):
        filter = pk
        await self.send_json(await self.get_items_db(filter))

    @action()
    async def spin(self, pk, **kwargs):
        await self.send_json(await self.play(pk['token'], pk['item_from'], pk['item_to']))

    @database_sync_to_async
    def get_items_user(self, token):
        user = Users.objects.get(token=token)
        inventory = ast.literal_eval(user.inventory)
        _inventory = []

        for item_inv in inventory:
            itema = item.objects.get(id_item=item_inv)
            _inventory.append({'name': itema.name, 'price': itema.price, 'id': itema.id_item,
                               'img': (f'http://{url_server}/media/' + itema.icon.name), 'id': itema.id_item})

        return json.dumps({"action": "user_items", "inventory": json.dumps(_inventory)})

    @database_sync_to_async
    def get_items_db(self, filter):
        if filter['name'] == None:
            filter['name'] = '|'
        if filter['min'] != None and filter['max'] != None and filter['max'] != '' and filter['min'] != '':
            items_ = DB_ITEMS.objects.filter(price__range=(filter['min'], filter['max'])).filter(
                name__contains=filter['name'])
        elif filter['min'] != None and filter['min'] != '':
            items_ = DB_ITEMS.objects.filter(price__gt=filter['min']).filter(name__contains=filter['name'])
        elif filter['max'] != None and filter['max'] != '':
            items_ = DB_ITEMS.objects.filter(price__range=(0, filter['max'])).filter(name__contains=filter['name'])
        else:
            items_ = DB_ITEMS.objects.all().filter(name__contains=filter['name'])
        items = []
        items_ = sorted(items_, key=lambda student: student.price)
        for item_ in items_:
            items.append(
                {'name': item_.name, 'price': item_.price, 'img': (f'http://{url_server}/media/' + item_.icon.name),
                 'id': item_.id_item})
        return json.dumps({"action": "get_items", "items": json.dumps(items)})

    @database_sync_to_async
    def play(self, token, _item_from, _item_to):
        with open('static/settings.json') as file:
            settings = json.load(file)[0]
        item_from = DB_ITEMS.objects.get(id_item=_item_from)
        item_to = DB_ITEMS.objects.get(id_item=_item_to)
        user = Users.objects.get(token=token)
        inventory = ast.literal_eval(user.inventory)
        result_item = {}
        subcoef = (item_from.price / item_to.price)
        start_position = -7
        coef = random.random()
        if (coef <= (subcoef / settings['division'])):
            position_cursor = random.randint(start_position, int(subcoef * 3.6 * 100))
            status = True
            result_item = {'name':item_to.name, 'price':item_to.price, 'img':(f'http://{url_server}/media/' + item_to.icon.name)}
            inventory.remove(_item_from)
            inventory.append(_item_to)
        else:
            position_cursor = random.randint(int(subcoef * 360 - 7), int(int(subcoef * 360 - 7) + (int(subcoef * 360 - 7) *0.25)))
            status = False
            inventory.remove(_item_from)
        user.inventory = inventory
        user.save()
        list = []
        for item_inv in inventory:
            itema = item.objects.get(id_item=item_inv)
            list.append({'name': itema.name, 'price': itema.price, 'id': itema.id_item,
                         'img': (f'http://{url_server}/media/' + itema.icon.name), 'id': itema.id_item})
        return json.dumps({'action': 'spin', 'start': start_position, 'cursor': position_cursor + (random.randint(3, 5) * 360), 'status':status, 'res_item': result_item, 'inventory': json.dumps(list)})
