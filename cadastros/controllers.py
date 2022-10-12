from typing import Any, Type

from .models import ComposicaoItem, Item, MedidaCaseira, Nutricional, RendimentoItem
from .utils import clean_text


def criar_item(
    descricao : str,
    medida_caseira : int, #nutricional

    ingrediente : bool = False,
    composto: bool = False,
    
    quantidade_porcao : float = 0.0,
    quantidade_embalagem : int = 1,
    quantidade_medida_caseira : float = 0.0,
    valor_energetico : float = 0.0,
    carboidrato : float = 0.0,
    acucar_total : float = 0.0,
    acucar_adicionado : float = 0.0,
    proteina : float = 0.0,
    gordura_total : float = 0.0,
    gordura_saturada : float = 0.0,
    gordura_trans : float = 0.0,
    fibra_alimentar : float = 0.0,
    sodio : float = 0.0,

    quantidade_rendimento : float = 0.0,
    ingredientes : list[dict[str, Any]] = []
    ) -> tuple[bool, str, Type[Item] | None] :

    descricao = clean_text(descricao)

    item : Type[Item] = Item.objects.filter(descricao=descricao)
    if (item.exists()):
        item = item.first()
        return (False, f'Item já existe: [{item.id} - {item}]', None) 

    if composto:
        try:
            item : Type[Item] = Item(
                descricao=descricao,
                ingrediente=ingrediente,
                composto=composto)
            item.save()

            rendimento : tuple[bool, str, Type[RendimentoItem] | None] = criar_rendimento(item, quantidade_rendimento)
            if not rendimento[0]:
                return (False, rendimento[1], None)
            else:
                rendimento : Type[RendimentoItem] = rendimento[2]
            
            for ingrediente in ingredientes:
                ing_result : tuple[bool, str, Type[ComposicaoItem] | None] = criar_ingrediente(
                    produto_final = item,
                    ingrediente = ingrediente['ingrediente'],
                    quantidade_ingrediente = ingrediente['quantidade_ingrediente'],
                    acucar_adicional = ingrediente['acucar_adicional']
                )

                if not ing_result[0]:
                    return (False, ing_result[1], None)

            ingredientes : Type[ComposicaoItem] = ComposicaoItem.objects.filter(produto_final=item).all()

            rotulo_nutricional : dict[str, float] = {
                'valor_energetico' : 0.0,
                'carboidrato' : 0.0,
                'acucar_total' : 0.0,
                'acucar_adicionado' : 0.0,
                'proteina' : 0.0,
                'gordura_total' : 0.0,
                'gordura_saturada' : 0.0,
                'gordura_trans' : 0.0,
                'fibra_alimentar' : 0.0,
                'sodio' : 0.0
            }

            for i in ingredientes:
                _ingrediente : Type[Nutricional] = Nutricional.objects.get(item=i.ingrediente)
                rotulo_nutricional['carboidrato'] += (_ingrediente.carboidrato / _ingrediente.quantidade_porcao) * i.quantidade_ingrediente
                rotulo_nutricional['acucar_total'] += (_ingrediente.acucar_total / _ingrediente.quantidade_porcao) * i.quantidade_ingrediente
                rotulo_nutricional['proteina'] += (_ingrediente.proteina / _ingrediente.quantidade_porcao) * i.quantidade_ingrediente
                rotulo_nutricional['gordura_total'] += (_ingrediente.gordura_total / _ingrediente.quantidade_porcao) * i.quantidade_ingrediente
                rotulo_nutricional['gordura_saturada'] += (_ingrediente.gordura_saturada / _ingrediente.quantidade_porcao) * i.quantidade_ingrediente
                rotulo_nutricional['fibra_alimentar'] += (_ingrediente.fibra_alimentar / _ingrediente.quantidade_porcao) * i.quantidade_ingrediente
                rotulo_nutricional['sodio'] += (_ingrediente.sodio / _ingrediente.quantidade_porcao) * i.quantidade_ingrediente

                if i.acucar_adicional:
                    rotulo_nutricional['acucar_adicionado'] += (_ingrediente.acucar_total / _ingrediente.quantidade_porcao) * i.quantidade_ingrediente
                else:
                    rotulo_nutricional['acucar_adicionado'] += (_ingrediente.acucar_adicionado / _ingrediente.quantidade_porcao) * i.quantidade_ingrediente


            rotulo_nutricional['valor_energetico'] = (4 * (rotulo_nutricional['carboidrato'] + rotulo_nutricional['proteina'])) + (9 * rotulo_nutricional['gordura_total']) + (2 * rotulo_nutricional['fibra_alimentar'])
            
            nutricional : tuple[bool, str, Type[Nutricional]] = criar_nutricional(
                item = item,
                quantidade_porcao = quantidade_porcao,
                quantidade_embalagem = quantidade_embalagem,
                quantidade_medida_caseira = quantidade_medida_caseira,
                medida_caseira = medida_caseira,
                valor_energetico = (rotulo_nutricional['valor_energetico'] / rendimento.quantidade_rendimento) * quantidade_porcao,
                carboidrato = (rotulo_nutricional['carboidrato'] / rendimento.quantidade_rendimento) * quantidade_porcao,
                acucar_total = (rotulo_nutricional['acucar_total'] / rendimento.quantidade_rendimento) * quantidade_porcao,
                acucar_adicionado = (rotulo_nutricional['acucar_adicionado'] / rendimento.quantidade_rendimento) * quantidade_porcao,
                proteina = (rotulo_nutricional['proteina'] / rendimento.quantidade_rendimento) * quantidade_porcao,
                gordura_total = (rotulo_nutricional['gordura_total'] / rendimento.quantidade_rendimento) * quantidade_porcao,
                gordura_saturada = (rotulo_nutricional['gordura_saturada'] / rendimento.quantidade_rendimento) * quantidade_porcao,
                gordura_trans = (rotulo_nutricional['gordura_trans'] / rendimento.quantidade_rendimento) * quantidade_porcao,
                fibra_alimentar = (rotulo_nutricional['fibra_alimentar'] / rendimento.quantidade_rendimento) * quantidade_porcao,
                sodio = (rotulo_nutricional['sodio'] / rendimento.quantidade_rendimento) * quantidade_porcao
            )
            if nutricional[0]:
                return (True, 'Item criado com sucesso!', item)
            else:
                return (False, nutricional[1], None)

        except Exception as e:
            return (False, f'Não foi possível criar o item. [{str(e)}]', None)
    else:
        try:
            item : Type[Item] = Item(descricao=descricao, ingrediente=ingrediente)
            item.save()
            
            nutricional : tuple[bool, str, Type[Nutricional]] = criar_nutricional(
                item = item,
                quantidade_porcao = quantidade_porcao,
                quantidade_embalagem = quantidade_embalagem,
                quantidade_medida_caseira = quantidade_medida_caseira,
                medida_caseira = medida_caseira,
                valor_energetico = valor_energetico,
                carboidrato = carboidrato,
                acucar_total = acucar_total,
                acucar_adicionado = acucar_adicionado,
                proteina = proteina,
                gordura_total = gordura_total,
                gordura_saturada = gordura_saturada,
                gordura_trans = gordura_trans,
                fibra_alimentar = fibra_alimentar,
                sodio = sodio
            )
            if nutricional[0]:
                return (True, 'Item criado com sucesso!', item)
            else:
                return (False, nutricional[1], None)
        except Exception as e:
            return (False, f'Não foi possível criar o item. [{str(e)}]', None)

