import ast
import json
import random

import requests
from rest_framework.response import Response
from rest_framework.views import APIView
from chat.models import Users, item

url_server = '192.168.1.68:8000'

class AuthUser(APIView):
    def post(self, request, format=None):
        token = self.request.data.get("token")
        print(token)
        try:
            user = Users.objects.get(token=token)
            info = {
                'name':user.name,
                'img':user.img,
                'money': round(user.money, 2)
            }
            return Response(json.dumps(info))
        except:
            req = requests.get(
                f'https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key=3C99FA8D12D9A5A39123D6D5ABD713C9&steamids={token}')
            data = json.loads(req.text)
            print(data['response']['players'][0]['personaname'])
            user = Users(
                token = token,
                name = data['response']['players'][0]['personaname'],
                img = data['response']['players'][0]['avatarfull']
            )
            user.save()
            user = Users.objects.get(token=token)
            info = {
                'name': user.name,
                'img': user.img,
                'money': user.money,
            }
            return Response(json.dumps(info))
        return Response('XXXXXXM')

    # def get(self, request):
    #     res = requests.get('https://market.csgo.com/api/v2/prices/class_instance/RUB.json')
    #     data = json.loads(res.text)['items']
    #     a = 0
    #     for item in data:
    #         if a < 5:
    #             print('\n',item,data[item]['price'], data[item]['market_hash_name'], data[item]['ru_name'],'\n')
    #         else:
    #             return Response('ads')
    #         a+=1

class Upgrade(APIView):
    def get(self, requets, format=None):
        token = self.request.query_params.get('token')
        user = Users.objects.get(token=token)
        inventory = ast.literal_eval(user.inventory)
        items_list = item.objects.all()
        _inventory = []
        items = []

        for item_ in items_list:
            items.append({'name':item_.name, 'price':item_.price, 'img':(f'http://{url_server}/media/' + item_.icon.name), 'id':item_.id_item})

        for item_inv in inventory:
            itema = item.objects.get(id_item=item_inv)
            _inventory.append({'name': itema.name, 'price': itema.price, 'id': itema.id_item,
                         'img': (f'http://{url_server}/media/' + itema.icon.name), 'id':itema.id_item})

        return Response(json.dumps({"items": json.dumps(items), "inventory": json.dumps(_inventory)}))

    def post(self, request, format=None):
        coef = random.random() * 100
        token = self.request.data.get("token")
        user = Users.objects.get(token=token)

        proc = float(self.request.data.get("proc"))
        toItem = self.request.data.get("to")
        fromItem = self.request.data.get("from")
        inventory = ast.literal_eval(user.inventory)
        if float(coef) <= float(proc):
            status = 'Выиграл'
            k = 0
            if coef > 30 and coef < 60:
                k = 10
            elif coef > 120 and coef < 160:
                k = -10
            elif coef > 210 and coef < 240:
                k = 10
            elif coef > 300 and coef < 330:
                k = -10
            else:
                k = 0
            a = (180 - (float(coef) * 1.8) + k)
            b = (180 + (float(coef) * 1.8) + k)
            pi = random.randint(int(a), int(b)) + random.randint(3, 5) * 360
            inventory.remove(fromItem)
            inventory.append(toItem)
        else:
            status = 'Проиграл'
            k = 0
            if coef > 30 and coef < 60:
                k = 10
            elif coef > 120 and coef < 160:
                k = -10
            elif coef > 210 and coef < 240:
                k = 10
            elif coef > 300 and coef < 330:
                k = -10
            else:
                k = 0
            a = (180 - (float(coef) * 1.8) + k)
            b = (180 - (float(coef) * 1.8) + k) * -1
            pi = random.randint(int(b), int(a)) + random.randint(3, 5) * 360
            inventory.remove(fromItem)
        # print(coef ,'<',proc, pi, k)
        user.inventory = inventory
        user.save()
        list = []
        for item_inv in inventory:
            itema = item.objects.get(id_item=item_inv)
            list.append({'name': itema.name, 'price': itema.price, 'id': itema.id_item,
                               'img': (f'http://{url_server}/media/' + itema.icon.name), 'id': itema.id_item})
        return Response(json.dumps({'pi':pi, 'items':json.dumps(list), 'status':status}))

class  Contract(APIView):
    def post(self, request, format=None):
        data = json.loads(self.request.data.get('data'))
        items = data['items']
        user = Users.objects.get(token=data['token'])
        inventory = ast.literal_eval(user.inventory)
        for item_ in items:
            inventory.remove(item_)
        price = 0
        for item_ in items:
            item__ = item.objects.get(id_item=item_)
            price += item__.price
        min_price = round((price / 4))
        max_price = round(((price * 307) / 100))
        _price = random.randint(min_price, max_price)
        print(price, min_price, max_price, _price)
        items_ = item.objects.all()
        items_all = []
        for it in items_:
            items_all.append({'id':it.id_item, 'price':it.price,  'img': (f'http://{url_server}/media/' + it.icon.name), 'name':it.name})
        tems = sorted(items_all, key=lambda student: student['price'])
        select_item = None
        for sel_item in tems:
            if sel_item['price'] > _price:
                select_item = sel_item
                break
        inventory.append(select_item['id'])
        user.inventory = inventory
        user.save()
        return Response(json.dumps({'win':json.dumps(select_item), 'inventory':json.dumps(inventory) }))
    def get(self, request, format=None):
        items = item.objects.all()
        data = json.loads(requests.get('https://market.csgo.com/api/v2/prices/RUB.json').text)['items']
        for _item in items:
            for _item_market in data:
                if _item.hash_name == _item_market['market_hash_name']:
                    _item_db = item.objects.get(hash_name=_item_market['market_hash_name'])
                    _item_db.price = 1000
                    _item_db.save()
        return Response('k')