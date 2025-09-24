from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField
from django_countries.fields import CountryField
from core_apps.common.models import TimeStampedModel

User = get_user_model()


class Profile(TimeStampedModel):
    class Gender(models.TextChoices):
        MALE = "M", _("Male"),
        FEMALE = "F", _("Female"),
        OTHER = "O", _("Other"),
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="profile")
    phone_number = PhoneNumberField(verbose_name=_("phone Number"),
                                    max_length=30, default="+23401927310246")
    about_me = models.TextField(verbose_name=_(
        "about Me"), max_length=500, blank=True, default="Say something about yourself")
    gender = models.CharField(
        verbose_name=_("gender"),
        choices=Gender.choices, default=Gender.OTHER, max_length=20
    )
    country = CountryField(verbose_name=_("Country"),
                           default="VN", blank=False, null=False)
    city = models.CharField(verbose_name=_("city"), max_length=180, blank=True)
    profile_photo = models.ImageField(
        verbose_name=_("profile Photo"), default="/profile_default.png"
    )
    twitter_handle = models.CharField(
        verbose_name=_("twitter Handle"), max_length=20, blank=True
    )
    followers = models.ManyToManyField(
        "self", symmetrical=False, related_name="following", blank=True
    )

    def __str__(self):
        return f"{self.user.first_name}'s profile"

    def follow(sefl, profile):
        sefl.followers.add(profile)
        
    def unfollow(self, profile):
        self.followers.remove(profile)

    def check_following(self, profile):
        return self.followers.filter(pk=profile.pkid).exists()