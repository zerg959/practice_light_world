import pytest
from users.models import User, Role

@pytest.mark.django_db

class TestUserModel:
    """Юнит-тесты модели User."""

    def test_create_user_with_default_role(self, user):
        """Созданный пользователь получает статус 'user'."""
        assert user.role == Role.USER


    def test_user_saved_to_db(self, user, fake):
        """Созданный пользователь доступен в базе по имени."""
        found = User.objects.filter(username=user.username).first()
        assert found is not None
        assert found.email == user.email
        assert found.pk == user.pk
