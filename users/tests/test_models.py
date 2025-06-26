import pytest
from django.contrib.auth import get_user_model
from django.db import IntegrityError

User = get_user_model()

@pytest.mark.django_db
def test_create_user_success():
    user = User.objects.create_user(email="test@example.com", password="secure123")
    assert user.email == "test@example.com"
    assert user.check_password("secure123")
    assert user.is_active
    assert not user.is_staff
    assert not user.is_superuser
    print("✅ 建立使用者測試成功！")


@pytest.mark.django_db
def test_create_superuser_success():
    admin = User.objects.create_superuser(email="admin@example.com", password="admin123")
    assert admin.is_staff
    assert admin.is_superuser
    print("✅ 建立管理員測試成功！")
    


@pytest.mark.django_db
def test_create_user_without_email_fail():
    with pytest.raises(ValueError):
        User.objects.create_user(email=None, password="123")
    print("✅ Email必填測試成功！")

@pytest.mark.django_db
def test_user_email_unique():
    User.objects.create_user(email="unique@example.com", password="a")
    with pytest.raises(IntegrityError):
        User.objects.create_user(email="unique@example.com", password="b")
    print("✅ Email唯一值測試成功！")