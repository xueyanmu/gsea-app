# Generated by Django 3.1.6 on 2021-04-10 05:00

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('genes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Geneset',
            fields=[
                ('id', models.CharField(max_length=200, primary_key=True, serialize=False)),
                ('size', models.IntegerField(default=0)),
                ('grouping', models.CharField(max_length=64)),
                ('organisms', models.OneToOneField(to='organisms.Organism', on_delete=models.CASCADE)),
                ('function_database', models.CharField(max_length=200)),
                ('genes', models.ManyToManyField(to='genes.Gene')),
            ],
            options={
                'ordering': ['id'],
            },
        ),
    ]