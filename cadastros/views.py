import json
from typing import Any, Type

from django.shortcuts import render
from django.http import JsonResponse

from .models import Item, MedidaCaseira, Nutricional
from .controllers import criar_item, criar_medida_caseira
from .utils import true_or_false

# Create your views here.

def cadastro_medida_caseira(request):
    context = {
        'msg' : ''
    }

    if request.method == 'POST':
        descricao = request.POST.get('descricao').strip().upper()
        result = criar_medida_caseira(
            descricao=descricao
            )
        context['msg'] = result[1]
        return render(request, 'cadastro_medida_caseira.html', context=context)
    else:
        return render(request, 'cadastro_medida_caseira.html', context=context)

def cadastro_item(request):
    ingredientes : Type[Item] = Item.objects.filter(ingrediente=True).order_by('descricao')
    medidas_caseiras : Type[MedidaCaseira] = MedidaCaseira.objects.all().order_by('descricao')
    context : dict[str] = {
        'ingredientes': ingredientes,
        'medidas_caseiras' : medidas_caseiras,
        'msg': ''
    }
    if request.method == 'POST':
        try:
            data_post : json = json.loads(request.body.decode("utf-8"))
            composto : bool = data_post['composto']
        except:
            composto  : str = request.POST.get('radioFormula')
            composto : bool = true_or_false(composto)

        if not composto:
            descricao : str = request.POST.get('produto')
            ingrediente  : str = request.POST.get('ingrediente')
            
            ingrediente : bool = true_or_false(ingrediente)

            quantidade_porcao : float = float(request.POST.get('quantidadePorcao'))
            quantidade_embalagem : int = int(request.POST.get('quantidadeEmbalagem'))
            quantidade_medida_caseira : float = float(request.POST.get('quantidadeCaseira'))
            medida_caseira : int = int(request.POST.get('medidaCaseira'))

            valor_energetico : float = float(request.POST.get('valorEnergetico'))
            carboidrato : float = float(request.POST.get('carboidrato'))
            acucar_total : float = float(request.POST.get('acucarTotal'))
            acucar_adicionado : float = float(request.POST.get('acucarAdicionado'))
            proteina : float = float(request.POST.get('proteina'))
            gordura_total : float = float(request.POST.get('gorduraTotal'))
            gordura_saturada : float = float(request.POST.get('gorduraSaturada'))
            gordura_trans : float = float(request.POST.get('gorduraTrans'))
            fibra_alimentar : float = float(request.POST.get('fibraAlimentar'))
            sodio : float = float(request.POST.get('sodio'))

            result : tuple[bool, str, Type[Item] | None] = criar_item(
            descricao=descricao,
            medida_caseira=medida_caseira,
            ingrediente=ingrediente,
            composto=composto,
            quantidade_porcao=quantidade_porcao,
            quantidade_embalagem=quantidade_embalagem,
            quantidade_medida_caseira=quantidade_medida_caseira,
            valor_energetico=valor_energetico,
            carboidrato=carboidrato,
            acucar_total=acucar_total,
            acucar_adicionado=acucar_adicionado,
            proteina=proteina,
            gordura_total=gordura_total,
            gordura_saturada=gordura_saturada,
            gordura_trans=gordura_trans,
            fibra_alimentar=fibra_alimentar,
            sodio=sodio
        )
            context['msg'] = result[1]    
            #render POST
            return render(request, 'cadastro_item.html', context)
        else: #Se item composto
            descricao : str = data_post['produto']
            composto : bool = composto
            ingrediente : bool = data_post['ingrediente']
            quantidade_porcao : float = float(data_post['quantidade_porcao'])
            quantidade_embalagem : int = int(data_post['quantidade_embalagem'])
            quantidade_medida_caseira : float = float(data_post['quantidade_medida_caseira'])
            medida_caseira : int = int(data_post['medida_caseira'])
            quantidade_rendimento : float = float(data_post['quantidade_rendimento'])
            ingredientes : dict[str,Any]= data_post['ingredientes']

            lista_ingredientes : list[dict] = []
            for ing in ingredientes:
                lista_ingredientes.append({
                    'ingrediente': ing['descricao'],
                    'quantidade_ingrediente': ing['qtd'],
                    'acucar_adicional': ing['acucarAdicionado']

                })

            result : tuple[bool, str, Type[Item] | None] = criar_item(
                descricao=descricao,
                medida_caseira=medida_caseira,
                ingrediente=ingrediente,
                composto=composto,
                quantidade_porcao=quantidade_porcao,
                quantidade_embalagem=quantidade_embalagem,
                quantidade_medida_caseira=quantidade_medida_caseira,
                quantidade_rendimento=quantidade_rendimento,
                ingredientes=lista_ingredientes
            )

            data : dict = {
                'cod': result[0],
                'msg': result[1],
            }

            return JsonResponse(data)
    #render GET
    return render(request, 'cadastro_item.html', context)

def exibe_rotulo(request, id_item):
    item : Type[Item] = Item.objects.filter(id=id_item)

    if (item.exists()):
        item = item.first()
    else:
        #item nao existe
        pass
    
    rotulo : Type[Nutricional] = item.nutricional
    rotulo_percent : dict[str,float] = {}

    rotulo_percent['valor_energetico'] = (rotulo.valor_energetico / rotulo.quantidade_porcao) * .1
    rotulo_percent['carboidrato'] = (rotulo.carboidrato / rotulo.quantidade_porcao) * .1
    rotulo_percent['acucar_total'] = (rotulo.acucar_total / rotulo.quantidade_porcao) * .1
    rotulo_percent['acucar_adicionado'] = (rotulo.acucar_adicionado / rotulo.quantidade_porcao) * .1
    rotulo_percent['proteina'] = (rotulo.proteina / rotulo.quantidade_porcao) * .1
    rotulo_percent['gordura_total'] = (rotulo.gordura_total / rotulo.quantidade_porcao) * .1
    rotulo_percent['gordura_saturada'] = (rotulo.gordura_saturada / rotulo.quantidade_porcao) * .1
    rotulo_percent['gordura_trans'] = (rotulo.gordura_trans / rotulo.quantidade_porcao) * .1
    rotulo_percent['fibra_alimentar'] = (rotulo.fibra_alimentar / rotulo.quantidade_porcao) * .1
    rotulo_percent['sodio'] = (rotulo.sodio / rotulo.quantidade_porcao) * .1

    context : dict[str] = {
        'item' : item,
        'rotulo' : item.nutricional,
        'rotulo_percent': rotulo_percent
    }
    return render(request, 'exibe_rotulo.html', context)
