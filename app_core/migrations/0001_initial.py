# Generated by Django 2.2 on 2019-06-23 23:26

import autoslug.fields
import cities_light.abstract_models
import cities_light.validators
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('nombres', models.CharField(default='', max_length=30, verbose_name='Nombres')),
                ('apellidos', models.CharField(default='', max_length=30, verbose_name='Apellidos')),
                ('email', models.EmailField(default='', max_length=255, unique=True, verbose_name='Email')),
                ('genero', models.CharField(blank=True, choices=[('Masculino', 'Masculino'), ('Femenino', 'Femenino'), ('Otros', 'Otros')], default='', max_length=10, null=True, verbose_name='Genero')),
                ('id_restablecimiento', models.CharField(blank=True, default='', max_length=60, null=True, verbose_name='Id Recuperacion')),
                ('is_staff', models.BooleanField(default=True)),
                ('is_superuser', models.BooleanField(default=True)),
                ('password', models.CharField(default='', max_length=128, verbose_name='Password')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=200)),
                ('name_ascii', models.CharField(blank=True, db_index=True, max_length=200)),
                ('slug', autoslug.fields.AutoSlugField(editable=False, populate_from='name_ascii')),
                ('geoname_id', models.IntegerField(blank=True, null=True, unique=True)),
                ('alternate_names', models.TextField(blank=True, default='', null=True)),
                ('code2', models.CharField(blank=True, max_length=2, null=True, unique=True)),
                ('code3', models.CharField(blank=True, max_length=3, null=True, unique=True)),
                ('continent', models.CharField(choices=[('OC', 'Oceania'), ('EU', 'Europe'), ('AF', 'Africa'), ('NA', 'North America'), ('AN', 'Antarctica'), ('SA', 'South America'), ('AS', 'Asia')], db_index=True, max_length=2)),
                ('tld', models.CharField(blank=True, db_index=True, max_length=5)),
                ('phone', models.CharField(blank=True, max_length=20, null=True)),
            ],
            options={
                'verbose_name_plural': 'countries',
                'ordering': ['name'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='EgresadosUTP',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('DNI', models.CharField(default='', max_length=10, verbose_name='DNI')),
                ('nombres', models.CharField(default='', max_length=30, verbose_name='Nombres')),
                ('apellidos', models.CharField(default='', max_length=30, verbose_name='Apellidos')),
                ('email', models.EmailField(default='', max_length=255, unique=True, verbose_name='Email')),
            ],
        ),
        migrations.CreateModel(
            name='Interes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(default='', max_length=30, null=True, verbose_name='Nombre')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Fecha de edición')),
            ],
            options={
                'verbose_name': 'Interes',
                'verbose_name_plural': 'Interes',
                'ordering': ['-created'],
            },
        ),
        migrations.CreateModel(
            name='SuperUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('email', models.EmailField(default='', max_length=255, unique=True, verbose_name='Email')),
                ('password', models.CharField(default='', max_length=128, verbose_name='Password')),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=True)),
                ('is_superuser', models.BooleanField(default=True)),
                ('is_egresado', models.BooleanField(default=False)),
                ('is_administrador', models.BooleanField(default=False)),
                ('is_superusuario', models.BooleanField(default=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Egresado',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('Tipo_de_identificacion', models.CharField(default='Cédula de ciudadania', max_length=20, verbose_name='Identificacion')),
                ('DNI', models.CharField(default='', max_length=10, verbose_name='DNI')),
                ('activacion', models.BooleanField(default=False, null=True, verbose_name='Activacion')),
                ('fecha_nacimiento', models.DateField(blank=True, null=True, verbose_name='Fecha de nacimiento')),
                ('is_active', models.BooleanField(default=True)),
                ('is_egresado', models.BooleanField(default=True)),
                ('is_administrador', models.BooleanField(default=False)),
                ('is_superusuario', models.BooleanField(default=False)),
                ('validado', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'Egresado',
                'verbose_name_plural': 'Egresados',
            },
            bases=('app_core.user',),
        ),
        migrations.CreateModel(
            name='Region',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=200)),
                ('name_ascii', models.CharField(blank=True, db_index=True, max_length=200)),
                ('slug', autoslug.fields.AutoSlugField(editable=False, populate_from='name_ascii')),
                ('geoname_id', models.IntegerField(blank=True, null=True, unique=True)),
                ('alternate_names', models.TextField(blank=True, default='', null=True)),
                ('display_name', models.CharField(max_length=200)),
                ('geoname_code', models.CharField(blank=True, db_index=True, max_length=50, null=True)),
                ('country', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_core.Country')),
            ],
            options={
                'verbose_name': 'region/state',
                'verbose_name_plural': 'regions/states',
                'ordering': ['name'],
                'abstract': False,
                'unique_together': {('country', 'name'), ('country', 'slug')},
            },
        ),
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=200)),
                ('name_ascii', models.CharField(blank=True, db_index=True, max_length=200)),
                ('slug', autoslug.fields.AutoSlugField(editable=False, populate_from='name_ascii')),
                ('geoname_id', models.IntegerField(blank=True, null=True, unique=True)),
                ('alternate_names', models.TextField(blank=True, default='', null=True)),
                ('display_name', models.CharField(max_length=200)),
                ('search_names', cities_light.abstract_models.ToSearchTextField(blank=True, db_index=True, default='', max_length=4000)),
                ('latitude', models.DecimalField(blank=True, decimal_places=5, max_digits=8, null=True)),
                ('longitude', models.DecimalField(blank=True, decimal_places=5, max_digits=8, null=True)),
                ('population', models.BigIntegerField(blank=True, db_index=True, null=True)),
                ('feature_code', models.CharField(blank=True, db_index=True, max_length=10, null=True)),
                ('timezone', models.CharField(blank=True, db_index=True, max_length=40, null=True, validators=[cities_light.validators.timezone_validator])),
                ('country', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_core.Country')),
                ('region', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app_core.Region')),
            ],
            options={
                'verbose_name_plural': 'cities',
                'ordering': ['name'],
                'abstract': False,
                'unique_together': {('region', 'name'), ('region', 'slug')},
            },
        ),
        migrations.AddField(
            model_name='user',
            name='pais',
            field=models.ForeignKey(blank=True, default='', null=True, on_delete=django.db.models.deletion.CASCADE, to='app_core.City'),
        ),
        migrations.CreateModel(
            name='Intereses',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('interes', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_core.Interes')),
                ('egresado', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_core.Egresado')),
            ],
            options={
                'verbose_name': 'Intereses',
                'verbose_name_plural': 'Intereses',
            },
        ),
        migrations.CreateModel(
            name='Administrador',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('Tipo_de_identificacion', models.CharField(default='Cédula de ciudadania', max_length=20, verbose_name='ID')),
                ('DNI', models.CharField(default='', max_length=10, verbose_name='DNI')),
                ('telefono', models.IntegerField(blank=True, default='', null=True, verbose_name='Telefono')),
                ('direccion', models.CharField(max_length=30, verbose_name='Direccion')),
                ('is_active', models.BooleanField(default=True)),
                ('is_egresado', models.BooleanField(default=False)),
                ('is_administrador', models.BooleanField(default=True)),
                ('is_superusuario', models.BooleanField(default=False)),
                ('ciudad', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_core.City')),
            ],
            options={
                'verbose_name': 'Administrador',
                'verbose_name_plural': 'Administradores',
            },
            bases=('app_core.user',),
        ),
    ]