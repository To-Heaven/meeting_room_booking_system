"""meeting_room_booking_system URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
# from django.urls import path, include
from django.urls import path, include
from room import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path(r'room/<int:year>/<int:month>/<int:day>/', views.table_change, name='table_orders'),
    path(r'room/', views.table_orders, name='table_orders'),
    path(r'room/login/', views.login),
    path(r'room/checkout/<int:order_id>/', views.checkout),     # int:xxx 之间不能有空格
    path(r'room/commit_choice/', views.commit_choice),
]
