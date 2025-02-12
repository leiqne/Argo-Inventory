function capitalizeFirstLetter(string) {
    return string.charAt(0).toUpperCase() + string.slice(1).toLowerCase();
}
function init(){
  var estado=document.getElementById("status-container").getAttribute("data-estado");
  capitalizeFirstLetter(estado);
}
document.getElementById("DOMContentLoaded", init);
const deleteSelected = async (button) => {
  const itemId = button.getAttribute('data-id'); // Obtener el ID del registro

  if (!itemId) {
      alert('Error: No se pudo obtener el ID del registro.');
      return;
  }

  if (!confirm('¿Está seguro de eliminar este registro?')) {
      return;
  }

  try {
      const response = await fetch(`/api/inventario/${itemId}`, {
          method: 'DELETE',
          headers: {
              'Content-Type': 'application/json'
          }
      });

      const result = await response.json();

      if (response.ok) {
          alert('Registro eliminado exitosamente.');
          button.closest('tr').remove(); // Eliminar la fila de la tabla
      } else {
          alert(`Error: ${result.error || 'No se pudo eliminar el registro'}`);
      }
  } catch (error) {
      console.error('Error:', error);
      alert('Ocurrió un error al intentar eliminar el registro.');
  }
};
