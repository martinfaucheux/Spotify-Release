from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    # def create_superuser(self, email, name="", password=None, **extra_fields):
    #     if not email:
    #         raise ValueError("User must have an email")
    #     # if not password:
    #     #     raise ValueError("User must have a password")
    #     # if not name:
    #     #     raise ValueError("User must have a name")

    #     user = self.model(email=self.normalize_email(email))
    #     user.name = name
    #     user.set_password(password)
    #     user.admin = True
    #     user.staff = True
    #     user.active = True
    #     user.save(using=self._db)
    #     return user

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError("The given email must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)

    def get_by_natural_key(self, email):
        """ Ensure that email is case insensitive when logging in """
        return self.get(email__iexact=email)
