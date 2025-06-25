import pytest
from django.contrib.auth import get_user_model
from shorturls.models import ShortURL, UTM

User = get_user_model()

@pytest.mark.django_db
def test_create_shorturl():
    user = User.objects.create_user(email="test@example.com", password="secure123")
    short = ShortURL.objects.create(url="https://example.com", short_url="abc123", created_by=user)
    assert short.url == "https://example.com"
    assert short.short_url == "abc123"
    assert str(short) == "abc123 → https://example.com"
    assert short.created_by == user
    assert short.is_active is True
    assert short.password is None
    # 測試反向關聯
    assert user.short_urls.count() == 1
    assert user.short_urls.first() == short
    print("✅ 短網址建立測試成功！")

@pytest.mark.django_db
def test_create_utm():
    user = User.objects.create_user(email="test@example.com", password="secure123")
    short = ShortURL.objects.create(url="https://example.com", short_url="abc123", created_by=user)
    utm = UTM.objects.create(
        short_url=short,
        source="google",
        medium="cpc",
        campaign="spring_sale"
    )
    assert utm.short_url == short
    assert utm.source == "google"
    assert utm.term is None  # 預設可為 None
    assert str(utm) == f"UTM for {short}: google, cpc, spring_sale"
    # 測試反向關聯
    assert short.utm.count() == 1
    assert short.utm.first() == utm
    print("✅ UTM建立測試成功！")
