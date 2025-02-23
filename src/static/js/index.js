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
    
        try {
            const data = Object.fromEntries(new FormData(formRegistroDevolucion).entries());
    
            // Obtener los tipos de envase seleccionados y sus datos
            const tiposEnvase = Array.from(document.querySelectorAll('input[name="tipos_envase"]:checked')).map(checkbox => {
                const label = checkbox.closest('label');
                const kilosInput = label.querySelector('input[name^="kilos"]');
                const cantidadInput = label.querySelector('input[name^="cantidad"]');
    
                const kilos = kilosInput ? parseFloat(kilosInput.value) || 0 : 0;
                const cantidad = cantidadInput ? parseInt(cantidadInput.value) || 0 : 0;
    
                return {
                    tipo: checkbox.value,
                    kilos: kilos,
                    cantidad: cantidad,
                    descripcion: kilos > 0 ? `${kilos} kgs ${checkbox.value}` : checkbox.value
                };
            });
    
            // Validación de datos
            if (!tiposEnvase.every(envase => (envase.kilos >= 0 && envase.cantidad > 0))) {
                alert('Debe ingresar una cantidad válida y, si aplica, los kilos deben ser mayores a 0.');
                return;
            }
    
            // Formatear datos para el servidor
            data.tipos_envase = tiposEnvase.map(e => e.descripcion);
            data.cantidades = tiposEnvase.map(e => e.cantidad);
    
            console.log('Datos enviados:', data);
    
            // Enviar los datos al backend
            const response = await fetch('/add-devolucion', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(data),
            });
    
            const result = await response.json();
    
            if (!response.ok) throw new Error(result.error || 'Hubo un error desconocido al guardar el registro.');
    
            alert(result.message || 'Registro de devolución guardado exitosamente');
            location.reload();
            ModalRegistroDevolucion.classList.add('hidden');
    
        } catch (error) {
            console.error('Error al guardar el registro:', error);
            alert(error.message || 'Error inesperado al guardar el registro.');
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
    
        try {
            const req = await fetch('/add-cliente', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data),
            });
    
            const res = await req.json();
    
            if (!req.ok) {
                // Si hay un error, muestra el mensaje en la interfaz
                alert(res.error || 'Error al agregar el cliente');
                return;
            }
    
            // Si todo está bien, muestra el mensaje de éxito
            alert(res.message || 'Cliente agregado exitosamente');
            ModalAddCliente.classList.add('hidden');
        } catch (error) {
            console.error('Error en la solicitud:', error);
            alert('Error en la conexión con el servidor');
        }
    });
    //clientes
    document.querySelectorAll('.cliente-item').forEach(item => {
        item.addEventListener('contextmenu', (e) => {
            e.preventDefault(); // Prevenir el menú contextual predeterminado
    
            // Eliminar la clase 'active-hover' de todos los clientes
            document.querySelectorAll('.cliente-item').forEach(cliente => {
                cliente.classList.remove('active-hover');
            });
    
            // Agregar la clase 'active-hover' al cliente seleccionado
            item.classList.add('active-hover');
    
            // Mostrar el menú contextual
            const contextMenu = document.getElementById('context-menu');
            const scrollY = window.scrollY; // Obtener el desplazamiento vertical de la página
            contextMenu.style.top = `${e.clientY + scrollY}px`; // Ajustar la posición Y
            contextMenu.style.left = `${e.clientX}px`; // La posición X no necesita ajuste
            contextMenu.classList.remove('hidden');
    
            // Guardar el cliente actual para usarlo en el menú contextual
            const clienteId = item.getAttribute('data-cliente');
            currentClienteId = clienteId;
        });
    });
    
    document.addEventListener('click', (e) => {
        const contextMenu = document.getElementById('context-menu');
        const clienteItems = document.querySelectorAll('.cliente-item');
    
        // Si el clic es fuera de los elementos '.cliente-item' y el menú contextual, eliminar la clase 'active-hover'
        if (!e.target.closest('.cliente-item') && !e.target.closest('#context-menu')) {
            clienteItems.forEach(item => {
                item.classList.remove('active-hover');
            });
            contextMenu.classList.add('hidden');
        }
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
            if (action === 'summary') location.href = '/summary/' + currentClienteId;
            if (action === 'pendientes') location.href = '/pendientes/' + currentClienteId;
        }
        contextMenu.classList.add('hidden'); 
    });

    document.getElementById('buscadorClientes').addEventListener('input', function () {
        const searchValue = this.value.toLowerCase();
        const clienteItems = document.querySelectorAll('.cliente-item');

        clienteItems.forEach(item => {
            const clienteNombre = item.getAttribute('data-cliente').toLowerCase();
            if (clienteNombre.includes(searchValue)) {
                item.classList.add('flex')
                item.classList.remove('hidden')
            } else {
                item.classList.remove('flex')
                item.classList.add('hidden')
            }
        });
    });

}

function initListenerChecboxes() {
    const checkboxes = document.querySelectorAll('input[type="checkbox"][name="tipos_envase"]');

    checkboxes.forEach((checkbox) => {
        checkbox.addEventListener('change', () => {
            // Obtener el contenedor del checkbox
            const container = checkbox.closest('label');

            // Buscar los inputs dentro del mismo contenedor
            const cantidadInput = container.querySelector('input[name^="cantidad_"]');
            const kilosInput = container.querySelector('input[name^="kilos_"]'); // Para Caneca Plástico

            // Habilitar/deshabilitar los inputs de cantidad y kilos según el estado del checkbox
            if (cantidadInput) {
                cantidadInput.disabled = !checkbox.checked;
                if (!checkbox.checked) cantidadInput.value = '';
            }

            if (kilosInput) {
                kilosInput.disabled = !checkbox.checked;
                if (!checkbox.checked) kilosInput.value = '';
            }
        });
    });
}

// Llamar la función después de cargar el DOM
document.addEventListener('DOMContentLoaded', initListenerChecboxes);