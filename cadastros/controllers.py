from typing import Any, Type

from django.db import transaction

from .models import ComposicaoItem, Item, MedidaCaseira, Nutricional, RendimentoItem
from .utils import clean_text


def criar_item(
    descricao : str,
    medida_caseira : int, #nutricional
    quantidade_porcao : float,

    ingrediente : bool = False,
    composto: bool = False,
    quantidade_embalagem : int = 1,
    quantidade_medida_caseira : float = 1,
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

    descricao : str = clean_text(descricao)

    item : Type[Item] = Item.objects.filter(descricao=descricao)
    if (item.exists()):
        item = item.first()
        return (False, f'Item já existe: [{item.id} - {item}]', None) 

    with transaction.atomic():
        try:
            if composto:
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
                
                nutricional : tuple[bool, str, Type[Nutricional]] = criar_nutricional(
                    item = item,
                    quantidade_porcao = quantidade_porcao,
                    quantidade_embalagem = quantidade_embalagem,
                    quantidade_medida_caseira = quantidade_medida_caseira,
                    medida_caseira = medida_caseira
                )

            else:
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
    medida_caseira : int,
    quantidade_porcao : float,
    quantidade_embalagem : int,
    quantidade_medida_caseira : float,
    **rotulo    
    ) -> tuple[bool, str, Type[Nutricional] | None] :

    try:
        medida_caseira : Type[MedidaCaseira] = MedidaCaseira.objects.get(id=medida_caseira)
    except Exception as e:
        return (False, f'Não foi possível criar o Nutricional. [{str(e)}]', None)

    with transaction.atomic():
        try:
            nutricional = Nutricional.objects.filter(item=item)

            if nutricional.exists():
                nutricional = nutricional.first()
                nutricional.medida_caseira = medida_caseira
            else:
                nutricional = Nutricional(
                    item=item,
                    medida_caseira=medida_caseira
                )

            nutricional.quantidade_porcao = quantidade_porcao
            nutricional.quantidade_embalagem = quantidade_embalagem
            nutricional.quantidade_medida_caseira = quantidade_medida_caseira
        
            if item.composto:
                ingredientes = ComposicaoItem.objects.filter(produto_final=item)

                for i in ingredientes:
                    _ingrediente : Type[Nutricional] = Nutricional.objects.get(item=i.ingrediente)
                    nutricional.carboidrato += (_ingrediente.carboidrato / _ingrediente.quantidade_porcao) * i.quantidade_ingrediente
                    nutricional.acucar_total += (_ingrediente.acucar_total / _ingrediente.quantidade_porcao) * i.quantidade_ingrediente
                    nutricional.proteina += (_ingrediente.proteina / _ingrediente.quantidade_porcao) * i.quantidade_ingrediente
                    nutricional.gordura_total += (_ingrediente.gordura_total / _ingrediente.quantidade_porcao) * i.quantidade_ingrediente
                    nutricional.gordura_saturada += (_ingrediente.gordura_saturada / _ingrediente.quantidade_porcao) * i.quantidade_ingrediente
                    nutricional.fibra_alimentar += (_ingrediente.fibra_alimentar / _ingrediente.quantidade_porcao) * i.quantidade_ingrediente
                    nutricional.sodio += (_ingrediente.sodio / _ingrediente.quantidade_porcao) * i.quantidade_ingrediente

                    if i.acucar_adicional:
                        nutricional.acucar_adicionado += (_ingrediente.acucar_total / _ingrediente.quantidade_porcao) * i.quantidade_ingrediente
                    else:
                        nutricional.acucar_adicionado += (_ingrediente.acucar_adicionado / _ingrediente.quantidade_porcao) * i.quantidade_ingrediente

                rendimento = RendimentoItem.objects.get(item=item).quantidade_rendimento

                nutricional.carboidrato = nutricional.carboidrato / rendimento * nutricional.quantidade_porcao
                nutricional.acucar_total = nutricional.acucar_total / rendimento * nutricional.quantidade_porcao
                nutricional.acucar_adicionado = nutricional.acucar_adicionado / rendimento * nutricional.quantidade_porcao
                nutricional.proteina = nutricional.proteina / rendimento * nutricional.quantidade_porcao
                nutricional.gordura_total = nutricional.gordura_total / rendimento * nutricional.quantidade_porcao
                nutricional.gordura_saturada = nutricional.gordura_saturada / rendimento * nutricional.quantidade_porcao
                nutricional.gordura_trans = nutricional.gordura_trans / rendimento * nutricional.quantidade_porcao
                nutricional.fibra_alimentar = nutricional.fibra_alimentar / rendimento * nutricional.quantidade_porcao
                nutricional.sodio = nutricional.sodio / rendimento * nutricional.quantidade_porcao
                
                nutricional.valor_energetico = (4 * (nutricional.carboidrato + nutricional.proteina)) + (9 * nutricional.gordura_total) + (2 * nutricional.fibra_alimentar)

            else:
                nutricional.quantidade_porcao = quantidade_porcao
                nutricional.quantidade_embalagem = quantidade_embalagem
                nutricional.quantidade_medida_caseira = quantidade_medida_caseira
                nutricional.medida_caseira = medida_caseira
                nutricional.valor_energetico = rotulo['valor_energetico'] if rotulo['valor_energetico'] else 0
                nutricional.carboidrato = rotulo['carboidrato'] if rotulo['carboidrato'] else 0
                nutricional.acucar_total = rotulo['acucar_total'] if rotulo['acucar_total'] else 0
                nutricional.acucar_adicionado = rotulo['acucar_adicionado'] if rotulo['acucar_adicionado'] else 0
                nutricional.proteina = rotulo['proteina'] if rotulo['proteina'] else 0
                nutricional.gordura_total = rotulo['gordura_total'] if rotulo['gordura_total'] else 0
                nutricional.gordura_saturada = rotulo['gordura_saturada'] if rotulo['gordura_saturada'] else 0
                nutricional.gordura_trans = rotulo['gordura_trans'] if rotulo['gordura_trans'] else 0
                nutricional.fibra_alimentar = rotulo['fibra_alimentar'] if rotulo['fibra_alimentar'] else 0
                nutricional.sodio = rotulo['sodio'] if rotulo['sodio'] else 0

            tmp_acucar_adicionado : float = (nutricional.acucar_adicionado / quantidade_porcao) * .1
            if tmp_acucar_adicionado >= 15:
                nutricional.alto_acucar = True

            tmp_gordura_saturada  : float = (nutricional.gordura_saturada / quantidade_porcao) * .1
            if tmp_gordura_saturada >= 6:
                nutricional.alto_gordura = True

            tmp_sodio : float = (nutricional.sodio / quantidade_porcao) * .1
            if tmp_sodio >= 600:
                nutricional.alto_sodio = True
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


