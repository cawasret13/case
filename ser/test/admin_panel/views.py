import json
import random

import requests
from rest_framework.response import Response
from rest_framework.views import APIView
from chat.models import cases, item

url_server = '192.168.1.68:8000'


class Case(APIView):
    def get(self, request, format=None):
        cases_ = cases.objects.all()
        list_cases = []
        for case in cases_:
            list_cases.append(
                {'name': case.name, 'img': (f'http://{url_server}/media/' + case.icon.name), 'price': case.price,
                 'items': case.amount_items,
                 'id_case': case.id_case, 'status': case.status}
            )
        return Response(json.dumps(list_cases[::-1]), )


class GetCase(APIView):
    def get(self, request, format=None):
        id_case = self.request.query_params.get('id_case')
        case = cases.objects.get(id_case=id_case)
        items_data = item.objects.all()
        items = case.items
        info = []
        for item_ in items_data:
            if item_.icon.name != None:
                info.append({'name': item_.name, 'price': item_.price, 'id_item': item_.id_item,
                             'img': (f'http://{url_server}/media/' + item_.icon.name)})
        return Response(json.dumps({'id_case': case.id_case, 'name': case.name, 'price': case.price,
                                    'img': (f'http://{url_server}/media/' + case.icon.name), 'items': json.dumps(items),
                                    'amount_items': 22, 'status': case.status, 'data': json.dumps(info)}))

    def options(self, request, format=None):
        data = json.loads(self.request.data.get("data"))
        case = cases.objects.get(id_case=data['id_case'])
        case.items = data['items']
        case.price = data['price']
        case.amount_items = len(case.items) - 1
        case.save()
        return Response(json.dumps('hhh'))

    def post(self, request, format=None):
        name = self.request.data.get('name')
        file = request.data.get('file')
        price = self.request.data.get('price')
        key = generate_key()
        casea = cases(
            id_case=key,
            name=name,
            price=price,
            icon=file,
            items=[{}]
        )
        casea.save()
        return Response(json.dumps(key))


def generate_key():
    key = random.randint(1000000, 9999999)
    if(len(cases.objects.filter(id_case=key))) == 0:
        return key
    else:
        generate_key()

class GetItems(APIView):
    def get(self, request):
        items = item.objects.all()
        list = []
        for itema in items:
            list.append({'name':itema.name, 'price':itema.price, 'img':(f'http://{url_server}/media/' + itema.icon.name), 'id':itema.id_item})
        return Response(json.dumps(list[::-1]))
    def post(self, request):
        file = self.request.data.get('file')
        id = self.request.data.get('id')
        item_ = item.objects.get(id_item=id)
        item_.icon = file
        item_.save()
        return Response(json.dumps('good'))

class AddItems(APIView):
    def get(self, request):
        data =  requests.get('https://market.csgo.com/api/v2/prices/class_instance/RUB.json')
        items = json.loads(data.text)['items']
        list = []
        for item in items:
            print(items[item])
            item_=items[item]
            if '(Well-Worn)' in item_['market_hash_name']:
                list.append({'price':item_['price'], 'name':item_['ru_name'],'id':item, 'hash':item_['market_hash_name']})
        return Response(json.dumps(list))
    def post(self, request):
        data = self.request.data.get('data')
        print(data)
        for item_ in json.loads(data):
            create_item = item(
                name=item_['name'].split('(')[0],
                price=item_['price'],
                id_item=item_['id'],
                hash_name=item_['hash']
            )
            create_item.save()
        return Response(json.dumps('ddd'))
