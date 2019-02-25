from django.conf.urls import url
from django.urls import include, path
from . import views
from django.contrib.auth.views import login, logout
from django.contrib.auth import views as auth_views
from sco.forms import CustomAuthForm
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    url(r'^$', views.home, name = 'home'),

    url(r'^login/$', auth_views.login, {'template_name': 'sco/login.html',
    'authentication_form': CustomAuthForm}, name='login'),
    url(r'^logout/$', logout, {'template_name': 'sco/logout.html'}, name = 'logout'),
    url(r'^registrar_usuario/$', views.register, name='register_user'),

    #User
    url(r'^usuarios/$', views.UserListView.as_view(), name='user-list'),
    url(r'^usuario/(?P<pk>\d+)/eliminar$', views.UserDelete.as_view(),
    name='user_delete'),

    #CRUD Document
    url(r'^registrar_oficio/$', views.register_document, name='register_document'),
    url(r'^oficios/$', views.DocumentListView.as_view(), name='document-list'),
    url(r'^oficio/(?P<pk>\d+)/$',views.DocumentDetailView.as_view(),
    name='document_detail'),
    url(r'^oficio/(?P<pk>\d+)/actualizar$', views.document_update, name='document_update'),
    url(r'^oficio/(?P<pk>\d+)/editar$', views.document_edit, name='document_edit'),


    #CRUD Authority
    url(r'^registrar_autoridad/$', views.register_authority, name='register_authority'),
    url(r'^autoridades/$', views.AuthorityListView.as_view(), name='authority-list'),
    url(r'^autoridad/(?P<pk>\d+)/$',views.AuthorityDetailView.as_view(),
    name='authority_detail'),
    url(r'^autoridad/(?P<pk>\d+)/editar$', views.AuthorityUpdate.as_view(),
    name='authority_edit'),
    url(r'^autoridad/(?P<pk>\d+)/eliminar$', views.AuthorityDelete.as_view(),
    name='authority_delete'),

    #CRUD Type = Materia
    url(r'^registrar_materia/$', views.register_type, name='register_type'),
    url(r'^materias/$', views.TypeListView.as_view(), name='type-list'),
    url(r'^materia/(?P<pk>\d+)/editar$', views.TypeUpdate.as_view(),
    name='type_edit'),
    url(r'^materia/(?P<pk>\d+)/eliminar$', views.TypeDelete.as_view(),
    name='type_delete'),

    #search document
    url(r'^buscar_oficio/$', views.document_search, name='document_search'),
    url(r'^search$', views.search, name='search'),
    url(r'^get_authorities$', views.get_authorities, name='get_authorities'),

    #create pdf
    url(r'^generar_oficio_PDF_document/(?P<pk>\d+)/$', views.document_generate_pdf,
     name="document_generate_pdf"),

    url(r'^generar_producto/$', views.document_generate_xml,
     name="document_generate_xml"),
    url(r'^filter_document_type$', views.filter_document_type, name='filter_document_type'),

    url(r'^oficios_asignados/$', views.document_assigned, name="document_assigned"),


    #urlpatterns.append(url(r'^/media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT})),






] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
