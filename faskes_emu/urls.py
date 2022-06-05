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
from django.urls import path, re_path, include
from rest_framework import routers
from pendaftaran.views import DataPasienViewSet
from django.conf import settings
from django.conf.urls.static import static
from laporan.views import index_page, laporan_page, penggunaan_bmhp, cetak_kartu_stok, lap_narko_psiko, tengok_stok_alkes, tengok_stok_obat, contact_developer, lap_generik, lap_por

from utils.utils import download_backup
from django.contrib.auth.views import LoginView

router = routers.DefaultRouter()
router.register(r'datapasien', DataPasienViewSet) 

urlpatterns = [
    path('app/', admin.site.urls),
    path('', index_page, name='index_page'),
    path('laporan/', laporan_page, name='laporan_page'),
    path('utils/backupd', download_backup, name='backupd'),
    path('kontak_dev/', contact_developer, name='contact_dev'),
    path('laporan/penggunaan_bmhp/', penggunaan_bmhp, name='penggunaan_bmhp'),
    path('laporan/cetak_kartu_stok/', cetak_kartu_stok, name='cetak_kartu'),
    path('laporan/lap_narko_psiko/', lap_narko_psiko, name='lap_narko_psiko'),
    path('laporan/tengok_stok_alkes/', tengok_stok_alkes, name='tengok_alkes'),
    path('laporan/tengok_stok_obat/', tengok_stok_obat, name='tengok_obat'),
    path('laporan/lap_generik/', lap_generik, name='lap_generik'),
    path('laporan/lap_por/', lap_por, name='lap_por'),
    re_path(r"^accounts/login/*", LoginView.as_view(), name="login"),
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
