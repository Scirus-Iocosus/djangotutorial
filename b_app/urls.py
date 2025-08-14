from django.urls import path
from . import views

urlpatterns = [
    path('admin/', views.admin, name="admin"),
    path("", views.index, name="base"),
    path("home/", views.home, name="home"),
    path("info/", views.info, name='info'),
    path("info2/", views.info2, name='info'),
    path("iscrizioni/", views.iscrizioni, name="iscrizioni"),
    path("iscritti/", views.iscrizioni2, name="iscritti"),
    path("appello/squadra/", views.elenco_animati, name='squadra'),
    path("appello/entrata/", views.entrata, name='accoglienza'),
    path("appello/uscita/", views.entrata, name='uscita'),
    path("classifica/", views.classifica, name='classifica'),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path('api/punteggi-rossi/', views.get_punteggio_rosso, name='punteggi-rossi'),
    path('api/punteggi-verdi/', views.get_punteggio_verde, name='punteggi-verdi'),
    path('api/punteggi-gialli/', views.get_punteggio_giallo, name='punteggi-gialli'),
    path('api/punteggi-blu/', views.get_punteggio_blu, name='punteggi-blu'),
    path('api/punteggi/', views.get_punteggi, name='api_punteggi'),
    path('salva_presenze/', views.salva_presenze, name='salva_presenze'),
    path('presenze/cancella/', views.cancella_presenze, name='cancella_presenze'),
    path('presenze/print/', views.presenze_print, name='presenze_print'),
    path('appello/squadra/blu', views.blu, name='squadra_blu'),
    path('appello/squadra/gialli', views.gialli, name='squadra_gialla'),
    path('appello/squadra/verdi', views.verdi, name='squadra_verde'),
    path('appello/squadra/rossi', views.rossi, name='squadra_rossa'),
    path('files/', views.documenti, name="documenti")
]
