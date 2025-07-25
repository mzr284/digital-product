from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager, send_mail
from django.utils.translation import gettext_lazy as _
from django.db import models
from django.core.validators import RegexValidator
import random



class UserManager(BaseUserManager):

    use_in_migrations = True
    def _create_user(self, username, phone_number, email, password, is_staff, is_superuser, **extra_fields):
        if not username:
            raise ValueError("You must give your username")
        email = self.normalize_email(email)
        user = self.model(phone_number=phone_number,
                          username=username, email=email,
                          is_staff=is_staff, is_active=True,
                          is_superuser=is_superuser,
                          data_joined=timezone.now(), **extra_fields
                          )

        if not extra_fields.get("no_password"):
            user.set_password(password)

        user.save(using=self._db)
        return user



    def create_user(self, username=None, phone_number=None, email=None, password=None, is_staff=None, **extra_field):
        if username is None:
            if email:
                username = email.split("@", 1)[0]
            if phone_number:
                username = random.choice('abcdefghigklmnoprstuvwxqyz') + str(phone_number)[-7:]
            while User.objects.filter(username=username).exists():
                username += str(random.randint(10, 99))
            if is_staff == None:
                is_staff = False
        return self._create_user(username, phone_number, email, password, is_staff, False, **extra_field)

    def create_superuser(self, username, phone_number, email, password, **extra_field):
        return self._create_user(username, phone_number, email, password, True, True, **extra_field)



class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(_("username"), max_length=20, unique=True,
                                help_text="Enter the 5 character or number at least",
                                validators=[
                                    RegexValidator(r'^[a-zA-Z][a-zA-Z0-9_\.]+$',
                                    _("Enter The valid user name must be contain the letters,"
                                      " numbers, and under lines"), "Invalid")
                                ],
                                error_messages={
                                    "unique": _("A user with this username already exist, Please enter the other username"),
                                },
                                )
    first_name = models.CharField(_("first name"), max_length=30, blank=True)
    last_name = models.CharField(_("last name"), max_length=30, blank=True)
    email = models.CharField(_("Email"),max_length=50 , unique=True, blank=True, null=True)
    phone_number = models.BigIntegerField(_("Phone_number"), unique=True, blank=True, null=True,
                                          validators=[
                                              RegexValidator(r'^989[0-3,9]\d{8}$',
                                              _("Enter The valid phone number"),
                                              "invalid",)
                                          ],
                                          error_messages={"unique": _("A user with this phone number already exist")},
                                          )
    is_staff = models.BooleanField(_("staff status"), default=False,
                                   help_text=_("Designed for recognize the user can be staff and can log as a admin into the site or not"),
                                   )
    is_active = models.BooleanField(_("active"), default=True, help_text=_("Designed for find oud the user is active or not"))
    data_joined = models.DateTimeField(_("data of join"), default=timezone.now())
    last_seen = models.DateTimeField(_("last seen date"), null=True)

    objects = UserManager()

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["phone_number", "email"]

    class Meta:
        db_table = "users"
        verbose_name = _("user")
        verbose_name_plural = _("users")

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def save(self, *args, **kwargs):
        if self.email is not None and self.email.strip() == '':
            self.email = None
        super().save(*args, **kwargs)


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nick_name = models.CharField(_('nick name'), max_length=50)
    avatar = models.ImageField(_('avatar'), blank=True)
    birthday = models.DateField(_("birthday date"), blank=True, null=True)
    gender = models.BooleanField(_("gender"), help_text=_("female is False, male is True"), null=True, default=True)

    class Meta:
        db_table = "user_profiles"
        verbose_name = _("user_profile")
        verbose_name_plural = _("user_profiles")


class Device(models.Model):
    WEB = 1
    IOS = 1
    ANDROID = 1
    DEVICE_TYPE_CHOICE = (
        (WEB, 'web'),
        (IOS, 'ios'),
        (ANDROID, 'android'),
    )

    user = models.ForeignKey(User, related_name='devices', on_delete=models.CASCADE)
    device_uuid = models.UUIDField(_("device uuid"), null=True)
    last_login = models.DateTimeField(_("last login date"), null=True)
    device_type = models.PositiveIntegerField(choices=DEVICE_TYPE_CHOICE, default=ANDROID)
    device_version = models.CharField(_("device model"),max_length=20 , blank=True)
    created_time = models.DateTimeField(_("created time"),auto_now_add=True , blank=True)

    class Meta:
        db_table = "devices"
        verbose_name = _("device")
        verbose_name_plural = _("devices")

