alert("funcionando el js");
// Función para capitalizar la primera letra
function capitalizeFirstLetter(string) {
    return string.charAt(0).toUpperCase() + string.slice(1).toLowerCase();
  }
  
  // Función para obtener el color de fondo según el estado
  function getStatusBackgroundColor(status) {
    switch (status.toLowerCase()) {
      case "pendiente":
        return "#FFFF00"; // Amarillo
      case "cancelado":
        return "#008000"; // Verde
      case "anulado":
        return "#FF0000"; // Rojo
      default:
        return "#808080"; // Gris
    }
  }
  
  // Función para crear y mostrar el badge con el estado
  function createStatusBadge(status) {
    const formattedStatus = capitalizeFirstLetter(status); 
    const backgroundColor = getStatusBackgroundColor(status); 
    const badge = document.createElement("div");
    badge.textContent = formattedStatus;
    badge.style.padding = "8px 12px";
    badge.style.borderRadius = "8px";
    badge.style.backgroundColor = backgroundColor;
    badge.style.color = "white";
    badge.style.fontWeight = "bold";
    badge.style.textAlign = "center";
    badge.style.margin = "4px";
  
    return badge;
  }
  
  // Ejemplo de uso: Renderizar varios estados
  const statuses = ["pendiente", "cancelado", "anulado", "desconocido"]; // Ejemplo de estados
  const container = document.getElementById("status-container");
  
  statuses.forEach((status) => {
    const badge = createStatusBadge(status);
    container.appendChild(badge);
  });
  