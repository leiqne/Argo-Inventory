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

    initListenerChecboxes();

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

    formRegistroDevolucion.addEventListener('submit', async (e) => {
        e.preventDefault();
    
        // Crear el objeto de datos
        const data = Object.fromEntries(new FormData(formRegistroDevolucion).entries());
    
        // Obtener los tipos de envase seleccionados
        const tiposEnvase = Array.from(
            document.querySelectorAll('input[name="tipos_envase"]:checked')
        ).map(checkbox => ({
            value: checkbox.value,
            element: checkbox.parentElement
        }));
        

        console.log({tiposEnvase});
        
        // Obtener las cantidades correspondientes
        const cantidades = tiposEnvase.map(envase => {
            const cantidadInput = envase.element.nextElementSibling
            return cantidadInput ? parseInt(cantidadInput.value || '0', 10) : 0;
        });

        // Validar que todas las cantidades sean enteros positivos
        if (!cantidades.every(cantidad => Number.isInteger(cantidad) && cantidad >= 0)) {
            alert('Las cantidades deben ser números enteros positivos.');
            return;
        }
    
        // Agregar tipos de envase y cantidades al objeto de datos
        data.tipos_envase = tiposEnvase.map(e => e.value);
        data.cantidades = cantidades;
    
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
                location.reload();
                ModalRegistroDevolucion.classList.add('hidden');
            } else {
                alert('Hubo un error al guardar el registro.');
            }
        } catch (error) {
            console.error('Error al guardar el registro:', error);
            alert('Error inesperado al guardar el registro.');
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

        ModalAddCliente.classList.add('hidden');
    });

    // Mostrar el menú contextual
    clienteItems.forEach((item) => {
        item.addEventListener('contextmenu', (e) => {
            e.preventDefault();

            const clienteId = item.dataset.cliente;
            currentClienteId = clienteId;
            console.log('Cliente seleccionado:', clienteId);

            contextMenu.style.top = `${e.clientY}px`;
            contextMenu.style.left = `${e.clientX}px`;

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
        contextMenu.classList.add('hidden'); 
    });
    
}


function initListenerChecboxes() {
    const checkboxes = document.querySelectorAll('input[type="checkbox"][name="tipos_envase"]');
    checkboxes.forEach((checkbox) => {
        checkbox.addEventListener('change', () => {
            // Crear el selector del input correspondiente a la cantidad
            const cantidadInput = checkbox.parentElement.nextElementSibling;

            if (cantidadInput) {
                cantidadInput.disabled = !checkbox.checked; // Habilitar/deshabilitar según el estado del checkbox
                if (!checkbox.checked) {
                    cantidadInput.value = ''; // Limpiar valor si se desmarca
                }
            }
        });
    });
}