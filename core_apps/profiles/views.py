# TODO : change this in production

from authors_api.settings.local import DEFAULT_FROM_EMAIL
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser

from .exceptions import CantFollowYourself
from .models import Profile
from .pagination import ProfilePagination
from .renderers import ProfileJSONRenderer, ProfilesJSONRenderer
from .serializers import ProfileSerializer, FollowingSerializer, UpdateProfileSerializer

User = get_user_model()


class ProfileListAPIView(generics.ListAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    pagination_class = ProfilePagination
    renderer_classes = [ProfilesJSONRenderer,]


class ProfileDetailAPIView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ProfileSerializer
    renderer_classes = [ProfileJSONRenderer,]

    def get_queryset(self):
        queryset = Profile.objects.select_related('user')
        return queryset

    def get_object(self):
        user = self.request.user
        profile = self.get_queryset().get(user=user)
        return profile


class UpdateProfileAPIView(generics.UpdateAPIView):
    serializer_class = UpdateProfileSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser]
    renderer_classes = [ProfileJSONRenderer,]

    def get_object(self):
        profile = self.request.user.profile
        return profile

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class FlolewerListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        try:
            profile = Profile.objects.get(user__id=request.user.id)
            follower_profiles = profile.followers.all()
            serializer = FollowingSerializer(follower_profiles, many=True)
            format_response = {
                "status_code": status.HTTP_200_OK,
                "followers_count": follower_profiles.count(),
                "followers": serializer.data
            }
            return Response(format_response, status=status.HTTP_200_OK)
        except Profile.DoesNotExist:
            raise Response(status=404)


class FlolowingListView(APIView):
    def get(self, request, user_id, format=None):
        try:
            profile = Profile.objects.get(user__id=user_id)
            following_profiles = profile.followers.all()
            users = [p.user for p in following_profiles]
            serializer = FollowingSerializer(users, many=True)
            format_response = {
                "status_code": status.HTTP_200_OK,
                "followers_count": following_profiles.count(),
                "users_i_follow": serializer.data
            }
            return Response(format_response, status=status.HTTP_200_OK)
        except Profile.DoesNotExist:
            raise Response(status=404)


class FollowAPIView(APIView):
    def post(self, request, user_id, format=None, *args, **kwargs):
        try:
            follewers = Profile.objects.get(user=self.request.user)
            user_profile = request.user.profile
            profile = Profile.objects.get(user__id=user_id)

            if profile == follewers:
                raise CantFollowYourself

            if user_profile.check_following(profile):
                format_response = {
                    "status_code": status.HTTP_400_BAD_REQUEST,
                    "message": f"You are already following {profile.user.first_name} {profile.user.last_name}",
                }
                return Response(format_response, status=status.HTTP_400_BAD_REQUEST)

            user_profile.follow(profile)
            subject = "A new user is follows you"
            massage = f"Hi {profile.user.first_name}, {request.user.first_name} is now following you."
            from_email = DEFAULT_FROM_EMAIL
            recipient_list = [profile.user.email]
            send_mail(subject, massage, from_email, recipient_list)

            return Response({
                "status_code": status.HTTP_200_OK,
                "message": f"You are now following {profile.user.first_name} {profile.user.last_name}"
            }, status=status.HTTP_200_OK)
        except Profile.DoesNotExist:
            raise NotFound(
                detail="you cannot follow this user that does not exist")


class UnFollowAPIView(APIView):
    def post(self, request, user_id, format=None, *args, **kwargs):
        user_profile = request.user.profile
        profile = Profile.objects.get(user__id=user_id)

        if not user_profile.check_following(profile):
            format_response = {
                "status_code": status.HTTP_400_BAD_REQUEST,
                "message": f"You are not following {profile.user.first_name} {profile.user.last_name}",
            }
            return Response(format_response, status=status.HTTP_400_BAD_REQUEST)

        user_profile.unfollow(profile)
        return Response({
            "status_code": status.HTTP_200_OK,
            "message": f"You have unfollowed {profile.user.first_name} {profile.user.last_name}"
        }, status=status.HTTP_200_OK)
