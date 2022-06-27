from django.urls import path
#from .views import TicketViewSet
from . import views
from .views import TicketAPIView

urlpatterns = [
    #path('TicketViewSet/<int:id>', views.TicketViewSet,name = "TicketViewSet"),
    path('helpdesk/<int:pk>/',TicketAPIView.as_view()),
]