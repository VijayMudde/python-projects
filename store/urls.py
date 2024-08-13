from django.urls import path
from . import views

urlpatterns = [

        path('', views.store, name="store"),
        path('store/', views.store, name="store"),
        path('cart/', views.cart, name="cart"),
        path('checkout/', views.checkout, name="checkout"),
        path('update_item/', views.updateItem, name="update_item"),
        path('track_order/', views.track_order, name="track_order"),
        path('register/', views.register, name="register"),
        path('navbar/', views.navbar, name="navbar"),
        path('login/', views.login, name="login"),
        path('logout/', views.logout, name="logout"),
        path('about_us/', views.about_us, name="about_us"),
        path('contact_us/', views.contact_us, name="contact_us"),
        path('faq/', views.faq, name="faq"),
        path('track/', views.track, name="track"),
        path('offer/', views.offer, name="offer"),
        path('returns/', views.returns, name="returns"),
        path('gift/', views.gift, name="gift"),
        path('blog/', views.blog, name="blog"),
        path('press/', views.press, name="press"),
        path('career/', views.career, name="career"),
        path('profile/', views.profile, name="profile"),
        path('order_history/', views.order_history, name='order_history'),
        path('update_profile/', views.update_profile, name='update_profile'),
        path('update_password/', views.update_password, name='update_password'),
        path('order/', views.order, name='order'),
                
]