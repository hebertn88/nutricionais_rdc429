from pydoc import describe
from django.shortcuts import render
from django.http import HttpResponse

from cadastros.models import MedidaCaseira
from .controllers import criar_item, criar_medida_caseira

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
    medidas_caseiras = MedidaCaseira.objects.all().order_by('descricao')
    context = {
        'medidas_caseiras' : medidas_caseiras,
        'msg': ''
    }
    if request.method == 'POST':
        descricao = request.POST.get('produto').strip().upper()
        composto = request.POST.get('radioComposicao')
        ingrediente = request.POST.get('ingrediente')

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

        match composto:
            case 'True':
                composto = True
            case _:
                composto = False

        match ingrediente:
            case 'True':
                ingrediente = True
            case _:
                ingrediente = False
        
        if not composto:
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
    #render GET
    return render(request, 'cadastro_simples.html', context)

