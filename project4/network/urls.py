
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path('u/<username>', views.profile, name="profile"),
    path('following/', views.following, name="following"),
    path('like/', views.like),
    path('follow/', views.follow),
    path('edit_post/', views.edit_post),
    path('addpost/', views.addpost),
]



# from django.urls import path
#
# from . import views
#
# urlpatterns = [
#     path("", views.index, name="index"),
#     path("login", views.login_view, name="login"),
#     path("logout", views.logout_view, name="logout"),
#     path("register", views.register, name="register"),
#     path("create", views.create_listing, name="create"),
#     path("categories", views.categories, name="categories"),
#     path("category/<int:id>", views.category, name="category"),
#     path("focus/<int:id>", views.focus, name="focus"), # this is to focus on single product where bid, comment option is given to the user.
#     path("bid/<int:id>", views.bid, name="bid"),
#     path("comment/<int:id>", views.comment, name="comment"),
#     path("add_watchlist/<int:id>", views.add_watchlist, name="add_watchlist"),
#     path("watchlist", views.watchlist, name="watchlist"),
#     path("closebid/<int:id>", views.closebid, name="closebid"),
#     path("closedlisting", views.closedlisting, name="closedlisting"),
# ]