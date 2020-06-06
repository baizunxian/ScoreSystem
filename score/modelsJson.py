from rest_framework import serializers
from score.models import *


class BonusSerializers(serializers.ModelSerializer):
    """
    序列号 bonus
    """
    create_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    update_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    start_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    end_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    teacher_name = serializers.CharField(source='Tuser.TName')
    teacher_college = serializers.CharField(source='Tuser.TCollege.college_name')

    class Meta:
        model = Bonus
        # 需要返回的字段
        fields = '__all__'
