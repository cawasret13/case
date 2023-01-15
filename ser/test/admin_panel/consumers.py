import json

from channels.db import database_sync_to_async
from djangochannelsrestframework.decorators import action
from djangochannelsrestframework.generics import GenericAsyncAPIConsumer
from datetime import datetime

from chat.models import cases, item
from test.settings import url_server
class Case_admin(GenericAsyncAPIConsumer):
    async def connect(self):
        await self.accept()

    @action()
    async def join_admin_case(self, pk, **kwargs):
        await self.send_json(json.dumps({'action': 'result', 'data': await self.get_case(pk), 'grath':await self.grath(pk)}))

    @database_sync_to_async
    def get_case(self, id_case):
        case = cases.objects.get(id_case=id_case)
        items_data = item.objects.all()
        items = case.items
        info = []
        for item_ in items_data:
            if item_.icon.name != None:
                info.append({'name': item_.name, 'price': item_.price, 'id_item': item_.id_item,
                             'img': (f'http://{url_server}/media/' + item_.icon.name)})
        return (json.dumps({'id_case': case.id_case, 'name': case.name, 'price': case.price,
                                    'img': (f'http://{url_server}/media/' + case.icon.name), 'items': json.dumps(items),
                                    'amount_items': 22, 'status': case.status, 'data': json.dumps(info)}))

    @database_sync_to_async
    def grath(self, id_case):
        date = (datetime.now().date())
        case = cases.objects.get(id_case=id_case)
        history = case.history
        pr = num = []
        price_case = case.price
        money = loss = count = 0
        gl_money = []
        for cell in history:
            if cell != {} :
                if (json.loads(cell['date']) == str(date)):
                    num.append(round(count + 1))
                    count += 1
                    money += float(price_case)
                    loss += float(cell['price'])
                    pr.append(round(money - loss))
        arr_day = []
        for day in range(1, 32):
            arr_day.append(day)
            _money = 0
            for cell in history:
                if cell != {}:
                    date_cell = datetime.strptime(str(json.loads(cell['date'])), "%Y-%m-%d")
                    if date.month == date_cell.month and date.year == date_cell.year and date_cell.day == day:
                        _money += float(price_case - cell['price'])
            gl_money.append(_money)
        print(gl_money)
        return json.dumps({'data':json.dumps(pr), 'labels':json.dumps(num), 'days':json.dumps(arr_day), 'volue_day':json.dumps(gl_money)})
