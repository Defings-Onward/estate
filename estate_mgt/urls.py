from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('signup', views.sign_up, name='signup'),
    path('properties', views.properties, name='properties'),
    path('manage-property', views.manage_properties, name="manage_property"),
    path('create', views.create_property, name="create"),
    path('property-single/<int:id>', views.property_single, name="property-single"),
    path('card', views.card, name="card"),
    path('services', views.service, name="service"),
    path('service-detail/<int:id>', views.service_detail, name="service-detail"),
    path('contact', views.contact, name="contact"),
    path('about', views.about, name="about"),
    path('agents', views.agent, name="agents"),

    #path('login', views.login, name='login'),

    # path('preview', views.zoom_view, name='zoom_view' )
]