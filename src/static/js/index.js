window.onload = init
let currentClienteId = null;

function init() {
    const contextMenu = document.getElementById('context-menu');
    const clienteItems = document.querySelectorAll('.cliente-item');
    const ModalAddCliente = document.getElementById('ModalAddCliente');
    const formAddCliente = document.getElementById('formAddCliente');
    const btnAddCliente = document.getElementById('btnAddCliente');


    btnAddCliente.addEventListener('click', ()=> {
        ModalAddCliente.classList.toggle('hidden')
    })

    formAddCliente.addEventListener('submit', async (e)=>{
        e.preventDefault();
        const data = Object.fromEntries(new FormData(formAddCliente).entries());

        const req = await fetch('/add-cliente', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });
        const res = await req.json();
        console.log('Respuesta del servidor:', res);
    })

    clienteItems.forEach(item => {
        item.addEventListener('contextmenu', (e) => {
            e.preventDefault();

            const clienteId = item.dataset.cliente;
            currentClienteId = clienteId;
            console.log('Cliente seleccionado:', clienteId);

            // Posiciona el menú en el cursor
            contextMenu.style.top = `${e.clientY}px`;
            contextMenu.style.left = `${e.clientX}px`;

            // Muestra el menú
            contextMenu.classList.remove('hidden');
        });
    });

    // Ocultar el menú al hacer clic en cualquier parte
    document.addEventListener('click', () => {
        contextMenu.classList.add('hidden');
        currentClienteId = null;
    });

    // Manejar las acciones del menú
    contextMenu.addEventListener('click', (e) => {
        const action = e.target.dataset.action;
        if (action) {
            if (action === 'pendientes') location.href = '/pendientes/' + currentClienteId;
        }
        contextMenu.classList.add('hidden'); // Cierra el menú tras seleccionar
    });
}