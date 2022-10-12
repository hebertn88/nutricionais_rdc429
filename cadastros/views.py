import json
import pprint

from django.shortcuts import render
from django.http import HttpResponse

from nutricionais.settings  import BASE_DIR
from pathlib import Path

from .models import Item, MedidaCaseira
from .controllers import criar_item, criar_medida_caseira
from .utils import clean_text, true_or_false

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

def cadastro(request):
    ingredientes = Item.objects.filter(ingrediente=True).order_by('descricao')
    medidas_caseiras = MedidaCaseira.objects.all().order_by('descricao')
    context = {
        'ingredientes': ingredientes,
        'medidas_caseiras' : medidas_caseiras,
        'msg': ''
    }
    if request.method == 'POST':
        try:
            data_post = json.loads(request.body.decode("utf-8"))
            composto = data_post['composto']
            descricao = data_post['produto']
            ingrediente = data_post['ingrediente']
            quantidade_rendimento = data_post['rendimento']
            ingredientes = data_post['ingredientes']

            print(f'{descricao=}')
            print(f'{composto=}')
            print(f'{quantidade_rendimento=}')
            print(f'{ingrediente=}')
            print(f'{ingredientes=}')
            
        except Exception as e:
            descricao = request.POST.get('produto')
            composto = request.POST.get('radioFormula')
            ingrediente = request.POST.get('ingrediente')
            
            composto = true_or_false(composto)
            ingrediente = true_or_false(ingrediente)

        if not composto:
            quantidade_porcao = float(request.POST.get('quantidadePorcao')) / 1000
            quantidade_embalagem = int(request.POST.get('quantidadeEmbalagem'))
            quantidade_medida_caseira = float(request.POST.get('quantidadeCaseira'))
            medida_caseira = int(request.POST.get('medidaCaseira'))

            valor_energetico = float(request.POST.get('valorEnergetico'))
            carboidrato = float(request.POST.get('carboidrato'))
            acucar_total = float(request.POST.get('acucarTotal'))
            acucar_adicionado = float(request.POST.get('acucarAdicionado'))
            proteina = float(request.POST.get('proteina'))
            gordura_total = float(request.POST.get('gorduraTotal'))
            gordura_saturada = float(request.POST.get('gorduraSaturada'))
            gordura_trans = float(request.POST.get('gorduraTrans'))
            fibra_alimentar = float(request.POST.get('fibraAlimentar'))
            sodio = float(request.POST.get('sodio'))

            result = criar_item(
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
            return render(request, 'cadastro_simples.html', context)
        else: #Se item composto
            lista_ingredientes : list = []
            for ing in ingredientes:
                lista_ingredientes.append({
                    'ingrediente': ing['descricao'],
                    'quantidade_ingrediente': ing['qtd'],
                    'acucar_adicional': ing['acucarAdicionado']

                })
            '''

            descricao = data_post['produto']
            ingrediente = data_post['ingrediente']
            quantidade_rendimento = data_post['rendimento']
            ingredientes = data_post['ingredientes']


            pf = criar_item(
            descricao=descricao,
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
            '''

            return render(request, 'cadastro_simples.html', context)
    #render GET
    return render(request, 'cadastro_simples.html', context)

def cadastro_composto(request):
    ingredientes = Item.objects.filter(ingrediente=True).order_by('descricao')
    context = {
        'msg': '',
        'ingredientes': ingredientes
    }
    return render(request, 'cadastro_composto.html', context) 