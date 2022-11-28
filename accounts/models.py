from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill
# Create your models here.
# 이름 비밀번호 설명 주소 생년월일

class User(AbstractUser):
    profile_pic = ProcessedImageField(  # 프로필사진
        upload_to="profile/%Y%m%d/",
        null=True,
        processors=[ResizeToFill(360, 360)],
        format="JPEG",
        options={"quality": 80},
    )
    GENDER_CHOICES = (
        ("M", "남자"),
        ("F", "여자"),
    )
    gender = models.CharField(  # 성별
        max_length=2,
        choices=GENDER_CHOICES,
    )
    address = models.CharField(max_length=50)  # 주소
    address_detail = models.CharField(max_length=40, null=True)  # 상세주소
    birth = models.DateTimeField(default=timezone.now)  # 나이
    follwings = models.ManyToManyField('self',symmetrical=False, related_name='followers')
    
    
    @property
    def get_photo_url(self):

        if self.profile_pic:
            return self.profile_pic.url
        return None
    