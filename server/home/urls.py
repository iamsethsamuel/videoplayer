from django.urls import path, re_path
from . import views

urlpatterns = [ 
    path('',views.home),
    path("js/<str:file>",views.JSFiles,name='JSFiles'),
    path("createhls",views.createHLS),
    path("files/<str:src>",views.fileSource),
    path("files/<str:src>/<str:src1>",views.fileSourceFormat)
] 
