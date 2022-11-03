const elBody = document.querySelectorAll('table tbody tr');

document.addEventListener('DOMContentLoaded', ()=>{
    elBody.forEach(item =>{
        //console.log(item);
        const buttons = item.querySelectorAll('td a')
        //console.log(item.firstElementChild.innerHTML)
        //console.log(window.location.hostname)
        const editURL = `http://${window.location.hostname}:${window.location.port}/cadastro/edita_item/${item.querySelector('td').innerText}`;
        buttons[1].setAttribute("href", editURL);
        
        const removeURL = `http://${window.location.hostname}:${window.location.port}/cadastro/exclui_item/${item.querySelector('td').innerText}`;
        buttons[2].setAttribute("href", removeURL);
        buttons[2].addEventListener('click', function (e) {
            const modalItem = document.getElementById('modalItem');
            modalItem.innerText = item.children[1].innerText;
            
            const btnConfimaExcluir = document.getElementById('btnConfimaExcluir');
            btnConfimaExcluir.setAttribute("href", removeURL);
        });
    })
})