"""onlineComputerStoreProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from onlineComputerStore import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index),
    path('login/', views.login),
    path('register/', views.register),
    path('logout/', views.logout),
    path('account/', views.account),
    path('addItem/', views.addItem),
    path('browse/', views.browse),
    path('browse/<slug:url_slug>', views.browse),
    path('topUp/', views.topUp),
    path('forum/', views.forum),
    path('forum/addDiscussion/', views.addDiscussion),
    path('forum/report/', views.forum_report),
    path('forum/reply/', views.forum_reply),
    path('item/<slug:url_slug>', views.item),
    path('purchase/<slug:url_slug>', views.purchase),
    path('delivery/', views.delivery),
    path('purchaseConfirm/<slug:url_slug>', views.purchaseConfirm),
    path('taboolist/', views.tabooList),
    path('transaction/', views.transaction),
    path('viewOrder/', views.viewOrder),
    path('changePassword/', views.changePassword),
    path('assignDeliCom/', views.assignDeliCom),
    path('justification/', views.justification),
    path('tracking/<slug:url_slug>', views.tracking),
    path('address/', views.address),
    path('viewWarning/', views.viewWarning)
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


