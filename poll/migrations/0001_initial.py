# Generated by Django 3.1 on 2020-08-16 11:13

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=128, null=True)),
                ('correct', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Block',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type_block', models.CharField(choices=[('PL', 'Опросник'), ('TS', 'Тест')], default='TS', max_length=2)),
                ('title', models.CharField(max_length=128)),
                ('description', models.TextField(blank=True)),
                ('question_count', models.SmallIntegerField(default=0)),
                ('date_begin', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Дата начала теста')),
                ('date_end', models.DateTimeField(blank=True, null=True, verbose_name='Дата окончания теста')),
                ('available', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=264)),
                ('image', models.ImageField(blank=True, null=True, upload_to='questions_image/')),
                ('type_variant', models.CharField(choices=[('RB', 'Радиокнопка'), ('CB', 'Чекбокс')], default='RB', max_length=2)),
            ],
        ),
        migrations.CreateModel(
            name='QuestionInBlock',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('weight', models.SmallIntegerField(default=0)),
                ('block', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='block', to='poll.block')),
                ('question', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='question', to='poll.question')),
            ],
        ),
        migrations.CreateModel(
            name='UserAnswer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answers', models.ManyToManyField(related_name='answer', to='poll.Answer')),
                ('question_in_block', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='question_in_block', to='poll.questioninblock')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='BlockResult',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('result', models.SmallIntegerField(default=0)),
                ('is_full', models.BooleanField(default=False)),
                ('is_completed', models.BooleanField(default=False)),
                ('block', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='result', to='poll.block')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='block_result', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='answer',
            name='question',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='answer_in_question', to='poll.question'),
        ),
    ]
