from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _


class AdminUserManager(BaseUserManager):

    def create_user(self, email, firstname, lastname, dob, gender, hiredate, password, **extra_fields):
        email = self.normalize_email(email)
        email = email.lower()
        firstname = firstname.upper()
        lastname = lastname.upper()
        dob = dob
        gender = gender
        hiredate = hiredate

        user = self.model(email=email, firstname=firstname, lastname=lastname, dob=dob, gender=gender, hiredate=hiredate, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, firstname, lastname, dob, gender, hiredate, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))
        return self.create_user(email, firstname, lastname, dob, gender, hiredate, password, **extra_fields)
