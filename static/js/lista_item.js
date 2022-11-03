const elBody = document.querySelectorAll('table tbody tr');

document.addEventListener('DOMContentLoaded', ()=>{
    elBody.forEach(item =>{
        //console.log(item);
        const buttons = item.querySelectorAll('td a')
        //console.log(item.firstElementChild.innerHTML)
        //console.log(window.location.hostname)
        buttons[2].addEventListener('click', function (e) {
            const modalItem = document.getElementById('modalItem');
            modalItem.innerText = item.children[1].innerText;
            
            const btnConfimaExcluir = document.getElementById('btnConfimaExcluir');
            const btnURL = `http://${window.location.hostname}:${window.location.port}/cadastro/exclui_item/${item.querySelector('td').innerText}`;
            btnConfimaExcluir.setAttribute("href", btnURL);
        })
    })
})