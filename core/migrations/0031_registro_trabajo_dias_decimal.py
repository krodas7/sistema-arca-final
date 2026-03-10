from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0030_asistencia_horario_completo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='registrotrabajo',
            name='dias_trabajados',
            field=models.DecimalField(
                decimal_places=1,
                max_digits=5,
                verbose_name='Días trabajados',
                help_text='Número de días trabajados en este período (acepta medios días: 0.5, 1.5, etc.)'
            ),
        ),
    ]
