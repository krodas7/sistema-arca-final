from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0029_merge_20260309_2343'),
    ]

    operations = [
        migrations.AddField(
            model_name='asistencia',
            name='hora_salida_almuerzo',
            field=models.TimeField(blank=True, null=True, verbose_name='Salida a Almuerzo'),
        ),
        migrations.AddField(
            model_name='asistencia',
            name='hora_entrada_almuerzo',
            field=models.TimeField(blank=True, null=True, verbose_name='Retorno de Almuerzo'),
        ),
        migrations.AddField(
            model_name='asistencia',
            name='horas_laboradas',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True, verbose_name='Horas Laboradas'),
        ),
    ]
