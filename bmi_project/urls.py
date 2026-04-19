from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse

def ads_txt(request):
    content = "google.com, pub-8936104184201511, DIRECT, f08c47fec0942fa0"
    return HttpResponse(content, content_type="text/plain")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('ads.txt', ads_txt),
    path('', include('bmi.urls')),
]