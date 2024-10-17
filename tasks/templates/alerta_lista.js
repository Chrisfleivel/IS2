// JavaScript (por ejemplo, en un archivo .js)
const listas = document.querySelectorAll('.lista');

listas.forEach(lista => {
    const tareasCount = lista.querySelector('.tareas-count').textContent;
    const maxWIP = lista.querySelector('.max-wip').textContent;

    if (tareasCount >= maxWIP) {
        lista.querySelector('.alerta').style.display = 'block';
    }
});