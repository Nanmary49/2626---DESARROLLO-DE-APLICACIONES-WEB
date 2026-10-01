var catalogoServicios = [
    { id:1, icono:'🎭', titulo:'Figuras Coleccionables', imagen:'figuras-coleccionables.jpg',
      descripcion:'Figuras de anime y personajes exclusivos pintadas a mano para coleccionistas exigentes.',
      badge:'bg-primary' },
    { id:2, icono:'🪖', titulo:'Modelos a Escala', imagen:'modelos-a-escala.jpg',
      descripcion:'Réplicas y modelos militares elaborados con gran detalle y precisión histórica.',
      badge:'bg-success' },
    { id:3, icono:'🖨️', titulo:'Impresiones 3D', imagen:'impresiones-3d.jpg',
      descripcion:'Diseños personalizados mediante tecnología de impresión 3D de alta resolución.',
      badge:'bg-warning text-dark' },
    { id:4, icono:'🎨', titulo:'Pintura Profesional', imagen:'pintura-profesional.jpg',
      descripcion:'Acabados de alta calidad con aerógrafo y pintura acrílica para miniaturas.',
      badge:'bg-danger' },
    { id:5, icono:'🔧', titulo:'Restauración', imagen:'restauracion.jpg',
      descripcion:'Recuperación y mantenimiento especializado de figuras coleccionables dañadas.',
      badge:'bg-info text-dark' },
    { id:6, icono:'⭐', titulo:'Artículos Exclusivos', imagen:'articulos-exclusivos.jpg',
      descripcion:'Piezas únicas de edición limitada para coleccionistas y aficionados al modelismo.',
      badge:'bg-secondary' }
];



document.addEventListener('DOMContentLoaded', function () {
    function renderizarCatalogo() {
        var contenedor = document.getElementById('contenedor-catalogo');
        contenedor.innerHTML = '';

        // CONDICIÓN: catálogo vacío → mensaje de advertencia
        if (catalogoServicios.length === 0) {
            var aviso = document.createElement('p');
            aviso.className = 'text-center text-warning col-12';
            aviso.textContent = '⚠️ No hay servicios disponibles en este momento.';
            contenedor.appendChild(aviso);
            return;
        }

        // ESTRUCTURA REPETITIVA: forEach genera una tarjeta Bootstrap por servicio
        catalogoServicios.forEach(function (servicio) {

            var col = document.createElement('div');
            col.className = 'col-md-4 col-sm-6';

            // Tarjeta Bootstrap con clases card, card-body, card-title, card-text
            var card     = document.createElement('div');
            card.className = 'card h-100 shadow-sm card-catalogo';

            var cardBody = document.createElement('div');
            cardBody.className = 'card-body d-flex flex-column';

            var image = document.createElement('img');
            image.className = 'card-catalogo-imagen';
            image.src = '/static/img/' + servicio.imagen;
            image.alt = servicio.titulo;
            image.loading = 'lazy';

            var titulo = document.createElement('h5');
            titulo.className = 'card-title';
            titulo.textContent = servicio.icono + ' ' + servicio.titulo;

            var descripcion = document.createElement('p');
            descripcion.className = 'card-text small flex-grow-1';
            descripcion.textContent = servicio.descripcion;

            // Badge Bootstrap con color dinámico desde el arreglo
            var badge = document.createElement('span');
            badge.className = 'badge ' + servicio.badge + ' mt-auto';
            badge.textContent = 'Servicio #' + servicio.id;

            card.appendChild(image);
            cardBody.appendChild(titulo);
            cardBody.appendChild(descripcion);
            cardBody.appendChild(badge);
            card.appendChild(cardBody);
            col.appendChild(card);
            contenedor.appendChild(col);
        });
    }

    // Renderizar catálogo al cargar la página
    renderizarCatalogo();



    var form = document.getElementById('formulario-contacto');
    if (form) form.addEventListener('submit', function (event) {
        event.preventDefault();
        var nombre = document.getElementById('contacto-nombre').value.trim();
        var correo = document.getElementById('contacto-correo').value.trim();
        var asunto = document.getElementById('contacto-asunto').value.trim();
        var mensaje = document.getElementById('contacto-mensaje').value.trim();
        var alerta = document.getElementById('alerta-contacto');
        alerta.className = 'alert alert-warning';
        if (!nombre || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(correo) || !asunto || !mensaje) {
            alerta.textContent = 'Completa todos los campos e ingresa un correo válido.';
            return;
        }
        alerta.textContent = 'Se abrirá tu aplicación de correo. Revisa el mensaje y pulsa Enviar allí; todavía no se ha enviado.';
        window.location.href = 'mailto:narvicollectors@gmail.com?subject=' + encodeURIComponent(asunto) + '&body=' + encodeURIComponent('Nombre: ' + nombre + '\nCorreo: ' + correo + '\n\n' + mensaje);
    });
});
