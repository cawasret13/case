from django.urls import path

from admin_panel.consumers import Case_admin
from case.consumers import Case, TestingCase
from chat.consumers import consumersTest, UserWeb
from upgrade.consumers import Upgrade

websocket_url = [
    path('ws/chat/', consumersTest.as_asgi()),
    path('ws/case/', Case.as_asgi()),#перенес
    path('ws/case/testing', TestingCase.as_asgi()),#сделал
    path('ws/admin/case', Case_admin.as_asgi()),
    path('ws/upgrade/', Upgrade.as_asgi()),
    path('ws/user/inventory', UserWeb.as_asgi()),
]