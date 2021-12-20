"""faskes_emu URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path, re_path
from django.conf import settings
from django.conf.urls.static import static
from laporan.views import index_page, laporan_page, penggunaan_bmhp, cetak_kartu_stok, lap_narko_psiko
from utils import download_backup
from django.contrib.auth.views import LoginView    

urlpatterns = [
    path('app/', admin.site.urls),
    path('', index_page, name='index_page'),
    path('laporan/', laporan_page, name='laporan_page'),
    path('utils/backupd', download_backup, name='backupd'),
    path('laporan/penggunaan_bmhp/', penggunaan_bmhp, name='penggunaan_bmhp'),
    path('laporan/cetak_kartu_stok/', cetak_kartu_stok, name='cetak_kartu'),
    path('laporan/lap_narko_psiko/', lap_narko_psiko, name='lap_narko_psiko'),
    re_path(r"^accounts/login/*", LoginView.as_view(), name="login"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
