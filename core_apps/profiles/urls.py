from django.urls import path
from . import views as profileViews

urlpatterns = [
    path("all/", profileViews.ProfileListAPIView.as_view(), name="all-profiles"),
    path("detail/", profileViews.ProfileDetailAPIView.as_view(), name="my-profile"),
    path("me/update/", profileViews.UpdateProfileAPIView.as_view(),
         name="update-profile"),
    path("me/followers/", profileViews.FlolewerListView.as_view(), name="followers"),
    path("<uuid:user_id>/follow/",
         profileViews.FollowAPIView.as_view(), name="follow"),
    path("<uuid:user_id>/unfollow/",
         profileViews.UnFollowAPIView.as_view(), name="unfollow"),
]
