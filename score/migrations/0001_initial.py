# Generated by Django 2.0.3 on 2020-04-14 20:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AdminUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('admin_name', models.CharField(max_length=255, verbose_name='用户名')),
                ('admin_pwd', models.CharField(max_length=255, verbose_name='密码')),
            ],
            options={
                'verbose_name': '管理员',
                'db_table': 'AdminUser',
            },
        ),
        migrations.CreateModel(
            name='Application',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('school_year', models.CharField(max_length=255, verbose_name='学年')),
                ('year_shift', models.CharField(max_length=255, verbose_name='年班')),
                ('credit_and_GPA', models.FloatField(max_length=255, verbose_name='学分和绩点')),
                ('dormitory_standard', models.CharField(max_length=255, verbose_name='宿舍不达标次数')),
                ('volunteer_hours', models.FloatField(max_length=255, verbose_name='志愿者小时数')),
                ('comprehensive_results', models.FloatField(max_length=255, verbose_name='综合成绩')),
                ('activity_quantification', models.FloatField(max_length=255, verbose_name='活动量化')),
                ('research_project', models.TextField(max_length=255, verbose_name='科研项目')),
                ('remarks', models.TextField(max_length=255, verbose_name='申请理由')),
                ('approval_remarks', models.TextField(max_length=255, null=True, verbose_name='审核备注')),
                ('country_image', models.ImageField(blank=True, null=True, upload_to='country_image', verbose_name='国家奖')),
                ('province_image', models.ImageField(blank=True, null=True, upload_to='province_image', verbose_name='省奖')),
                ('school_image', models.ImageField(blank=True, null=True, upload_to='school_image', verbose_name='校奖')),
                ('country_fraction', models.IntegerField(null=True, verbose_name='国家奖赋值分数')),
                ('province_fraction', models.IntegerField(null=True, verbose_name='省奖赋值分数')),
                ('school_fraction', models.IntegerField(null=True, verbose_name='校奖赋值分数')),
                ('application_state', models.IntegerField(default=0, verbose_name='申请状态')),
            ],
            options={
                'verbose_name': '申请表',
                'db_table': 'Application',
            },
        ),
        migrations.CreateModel(
            name='Bonus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('bonus_name', models.CharField(max_length=255, verbose_name='奖项名称')),
                ('credit_and_GPA', models.FloatField(max_length=255, verbose_name='学分和绩点')),
                ('dormitory_standard', models.CharField(max_length=255, verbose_name='宿舍不达标次数')),
                ('volunteer_hours', models.FloatField(max_length=255, verbose_name='志愿者小时数')),
                ('credit', models.FloatField(max_length=255, verbose_name='学分')),
                ('start_time', models.DateTimeField(max_length=255, verbose_name='开始时间')),
                ('end_time', models.DateTimeField(max_length=255, verbose_name='结束时间')),
                ('bonus_state', models.IntegerField(default=0, verbose_name='状态')),
                ('bonus_type', models.CharField(max_length=255, verbose_name='奖金类型')),
            ],
            options={
                'verbose_name': '奖学金设置表',
                'db_table': 'Bonus',
            },
        ),
        migrations.CreateModel(
            name='College',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('college_name', models.CharField(max_length=255, verbose_name='学院名')),
            ],
            options={
                'verbose_name': '学院表',
                'db_table': 'College',
            },
        ),
        migrations.CreateModel(
            name='Major',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('major_name', models.CharField(max_length=255, verbose_name='专业名')),
                ('college', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='score.College', verbose_name='学院id')),
            ],
            options={
                'verbose_name': '专业表',
                'db_table': 'Major',
            },
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('SName', models.CharField(max_length=255, null=True, verbose_name='用户名称')),
                ('Student_id', models.IntegerField(verbose_name='学号')),
                ('SPwd', models.CharField(max_length=255, verbose_name='密码')),
                ('SSex', models.CharField(max_length=255, verbose_name='用户性别')),
                ('SPhoneNumber', models.CharField(max_length=255, verbose_name='手机号码')),
                ('SIDCard', models.CharField(max_length=255, verbose_name='身份证号')),
                ('SCollege', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='score.College', verbose_name='学院')),
                ('SMajor', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='score.Major', verbose_name='专业')),
            ],
            options={
                'verbose_name': '学生表',
                'db_table': 'Student',
            },
        ),
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('TName', models.CharField(max_length=255, null=True, verbose_name='用户名称')),
                ('TStaff_number', models.IntegerField(verbose_name='职工号')),
                ('TMajor', models.IntegerField(null=True, verbose_name='老师专业')),
                ('TPwd', models.CharField(max_length=255, verbose_name='密码')),
                ('TSex', models.CharField(max_length=255, verbose_name='用户性别')),
                ('TPhoneNumber', models.CharField(max_length=255, verbose_name='手机号码')),
                ('TIDCard', models.CharField(max_length=255, verbose_name='身份证号')),
                ('TCollege', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='score.College', verbose_name='老师学院')),
            ],
            options={
                'verbose_name': '老师表',
                'db_table': 'Teacher',
            },
        ),
        migrations.AddField(
            model_name='bonus',
            name='Tuser',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='score.Teacher', verbose_name='发布人'),
        ),
        migrations.AddField(
            model_name='application',
            name='Suser',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='score.Student', verbose_name='申请人'),
        ),
        migrations.AddField(
            model_name='application',
            name='Tuser',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='score.Teacher', verbose_name='审核人'),
        ),
        migrations.AddField(
            model_name='application',
            name='bonus',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='score.Bonus', verbose_name='申请项目'),
        ),
        migrations.AddField(
            model_name='application',
            name='college',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='score.College', verbose_name='学院'),
        ),
        migrations.AddField(
            model_name='application',
            name='major',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='score.Major', verbose_name='专业'),
        ),
    ]
