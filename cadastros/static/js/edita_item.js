const formItem = document.getElementById('formItem');
const sectionSimples = document.getElementById('sectionSimples');
const sectionComposto = document.getElementById('sectionComposto');
const elEnviar = document.getElementById('enviar');

// Adiciona listener aos radios formula
const radiosFormula = document.getElementsByName('radioFormula'); 
const elSepFinalForm = document.getElementById('sepFinalSection');

// Desabilita se nao estiver preenchido requisitos
formItem.addEventListener('change', formListener);
formItem.addEventListener('keyup', formListener);

let listaIngredientes = [];

if (radiosFormula[1].checked) {

    // Botao Adicionar Item composto
    const elAdicionarItem = document.getElementById('adicionarItem');
    const elTBody = document.getElementById('tBody');
    
    const elTrs = elTBody.querySelectorAll("tr");
    
    for (let i = 0; i < elTrs.length - 1; i++) {
        let descIngrediente = elTrs[i].children[0].innerText;

        const acucarAdicionado = descIngrediente.endsWith(' Açúcar');
        
        descIngrediente = descIngrediente.replace(' Açúcar', '');
        
        const qtdUtilizada = parseFloat(elTrs[i].children[1].innerText);

        const btn = elTrs[i].children[2].children[0];
        btn.addEventListener('click', removeRowTable);
        
        listaIngredientes.push({
            descricao : descIngrediente,
            qtd : qtdUtilizada,
            acucarAdicionado : acucarAdicionado
        });
    }
    // Adicionar item composicao
    elAdicionarItem.addEventListener('click', ()=>{
        const elSelIngrediente = document.getElementById('selIngrediente');
        const elQtdUtilizada = document.getElementById('quantidadeIngrediente');
        const elAcucarAdicional = document.getElementById('acucarAdicional');
    
        // Verifica se descricao esta entre opcoes
        const elOptIngredientes = document.getElementsByClassName('optIngredientes')
        let ingredienteExiste = false;
    
        for (let i=0; i<elOptIngredientes.length; i++) {
            if (elSelIngrediente.value === elOptIngredientes[i].value) {
                ingredienteExiste = true;
                break;
            };
        }

    // Verifica se ingrediente ja foi incluido
    let ingredienteNaLista = listaIngredientes.findIndex(i => i.descricao === elSelIngrediente.value);
    
    if (ingredienteExiste && ingredienteNaLista === -1 ) {
        const elRowVazio = document.getElementById('rowVazio');
        if (elRowVazio.style.display == '') {
            elRowVazio.style.display = 'none';
        }
        
        const elTr = document.createElement('tr');
        
        const elTdDescricao = document.createElement('td');
        elTdDescricao.classList.add('p-3');
        elTdDescricao.innerText = elSelIngrediente.value;
    
        if (elAcucarAdicional.checked) {
            elTdDescricao.innerHTML += ' <span class="badge rounded-pill text-bg-primary">Açúcar</span>';
        }
        
        const elTdQuantidade = document.createElement('td');
        elTdQuantidade.classList.add('p-3');
        elTdQuantidade.innerText = parseFloat(elQtdUtilizada.value).toLocaleString();
        
        const elTdRemover = document.createElement('td');
        elTdRemover.classList.add('p-3');
        const elBtnRemover = document.createElement('button');
        elBtnRemover.classList.add('btn', 'btn-danger', 'btn-sm');
        elBtnRemover.innerHTML = '<i class="bi bi-trash3-fill"></i>';
        elTdRemover.appendChild(elBtnRemover);
        
        elTr.appendChild(elTdDescricao);
        elTr.appendChild(elTdQuantidade);
        elTr.appendChild(elTdRemover);
        elTBody.appendChild(elTr);
        elBtnRemover.addEventListener('click', removeRowTable);
        
        listaIngredientes.push({
            descricao : elSelIngrediente.value,
            qtd : parseFloat(elQtdUtilizada.value),
            acucarAdicionado : elAcucarAdicional.checked
        });
        
    }
    
    elSelIngrediente.value = '';
    elQtdUtilizada.value = '0';
    elAcucarAdicional.checked = false;
    });
    
    // Funcao remover item table
    function removeRowTable() {
        const elTr = this.parentNode.parentNode;
        let descIngrediente = elTr.children[0].innerText;
        descIngrediente = descIngrediente.replace(' Açúcar', '')
        listaIngredientes = listaIngredientes.filter(i => i.descricao != descIngrediente);
        elTr.remove();
        if (listaIngredientes.length === 0) {
            const elRowVazio = document.getElementById('rowVazio');
            elRowVazio.style.display = '';
        }
    }
}

function formListener(){
    if (radiosFormula[1].checked) {
        const elAdicionarItem = document.getElementById('adicionarItem');
        const elSelIngrediente = document.getElementById('selIngrediente');
        const elQtdUtilizada = document.getElementById('quantidadeIngrediente');
        
        if (elSelIngrediente.value === '' || elQtdUtilizada.value === '' || !(parseFloat(elQtdUtilizada.value) > 0)) {
            elAdicionarItem.setAttribute('disabled', '');
        } else {
            elAdicionarItem.removeAttribute('disabled');
        }
    }
}

elEnviar.addEventListener('click', (e)=>{
    if (radiosFormula[1].checked && formItem.reportValidity()) {
        e.preventDefault();
        fetch(window.location.href, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': document.getElementsByName('csrfmiddlewaretoken')[0].value,
            },
            mode: 'same-origin',
            body: JSON.stringify({
                produto: document.getElementById('produto').value,
                composto: radiosFormula[1].checked,
                ingrediente: document.getElementById('ingrediente').checked,
                quantidade_porcao: parseFloat(document.getElementById('quantidadePorcao').value),
                quantidade_embalagem: parseInt(document.getElementById('quantidadeEmbalagem').value),
                quantidade_medida_caseira: parseFloat(document.getElementById('quantidadeCaseira').value),
                medida_caseira: parseInt(document.getElementById('medidaCaseira').value),
                quantidade_rendimento: document.getElementById('rendimento').value,
                ingredientes: listaIngredientes,
            }),
        })
        .then((response) => response.json())
        .then((data) => {
            /*
            const cod = data['cod'];
            const msg = data['msg'];
            console.log(data.status)
            if (cod) {
                window.location.assign(window.location.href);
            }
            window.alert(msg);*/
            window.location.replace(window.location.href);
        }
        
        ).catch(
            error => {
                console.error;
            }
        )

            
    }
})