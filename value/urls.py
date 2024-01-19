
from django.urls import path
from value.views import get_data, sign_out

urlpatterns = [
    path('get-data/', view=get_data, name="get_data"),
    path('sign-out/', view=sign_out, name="sign_out")
]