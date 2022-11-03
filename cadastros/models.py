from django.db import models

# Create your models here.

class Item(models.Model):
    #produtos, ingredientes
    descricao = models.CharField('Descrição', max_length=150, unique=True)
    ingrediente = models.BooleanField('Ingrediente', default=False)
    composto = models.BooleanField('Composto', default=False)
    
    def __str__(self):
        return self.descricao

class RendimentoItem(models.Model):
    item = models.OneToOneField(Item, on_delete=models.CASCADE)
    quantidade_rendimento = models.FloatField('Quantidade da Medida Caseira', default=0.0)

class ComposicaoItem(models.Model):
    produto_final = models.ForeignKey(Item, on_delete=models.CASCADE, related_name="composicao_prod_final")
    ingrediente = models.ForeignKey(Item, on_delete=models.PROTECT, related_name="composicao_ingrediente")
    quantidade_ingrediente = models.FloatField('Quantidade do Ingrediente', default=0.0)
    acucar_adicional = models.BooleanField('Açúcar Adicional', default=False)

class MedidaCaseira(models.Model):
    descricao = models.CharField('Descrição', max_length=100, unique=True)

    def __str__(self):
        return self.descricao

class Nutricional(models.Model):
    item = models.OneToOneField(Item, on_delete=models.CASCADE)
    quantidade_porcao = models.FloatField('Porção', default=0.0)
    quantidade_embalagem = models.IntegerField('Quantidade por Embalagem', default=1)
    quantidade_medida_caseira = models.FloatField('Quantidade da Medida Caseira', default=0.0)
    medida_caseira = models.ForeignKey(MedidaCaseira, on_delete=models.PROTECT)
    valor_energetico = models.FloatField('Valor Energético', default=0.0)
    carboidrato = models.FloatField('Carboidratos', default=0.0)
    acucar_total = models.FloatField('Açúcares Totais', default=0.0)
    acucar_adicionado = models.FloatField('Açúcares Adicionados', default=0.0)
    proteina = models.FloatField('Proteinas', default=0.0)
    gordura_total = models.FloatField('Gorduras Totais', default=0.0)
    gordura_saturada = models.FloatField('Gorduras Saturadas', default=0.0)
    gordura_trans = models.FloatField('Gorduras Trans', default=0.0)
    fibra_alimentar = models.FloatField('Fibra Alimentar', default=0.0)
    sodio = models.FloatField('Sódio', default=0.0)
    alto_acucar = models.BooleanField('Alto Açúcar Adicionado', default=False)
    alto_gordura = models.BooleanField('Alto Gordura Saturada', default=False)
    alto_sodio = models.BooleanField('Alto Sódio', default=False)

    def __str__(self):
        return self.item.descricao
