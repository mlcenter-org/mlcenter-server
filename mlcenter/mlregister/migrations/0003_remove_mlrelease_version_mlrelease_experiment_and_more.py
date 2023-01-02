# Generated by Django 4.0.8 on 2022-12-27 10:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('experiments', '0001_initial'),
        ('mlregister', '0002_remove_mlregister_experiment'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mlrelease',
            name='version',
        ),
        migrations.AddField(
            model_name='mlrelease',
            name='experiment',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='experiments', to='experiments.experiment'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='mlrelease',
            name='mlregister',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='mlregister', to='mlregister.mlregister'),
        ),
        migrations.DeleteModel(
            name='MLDeploymentLifecycle',
        ),
    ]