def editar_item(
    item : Type[Item],
    medida_caseira : int, #nutricional
    quantidade_porcao : float,

    ingrediente : bool = False,
    quantidade_embalagem : int = 1,
    quantidade_medida_caseira : float = 1,
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

    compoe_algum_item = ComposicaoItem.objects.filter(ingrediente=item).exists()
    if (not ingrediente) and compoe_algum_item:
        return (False, f'Não foi possível atualizar o item. Ele faz parte da composição de pelo menos um item.', None)

    with transaction.atomic():
        try:
            item.ingrediente = ingrediente
            item.save()

            if item.composto:

                if quantidade_rendimento > 0:
                    RendimentoItem.objects.filter(item=item).update(quantidade_rendimento=quantidade_rendimento)

                if len(ingredientes) > 0:
                    ComposicaoItem.objects.filter(produto_final=item).delete()

                    for ingrediente in ingredientes:
                        ing_result : tuple[bool, str, Type[ComposicaoItem] | None] = criar_ingrediente(
                            produto_final = item,
                            ingrediente = ingrediente['ingrediente'],
                            quantidade_ingrediente = ingrediente['quantidade_ingrediente'],
                            acucar_adicional = ingrediente['acucar_adicional']
                        )

                        if not ing_result[0]:
                            return (False, ing_result[1], None)
                
                nutricional : tuple[bool, str, Type[Nutricional]] = criar_nutricional(
                    item = item,
                    quantidade_porcao = quantidade_porcao,
                    quantidade_embalagem = quantidade_embalagem,
                    quantidade_medida_caseira = quantidade_medida_caseira,
                    medida_caseira = medida_caseira
                )

            else:
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
            
            if item.ingrediente:
                composicao_itens = ComposicaoItem.objects.filter(ingrediente=item)

                if composicao_itens.exists():
                    for composicao in composicao_itens:
                        _item = composicao.produto_final
                        _mc = _item.nutricional.medida_caseira.id

                        _ingredientes = []
                        _tmp_ingr = ComposicaoItem.objects.filter(produto_final = _item)
                        for i in _tmp_ingr:
                            _ingredientes.append({
                                'ingrediente' : i.ingrediente,
                                'quantidade_ingrediente' : i.quantidade_ingrediente,
                                'acucar_adicional' : i.acucar_adicional
                            })
                        editar_item(
                            item = _item,
                            medida_caseira = _mc, #nutricional
                            quantidade_porcao = _item.nutricional.quantidade_porcao,
                            ingrediente = _item.ingrediente,
                            quantidade_embalagem = _item.nutricional.quantidade_embalagem,
                            quantidade_medida_caseira = _item.nutricional.quantidade_medida_caseira,
                            quantidade_rendimento = _item.rendimentoitem.quantidade_rendimento,
                            ingredientes = _ingredientes
                            )
            

            if nutricional[0]:
                return (True, 'Item atualizado com sucesso!', item)
            else:
                return (False, nutricional[1], None)

        except Exception as e:
            return (False, f'Não foi possível atualizar o item. [{str(e)}]', None)