def criar_nutricional(
    item : Type[Item],
    medida_caseira = int,
    quantidade_porcao : int = 0,
    quantidade_embalagem : int = 1,
    quantidade_medida_caseira : float = 0,
    valor_energetico : float = 0,
    carboidrato : float = 0,
    acucar_total : float = 0,
    acucar_adicionado : float = 0,
    proteina : float = 0,
    gordura_total : float = 0,
    gordura_saturada : float = 0,
    gordura_trans : float = 0,
    fibra_alimentar : float = 0,
    sodio : float = 0    
    ) -> tuple[bool, str, Type[Nutricional] | None] :

    try:
        medida_caseira : Type[MedidaCaseira] = MedidaCaseira.objects.get(id=medida_caseira)

        nutricional : Type[Nutricional] = Nutricional(
                item = item,
                quantidade_porcao = quantidade_porcao,
                quantidade_embalagem = quantidade_embalagem,
                quantidade_medida_caseira = quantidade_medida_caseira,
                medida_caseira = medida_caseira,
                valor_energetico = valor_energetico,
                carboidrato = carboidrato,
                acucar_total = acucar_total,
                acucar_adicionado = acucar_adicionado,
                proteina = proteina,
                gordura_total = gordura_total,
                gordura_saturada = gordura_saturada,
                gordura_trans = gordura_trans,
                fibra_alimentar = fibra_alimentar,
                sodio = sodio
            )
        nutricional.save()

        return (True, 'Nutricional criado com sucesso!', nutricional)
    except Exception as e:
        return (False, f'Não foi possível criar o Nutricional. [{str(e)}]', None)


def criar_medida_caseira(descricao : str) -> tuple[bool, str, Type[MedidaCaseira] | None] :
    descricao = clean_text(descricao)

    medida_caseira : Type[MedidaCaseira] = MedidaCaseira.objects.filter(descricao=descricao)
    if (medida_caseira.exists()):
        medida_caseira = medida_caseira.first()
        return (False, f'Medida Caseira já existe: [{medida_caseira.id} - {medida_caseira}]')

    try:
        medida_caseira = MedidaCaseira(descricao=descricao)
        medida_caseira.save()
        return (True, 'Medida Caseira criada com sucesso!', medida_caseira)
    except Exception as e:
        return (False, f'Não foi possível criar a Medida Caseira. [{str(e)}]', None)

def criar_rendimento(
    item: Type[Item],
    quantidade: float) -> tuple[bool, str, Type[RendimentoItem] | None] :
    try:
        rendimento : Type[RendimentoItem] = RendimentoItem(
            item=item,
            quantidade_rendimento=quantidade)
        rendimento.save()
        return (True, 'Rendimento criado com sucesso!', rendimento)
    except Exception as e:
        return (False, f'Não foi possível criar o Rendimento. [{str(e)}]', None)
        
def criar_ingrediente(
    produto_final : Type[Item],
    ingrediente : str,
    quantidade_ingrediente : float,
    acucar_adicional : bool) -> tuple[bool, str, Type[ComposicaoItem] | None] :
    
    ingrediente = Item.objects.get(descricao=ingrediente)


    item_composicao : Type[ComposicaoItem] = ComposicaoItem.objects.filter(produto_final=produto_final, ingrediente=ingrediente)
    if (item_composicao.exists()):
        return (False, 'Item da Composição já existe.', None)    

    try:
        item_composicao = ComposicaoItem(
            produto_final=produto_final,
            ingrediente=ingrediente,
            quantidade_ingrediente=quantidade_ingrediente,
            acucar_adicional=acucar_adicional
            )
        item_composicao.save()
        return (True, 'Item da Composição criado com sucesso!', item_composicao)
    except Exception as e:
        return (False, f'Não foi possível criar o Item da Composição. [{str(e)}]', None)    
