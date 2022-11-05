from typing import Type
from django.test import TestCase
from cadastros.controllers import criar_item, criar_medida_caseira, criar_rendimento, editar_item
from cadastros.models import MedidaCaseira, Nutricional

class Teste(TestCase):
    """
    def teste_criar_medida_caseira(self):
        result =  criar_medida_caseira('Medida Caseira Teste')
        assert result[0] == True
    def teste_criar_item(self):
        *_, medida_caseira = criar_medida_caseira('MedCaseiraTeste')

        '''
        result = criar_item(
            descricao="item teste",
            medida_caseira=medida_caseira.id,
            quantidade_porcao=0.05
        )
        '''

        result = criar_item(
            descricao='Mistura Pao Frances',
            medida_caseira=medida_caseira.id,
            ingrediente=True,
            composto=False,
            quantidade_porcao=0.05,
            quantidade_embalagem=1,
            quantidade_medida_caseira=1,
            valor_energetico=180,
            carboidrato=38,
            acucar_total=0.5,
            acucar_adicionado=0,
            proteina=8,
            gordura_total=0,
            gordura_saturada=0,
            gordura_trans=0,
            fibra_alimentar=1,
            sodio=390
        )

        print()
        print()
        print(70 * '-')
        print()
        print(result)
        rotulo : Type[Nutricional] = Nutricional.objects.get(item=result[2])
        print(f'{rotulo.item.descricao=}')
        print(f'{rotulo.valor_energetico=}')
        print(f'{rotulo.carboidrato=}')
        print(f'{rotulo.acucar_total=}')
        print(f'{rotulo.acucar_adicionado=}')
        print(f'{rotulo.proteina=}')
        print(f'{rotulo.gordura_total=}')
        print(f'{rotulo.gordura_saturada=}')
        print(f'{rotulo.gordura_trans=}')
        print(f'{rotulo.fibra_alimentar=}')
        print(f'{rotulo.sodio=}')
        print(70 * '-')
        print()

        assert result[0] == True

    def teste_falha_ao_criar_item_duplicado(self):
        *_, medida_caseira = criar_medida_caseira('MedCaseiraTeste')
        criar_item(
            "item teste",
            medida_caseira.id,
            0.05
        )

        result = criar_item(
            "item teste",
            medida_caseira.id,
            0.10
        )

        assert result[0] == False
    
    def teste_criar_rendimento(self):
        mc = criar_medida_caseira('medida')
        item = criar_item(
            'teste_rendimento',
            mc[2].id,
            0.05
        )

        result = criar_rendimento(
            item[2],
            50.5
        )

        assert result[0] == True


    def teste_criar_item_composto(self):
        *_, medida_caseira = criar_medida_caseira('Minha Medida Caseira')

        ing_01 = criar_item(
            descricao='Mistura Pao Frances',
            medida_caseira=medida_caseira.id,
            ingrediente=True,
            composto=False,
            quantidade_porcao=0.05,
            quantidade_embalagem=1,
            quantidade_medida_caseira=1,
            valor_energetico=180,
            carboidrato=38,
            acucar_total=0.5,
            acucar_adicionado=0,
            proteina=8,
            gordura_total=0,
            gordura_saturada=0,
            gordura_trans=0,
            fibra_alimentar=1,
            sodio=390
        )

        ing_02 = criar_item(
            descricao='Fermento',
            medida_caseira=medida_caseira.id,
            ingrediente=True,
            composto=False,
            quantidade_porcao=0.1,
            quantidade_embalagem=1,
            quantidade_medida_caseira=1,
            valor_energetico=96,
            carboidrato=2.4,
            acucar_total=0,
            acucar_adicionado=0,
            proteina=17.6,
            gordura_total=1.8,
            gordura_saturada=0.4,
            gordura_trans=0,
            fibra_alimentar=9.6,
            sodio=49
        )

        ing_03 = criar_item(
            descricao='Melhorador',
            medida_caseira=medida_caseira.id,
            ingrediente=True,
            composto=False,
            quantidade_porcao=0.1,
            quantidade_embalagem=1,
            quantidade_medida_caseira=1,
            valor_energetico=305,
            carboidrato=67,
            acucar_total=0,
            acucar_adicionado=0,
            proteina=0,
            gordura_total=4,
            gordura_saturada=0,
            gordura_trans=0,
            fibra_alimentar=0,
            sodio=0
        )

        pf = criar_item(
            descricao='Pao Frances',
            medida_caseira=medida_caseira.id,
            ingrediente=True,
            composto=True,
            quantidade_porcao=0.05,
            quantidade_rendimento=30.75,
            ingredientes= [
                {'ingrediente' : ing_01[2].descricao,
                'quantidade_ingrediente': 25,
                'acucar_adicional' : False},
                {'ingrediente' : ing_02[2].descricao,
                'quantidade_ingrediente': 0.75,
                'acucar_adicional' : False},
                {'ingrediente' : ing_03[2].descricao,
                'quantidade_ingrediente': 0.2,
                'acucar_adicional' : False},
                ]
        )

        print()
        print()
        print(70 * '-')
        print(pf)
        rotulo : Type[Nutricional] = Nutricional.objects.get(item=pf[2])
        print(f'{pf[2].descricao}')
        print(f'{rotulo.valor_energetico=}')
        print(f'{rotulo.carboidrato=}')
        print(f'{rotulo.acucar_total=}')
        print(f'{rotulo.acucar_adicionado=}')
        print(f'{rotulo.proteina=}')
        print(f'{rotulo.gordura_total=}')
        print(f'{rotulo.gordura_saturada=}')
        print(f'{rotulo.gordura_trans=}')
        print(f'{rotulo.fibra_alimentar=}')
        print(f'{rotulo.sodio=}')
        print(70 * '-')
        print()
        
        assert pf[0] == True

    
    def teste_editar_item_simples(self):
        *_, medida_caseira = criar_medida_caseira('MedCaseiraTeste')

        *_, item = criar_item(
                descricao='Mistura Pao Frances',
                medida_caseira=medida_caseira.id,
                ingrediente=False,
                composto=False,
                quantidade_porcao=0.05,
                quantidade_embalagem=1,
                quantidade_medida_caseira=1,
                valor_energetico=180,
                carboidrato=38,
                acucar_total=0.5,
                acucar_adicionado=0,
                proteina=8,
                gordura_total=0,
                gordura_saturada=0,
                gordura_trans=0,
                fibra_alimentar=1,
                sodio=390
            )

        print()
        print()
        print(70 * '-')
        print()
        print('ANTES')
        rotulo : Type[Nutricional] = Nutricional.objects.get(item=item)
        print(f'{rotulo.item.descricao=}')
        print(f'{rotulo.item.ingrediente=}')
        print(f'{rotulo.item.composto=}')
        print(f'{rotulo.valor_energetico=}')
        print(f'{rotulo.carboidrato=}')
        print(f'{rotulo.acucar_total=}')
        print(f'{rotulo.acucar_adicionado=}')
        print(f'{rotulo.proteina=}')
        print(f'{rotulo.gordura_total=}')
        print(f'{rotulo.gordura_saturada=}')
        print(f'{rotulo.gordura_trans=}')
        print(f'{rotulo.fibra_alimentar=}')
        print(f'{rotulo.sodio=}')
        print(70 * '-')
        print()
        
        result = editar_item(
            item=item,
            medida_caseira=medida_caseira.id,
            quantidade_porcao=99,
            ingrediente=True,
            quantidade_embalagem=99,
            quantidade_medida_caseira=99,
            valor_energetico=99,
            carboidrato=99,
            acucar_total=99,
            acucar_adicionado=99,
            proteina=99,
            gordura_total=99,
            gordura_saturada=99,
            gordura_trans=99,
            fibra_alimentar=99,
            sodio=99
        )

        print()
        print()
        print(70 * '-')
        print()
        print('DEPOIS')
        print(result)
        rotulo : Type[Nutricional] = Nutricional.objects.get(item=result[2])
        print(f'{rotulo.item.descricao=}')
        print(f'{rotulo.item.ingrediente=}')
        print(f'{rotulo.item.composto=}')
        print(f'{rotulo.valor_energetico=}')
        print(f'{rotulo.carboidrato=}')
        print(f'{rotulo.acucar_total=}')
        print(f'{rotulo.acucar_adicionado=}')
        print(f'{rotulo.proteina=}')
        print(f'{rotulo.gordura_total=}')
        print(f'{rotulo.gordura_saturada=}')
        print(f'{rotulo.gordura_trans=}')
        print(f'{rotulo.fibra_alimentar=}')
        print(f'{rotulo.sodio=}')
        print(70 * '-')
        print()

        assert result[0] == True


    def teste_editar_item_composto(self):
        *_, medida_caseira = criar_medida_caseira('Minha Medida Caseira')

        ing_01 = criar_item(
            descricao='Mistura Pao Frances',
            medida_caseira=medida_caseira.id,
            ingrediente=True,
            composto=False,
            quantidade_porcao=0.05,
            quantidade_embalagem=1,
            quantidade_medida_caseira=1,
            valor_energetico=180,
            carboidrato=38,
            acucar_total=0.5,
            acucar_adicionado=0,
            proteina=8,
            gordura_total=0,
            gordura_saturada=0,
            gordura_trans=0,
            fibra_alimentar=1,
            sodio=390
        )

        ing_02 = criar_item(
            descricao='Fermento',
            medida_caseira=medida_caseira.id,
            ingrediente=True,
            composto=False,
            quantidade_porcao=0.1,
            quantidade_embalagem=1,
            quantidade_medida_caseira=1,
            valor_energetico=96,
            carboidrato=2.4,
            acucar_total=0,
            acucar_adicionado=0,
            proteina=17.6,
            gordura_total=1.8,
            gordura_saturada=0.4,
            gordura_trans=0,
            fibra_alimentar=9.6,
            sodio=49
        )

        ing_03 = criar_item(
            descricao='Melhorador',
            medida_caseira=medida_caseira.id,
            ingrediente=True,
            composto=False,
            quantidade_porcao=0.1,
            quantidade_embalagem=1,
            quantidade_medida_caseira=1,
            valor_energetico=305,
            carboidrato=67,
            acucar_total=0,
            acucar_adicionado=0,
            proteina=0,
            gordura_total=4,
            gordura_saturada=0,
            gordura_trans=0,
            fibra_alimentar=0,
            sodio=0
        )

        *_, pf = criar_item(
            descricao='Pao Frances',
            medida_caseira=medida_caseira.id,
            ingrediente=False,
            composto=True,
            quantidade_porcao=0.05,
            quantidade_rendimento=30.75,
            ingredientes= [
                {'ingrediente' : ing_01[2].descricao,
                'quantidade_ingrediente': 25,
                'acucar_adicional' : False},
                {'ingrediente' : ing_02[2].descricao,
                'quantidade_ingrediente': 0.75,
                'acucar_adicional' : False},
                {'ingrediente' : ing_03[2].descricao,
                'quantidade_ingrediente': 0.2,
                'acucar_adicional' : False},
                ]
        )

        print()
        print()
        print(70 * '-')
        print()
        print('ANTES')
        rotulo : Type[Nutricional] = Nutricional.objects.get(item=pf)
        print(f'{rotulo.item.descricao=}')
        print(f'{rotulo.item.ingrediente=}')
        print(f'{rotulo.item.composto=}')
        print(f'{rotulo.valor_energetico=}')
        print(f'{rotulo.carboidrato=}')
        print(f'{rotulo.acucar_total=}')
        print(f'{rotulo.acucar_adicionado=}')
        print(f'{rotulo.proteina=}')
        print(f'{rotulo.gordura_total=}')
        print(f'{rotulo.gordura_saturada=}')
        print(f'{rotulo.gordura_trans=}')
        print(f'{rotulo.fibra_alimentar=}')
        print(f'{rotulo.sodio=}')
        print(70 * '-')
        print()
        
        result = editar_item(
            item=pf,
            medida_caseira=medida_caseira.id,
            quantidade_porcao=.05,
            ingrediente=True,
            quantidade_embalagem=99,
            quantidade_medida_caseira=99,
            quantidade_rendimento=28,
            ingredientes=[
                {
                    'ingrediente' : ing_01[2].descricao,
                    'quantidade_ingrediente': 25,
                    'acucar_adicional' : False   
                }
            ]
        )

        print()
        print()
        print(70 * '-')
        print()
        print('DEPOIS')
        print(result)
        rotulo : Type[Nutricional] = Nutricional.objects.get(item=result[2])
        print(f'{rotulo.item.descricao=}')
        print(f'{rotulo.item.ingrediente=}')
        print(f'{rotulo.item.composto=}')
        print(f'{rotulo.valor_energetico=}')
        print(f'{rotulo.carboidrato=}')
        print(f'{rotulo.acucar_total=}')
        print(f'{rotulo.acucar_adicionado=}')
        print(f'{rotulo.proteina=}')
        print(f'{rotulo.gordura_total=}')
        print(f'{rotulo.gordura_saturada=}')
        print(f'{rotulo.gordura_trans=}')
        print(f'{rotulo.fibra_alimentar=}')
        print(f'{rotulo.sodio=}')
        print(70 * '-')
        print()

        assert result[0] == True
"""

    def teste_editar_item_composto(self):
        *_, medida_caseira = criar_medida_caseira('Minha Medida Caseira')

        ing_01 = criar_item(
            descricao='Mistura Pao Frances',
            medida_caseira=medida_caseira.id,
            ingrediente=True,
            composto=False,
            quantidade_porcao=0.05,
            quantidade_embalagem=1,
            quantidade_medida_caseira=1,
            valor_energetico=180,
            carboidrato=38,
            acucar_total=0.5,
            acucar_adicionado=0,
            proteina=8,
            gordura_total=0,
            gordura_saturada=0,
            gordura_trans=0,
            fibra_alimentar=1,
            sodio=390
        )

        ing_02 = criar_item(
            descricao='Fermento',
            medida_caseira=medida_caseira.id,
            ingrediente=True,
            composto=False,
            quantidade_porcao=0.1,
            quantidade_embalagem=1,
            quantidade_medida_caseira=1,
            valor_energetico=96,
            carboidrato=2.4,
            acucar_total=0,
            acucar_adicionado=0,
            proteina=17.6,
            gordura_total=1.8,
            gordura_saturada=0.4,
            gordura_trans=0,
            fibra_alimentar=9.6,
            sodio=49
        )

        ing_03 = criar_item(
            descricao='Melhorador',
            medida_caseira=medida_caseira.id,
            ingrediente=True,
            composto=False,
            quantidade_porcao=0.1,
            quantidade_embalagem=1,
            quantidade_medida_caseira=1,
            valor_energetico=305,
            carboidrato=67,
            acucar_total=0,
            acucar_adicionado=0,
            proteina=0,
            gordura_total=4,
            gordura_saturada=0,
            gordura_trans=0,
            fibra_alimentar=0,
            sodio=0
        )

        *_, pf = criar_item(
            descricao='Pao Frances',
            medida_caseira=medida_caseira.id,
            ingrediente=False,
            composto=True,
            quantidade_porcao=0.05,
            quantidade_rendimento=30.75,
            ingredientes= [
                {'ingrediente' : ing_01[2].descricao,
                'quantidade_ingrediente': 25,
                'acucar_adicional' : False},
                {'ingrediente' : ing_02[2].descricao,
                'quantidade_ingrediente': 0.75,
                'acucar_adicional' : False},
                {'ingrediente' : ing_03[2].descricao,
                'quantidade_ingrediente': 0.2,
                'acucar_adicional' : False},
                ]
        )

        *_, pf2 = criar_item(
            descricao='PAO2',
            medida_caseira=medida_caseira.id,
            ingrediente=False,
            composto=True,
            quantidade_porcao=0.05,
            quantidade_rendimento=0.5,
            ingredientes= [
                {
                    'ingrediente' : pf.descricao,
                    'quantidade_ingrediente': 1,
                    'acucar_adicional' : False
                },
            ]
        )

        print()
        print()
        print(70 * '-')
        print()
        print('PRODUTO FINAL 2')
        rotulo : Type[Nutricional] = Nutricional.objects.get(item=pf2)
        print(f'{rotulo.item.descricao=}')
        print(f'{rotulo.item.ingrediente=}')
        print(f'{rotulo.item.composto=}')
        print(f'{rotulo.valor_energetico=}')
        print(f'{rotulo.carboidrato=}')
        print(f'{rotulo.acucar_total=}')
        print(f'{rotulo.acucar_adicionado=}')
        print(f'{rotulo.proteina=}')
        print(f'{rotulo.gordura_total=}')
        print(f'{rotulo.gordura_saturada=}')
        print(f'{rotulo.gordura_trans=}')
        print(f'{rotulo.fibra_alimentar=}')
        print(f'{rotulo.sodio=}')
        print(70 * '-')
        print()

        print()
        print()
        print(70 * '-')
        print()
        print('ANTES')
        rotulo : Type[Nutricional] = Nutricional.objects.get(item=pf)
        print(f'{rotulo.item.descricao=}')
        print(f'{rotulo.item.ingrediente=}')
        print(f'{rotulo.item.composto=}')
        print(f'{rotulo.valor_energetico=}')
        print(f'{rotulo.carboidrato=}')
        print(f'{rotulo.acucar_total=}')
        print(f'{rotulo.acucar_adicionado=}')
        print(f'{rotulo.proteina=}')
        print(f'{rotulo.gordura_total=}')
        print(f'{rotulo.gordura_saturada=}')
        print(f'{rotulo.gordura_trans=}')
        print(f'{rotulo.fibra_alimentar=}')
        print(f'{rotulo.sodio=}')
        print(70 * '-')
        print()
        
        result = editar_item(
            item=pf,
            medida_caseira=medida_caseira.id,
            quantidade_porcao=.05,
            ingrediente=True,
            quantidade_embalagem=99,
            quantidade_medida_caseira=99,
            quantidade_rendimento=28,
            ingredientes=[
                {
                    'ingrediente' : ing_01[2].descricao,
                    'quantidade_ingrediente': 25,
                    'acucar_adicional' : False   
                }
            ]
        )

        print()
        print()
        print(70 * '-')
        print()
        print('DEPOIS')
        print(result)
        rotulo : Type[Nutricional] = Nutricional.objects.get(item=result[2])
        print(f'{rotulo.item.descricao=}')
        print(f'{rotulo.item.ingrediente=}')
        print(f'{rotulo.item.composto=}')
        print(f'{rotulo.valor_energetico=}')
        print(f'{rotulo.carboidrato=}')
        print(f'{rotulo.acucar_total=}')
        print(f'{rotulo.acucar_adicionado=}')
        print(f'{rotulo.proteina=}')
        print(f'{rotulo.gordura_total=}')
        print(f'{rotulo.gordura_saturada=}')
        print(f'{rotulo.gordura_trans=}')
        print(f'{rotulo.fibra_alimentar=}')
        print(f'{rotulo.sodio=}')
        print(70 * '-')
        print()

        print()
        print()
        print(70 * '-')
        print()
        print('DEPOIS')
        print(result)
        rotulo : Type[Nutricional] = Nutricional.objects.get(item=pf2)
        print(f'{rotulo.item.descricao=}')
        print(f'{rotulo.item.ingrediente=}')
        print(f'{rotulo.item.composto=}')
        print(f'{rotulo.valor_energetico=}')
        print(f'{rotulo.carboidrato=}')
        print(f'{rotulo.acucar_total=}')
        print(f'{rotulo.acucar_adicionado=}')
        print(f'{rotulo.proteina=}')
        print(f'{rotulo.gordura_total=}')
        print(f'{rotulo.gordura_saturada=}')
        print(f'{rotulo.gordura_trans=}')
        print(f'{rotulo.fibra_alimentar=}')
        print(f'{rotulo.sodio=}')
        print(70 * '-')
        print()

        assert result[0] == True