# Generated by Django 4.0.8 on 2022-12-27 10:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('lifecycles', '0003_remove_lifecycle_owner_id_and_more'),
        ('mlregister', '0003_remove_mlrelease_version_mlrelease_experiment_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='mlregister',
            name='lifecycle',
            field=models.ForeignKey(default='6ac89bfb-6179-417b-99b7-ebbeab5adf85', on_delete=django.db.models.deletion.CASCADE, related_name='mlregister', to='lifecycles.lifecycle'),
            preserve_default=False,
        ),
    ]
