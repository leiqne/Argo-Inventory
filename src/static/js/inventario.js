function capitalizeFirstLetter(string) {
    return string.charAt(0).toUpperCase() + string.slice(1).toLowerCase();
}
function init(){
  var estado=document.getElementById("status-container").getAttribute("data-estado");
  capitalizeFirstLetter(estado);
}
document.getElementById("DOMContentLoaded", init);
deleteSelected = async (e) => {
  const selected = e.getAttribute('data')
  console.log({element: e, selected}, Boolean(selected))
  if (!selected || !e) {
      alert('Seleccione al menos un registro.');
      return;
  }

  if (confirm('¿Está seguro de eliminar los registros seleccionados?')) {
      try {
          const response = await fetch(`/api/pendientes/${CLIENT_NAME}`, {
              method: 'DELETE',
              headers: {
                  'Content-Type': 'application/json'
              },
              body: JSON.stringify({id: selected})
          });

          if (response.ok) {
              alert('Registros eliminados correctamente.');
              e.parentElement.parentElement.parentElement.remove();
          } else {
              alert('Ocurrió un error al intentar eliminar los registros.');
          }
      } catch (error) {
          console.error(error);
          alert('Ocurrió un error al intentar eliminar los registros.');
      }
  }
}