from django.db import models
from django.conf import settings


class ShortURL(models.Model):
    url = models.URLField(verbose_name="原始網址")
    short_url = models.CharField(max_length=20, unique=True, verbose_name="短網址代碼")
    is_active = models.BooleanField(default=True, verbose_name="是否啟用")
    password = models.CharField(max_length=128, blank=True, null=True, verbose_name="密碼（可選）")
    remarks = models.TextField(blank=True, null=True, verbose_name="備註說明")

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="建立時間")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新時間")

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="short_urls",
        verbose_name="建立者"
    )
    def __str__(self):
        return f"{self.short_url} → {self.url}"

class UTM(models.Model):
    short_url = models.ForeignKey(ShortURL, on_delete=models.CASCADE, related_name='utm')
    source = models.CharField(max_length=100)
    medium = models.CharField(max_length=100)
    campaign = models.CharField(max_length=100)
    term = models.CharField(max_length=100, blank=True, null=True)
    content = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'UTM for {self.short_url}: {self.source}, {self.medium}, {self.campaign}'