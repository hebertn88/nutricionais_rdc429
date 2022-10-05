# Generated by Django 4.1.1 on 2022-09-22 17:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descricao', models.CharField(max_length=150, unique=True, verbose_name='Descrição')),
                ('ingrediente', models.BooleanField(default=False, verbose_name='Ingrediente')),
                ('composto', models.BooleanField(default=False, verbose_name='Composto')),
            ],
        ),
        migrations.CreateModel(
            name='MedidaCaseira',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descricao', models.CharField(max_length=100, unique=True, verbose_name='Descrição')),
            ],
        ),
        migrations.CreateModel(
            name='RendimentoItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantidade_rendimento', models.DecimalField(decimal_places=2, default=0, max_digits=11, verbose_name='Quantidade da Medida Caseira')),
                ('item', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='cadastros.item')),
            ],
        ),
        migrations.CreateModel(
            name='Nutricional',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantidade_porcao', models.IntegerField(default=0, verbose_name='Porção')),
                ('quantidade_embalagem', models.IntegerField(default=1, verbose_name='Quantidade por Embalagem')),
                ('quantidade_medida_caseira', models.DecimalField(decimal_places=2, default=0, max_digits=11, verbose_name='Quantidade da Medida Caseira')),
                ('valor_energetico', models.DecimalField(decimal_places=2, default=0, max_digits=11, verbose_name='Valor Energético')),
                ('carboidrato', models.DecimalField(decimal_places=2, default=0, max_digits=11, verbose_name='Carboidratos')),
                ('acucar_total', models.DecimalField(decimal_places=2, default=0, max_digits=11, verbose_name='Açúcares Totais')),
                ('acucar_adicionado', models.DecimalField(decimal_places=2, default=0, max_digits=11, verbose_name='Açúcares Adicionados')),
                ('proteina', models.DecimalField(decimal_places=2, default=0, max_digits=11, verbose_name='Proteinas')),
                ('gordura_total', models.DecimalField(decimal_places=2, default=0, max_digits=11, verbose_name='Gorduras Totais')),
                ('gordura_saturada', models.DecimalField(decimal_places=2, default=0, max_digits=11, verbose_name='Gorduras Saturadas')),
                ('gordura_trans', models.DecimalField(decimal_places=2, default=0, max_digits=11, verbose_name='Gorduras Trans')),
                ('fibra_alimentar', models.DecimalField(decimal_places=2, default=0, max_digits=11, verbose_name='Fibra Alimentar')),
                ('sodio', models.DecimalField(decimal_places=2, default=0, max_digits=11, verbose_name='Sódio')),
                ('item', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='cadastros.item')),
                ('medida_caseira', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='cadastros.medidacaseira')),
            ],
        ),
        migrations.CreateModel(
            name='ComposicaoItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantidade_ingrediente', models.DecimalField(decimal_places=2, default=0, max_digits=11, verbose_name='Quantidade do Ingrediente')),
                ('acucar_adicional', models.BooleanField(default=False, verbose_name='Açúcar Adicional')),
                ('ingrediente', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='composicao_ingrediente', to='cadastros.item')),
                ('produto_final', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='composicao_prod_final', to='cadastros.item')),
            ],
        ),
    ]
