from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('herbal', '0074_rename_notes_crf3_remarks_remove_crf3_other_comments'),
    ]

    operations = [
        migrations.CreateModel(
            name='CRF7',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),

                ('anxiety', models.CharField(max_length=50, blank=True)),
                ('cdate', models.DateField(null=True, blank=True)),
                ('fdate', models.DateField(null=True, blank=True)),
                ('mobility', models.CharField(max_length=50, blank=True)),
                ('pain', models.CharField(max_length=50, blank=True)),
                ('remarks', models.TextField(blank=True)),
                ('self_care', models.CharField(max_length=50, blank=True)),
                ('tdate', models.DateField(null=True, blank=True)),
                ('usual_active', models.CharField(max_length=50, blank=True)),

                ('cpersid', models.ForeignKey(
                    to='accounts.staffprofile',
                    null=True,
                    blank=True,
                    on_delete=django.db.models.deletion.SET_NULL
                )),
            ],
        ),
    ]