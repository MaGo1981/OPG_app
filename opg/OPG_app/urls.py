from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path("register", views.register_user, name="register"),
    path("profile", views.profile, name="profile"),
    path("profile/edit", views.edit_profile, name="edit_profile"),
    path("login", views.login, name="login"),
    path("logout", views.logout, name="logout"),
    path("product_list", views.products, name="products"),
    path("product/<int:product_id>", views.product, name="product"),
    path("product/add", views.add_product, name="add_product"),
    path("product/<int:product_id>/edit", views.edit_product, name="edit_product"),
    path("product/delete/<int:product_id>", views.del_product, name="del_product"),
]
