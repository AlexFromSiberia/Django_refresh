from django.urls import path
from .views import MoviesView, MovieDetailView, AddReview, ActorView


urlpatterns = [
    path('', MoviesView.as_view(), name='movie_list'),
    path('<slug:slug>/', MovieDetailView.as_view(), name='movie_detail_view'),
    path('<int:pk>', AddReview.as_view(), name='add_review'),
    path('actor/<str:slug>', ActorView.as_view(), name='actor_detail'),
]
