window.onload = init;
let currentClienteId = null;

function init() {
    const contextMenu = document.getElementById('context-menu');
    const clienteItems = document.querySelectorAll('.cliente-item');
    const ModalAddCliente = document.getElementById('ModalAddCliente');
    const formAddCliente = document.getElementById('formAddCliente');
    const btnAddCliente = document.getElementById('btnAddCliente');
    const btnCloseModal = document.getElementById('btnCloseModal'); // Botón cancelar
    const ModalRegistroDevolucion = document.getElementById('ModalRegistroDevolucion');
    const formRegistroDevolucion = document.getElementById('formRegistroDevolucion');
    const btnCloseModalRegistroDevolucion = document.getElementById('btnCloseModalRegistroDevolucion');
    const devolucionClienteInput = document.getElementById('devolucion-cliente');

    // Mostrar el modal "Añadir Registro de Devolución"
    contextMenu.addEventListener('click', (e) => {
        const action = e.target.dataset.action;
        if (action === 'add') {
            if (currentClienteId) {
                // Autocompletar cliente
                devolucionClienteInput.value = currentClienteId;

                // Mostrar modal
                ModalRegistroDevolucion.classList.remove('hidden');
            } else {
                alert('Seleccione un cliente válido.');
            }
        }
    });

    // Cerrar el modal
    btnCloseModalRegistroDevolucion.addEventListener('click', () => {
        ModalRegistroDevolucion.classList.add('hidden');
    });
    ModalRegistroDevolucion.addEventListener('click', (e) => {
        if (e.target === ModalRegistroDevolucion) {
            ModalRegistroDevolucion.classList.add('hidden');
        }
    });

    // Enviar datos del formulario al servidor
    formRegistroDevolucion.addEventListener('submit', async (e) => {
    e.preventDefault();
    const data = Object.fromEntries(new FormData(formRegistroDevolucion).entries());
    console.log('Datos enviados:', data);
    try {
        const req = await fetch('/add-devolucion', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data),
        });

        if (req.ok) {
            alert('Registro de devolución guardado exitosamente');
            ModalRegistroDevolucion.classList.add('hidden');
        } else {
            alert('Hubo un error al guardar el registro.');
        }
    } catch (error) {
        console.error('Error al guardar el registro:', error);
        alert('Error inesperado al guardar el registro.');
    }
    });

    formAddCliente.addEventListener('submit', async (e) => {
        e.preventDefault();
        const data = Object.fromEntries(new FormData(formAddCliente).entries());
        console.log('Datos enviados:', data);
        try {
            const req = await fetch('/add-cliente', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data),
            });
    
            if (req.ok) {
                const res = await req.json();
                alert('Cliente guardado exitosamente');
                console.log('Respuesta del servidor:', res);
    
                // Cierra la ventana modal
                ModalAddCliente.classList.add('hidden');
            } else {
                alert('Hubo un error al guardar el cliente');
            }
        } catch (error) {
            console.error('Error al guardar el cliente:', error);
            alert('Error inesperado al guardar el cliente');
        }
    });
    

    // Mostrar el modal al hacer clic en "Agregar Cliente"
    btnAddCliente.addEventListener('click', () => {
        ModalAddCliente.classList.remove('hidden');
    });

    // Cerrar el modal al hacer clic en "Cancelar"
    btnCloseModal.addEventListener('click', () => {
        ModalAddCliente.classList.add('hidden');
    });

    // Enviar el formulario al servidor
    formAddCliente.addEventListener('submit', async (e) => {
        e.preventDefault();
        const data = Object.fromEntries(new FormData(formAddCliente).entries());

        const req = await fetch('/add-cliente', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data),
        });

        const res = await req.json();
        console.log('Respuesta del servidor:', res);

        // Cerrar el modal después de enviar
        ModalAddCliente.classList.add('hidden');
    });

    // Mostrar el menú contextual
    clienteItems.forEach((item) => {
        item.addEventListener('contextmenu', (e) => {
            e.preventDefault();

            const clienteId = item.dataset.cliente;
            currentClienteId = clienteId;
            console.log('Cliente seleccionado:', clienteId);

            // Posicionar el menú en el cursor
            contextMenu.style.top = `${e.clientY}px`;
            contextMenu.style.left = `${e.clientX}px`;

            // Mostrar el menú
            contextMenu.classList.remove('hidden');
        });
    });

    // Ocultar el menú contextual al hacer clic fuera
    document.addEventListener('click', () => {
        contextMenu.classList.add('hidden');
        currentClienteId = null;
    });

    // Manejar acciones del menú contextual
    contextMenu.addEventListener('click', (e) => {
        const action = e.target.dataset.action;
        if (action) {
            if (action === 'pendientes') location.href = '/pendientes/' + currentClienteId;
        }
        contextMenu.classList.add('hidden'); // Cerrar el menú después de seleccionar
    });
}
