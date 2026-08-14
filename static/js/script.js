// ================================================================
// script.js — Narvi Collector Scale Models
// Semana 8: Bootstrap modales, spinner, alertas + toda la lógica anterior
// Semana 7: Arreglos, renderizado dinámico, forEach, condiciones
// Semana 6: Validaciones input/blur/submit, is-valid/is-invalid
// Estudiante: Nancy Campos Basurto
// ================================================================


// ================================================================
// ARREGLO 1 — Catálogo de servicios del emprendimiento
// Datos representados como objetos dentro de un arreglo.
// Se renderiza dinámicamente con forEach (estructura repetitiva).
// ================================================================
var catalogoServicios = [
    { id:1, icono:'🎭', titulo:'Figuras Coleccionables',
      descripcion:'Figuras de anime y personajes exclusivos pintadas a mano para coleccionistas exigentes.',
      badge:'bg-primary' },
    { id:2, icono:'🪖', titulo:'Modelos a Escala',
      descripcion:'Réplicas y modelos militares elaborados con gran detalle y precisión histórica.',
      badge:'bg-success' },
    { id:3, icono:'🖨️', titulo:'Impresiones 3D',
      descripcion:'Diseños personalizados mediante tecnología de impresión 3D de alta resolución.',
      badge:'bg-warning text-dark' },
    { id:4, icono:'🎨', titulo:'Pintura Profesional',
      descripcion:'Acabados de alta calidad con aerógrafo y pintura acrílica para miniaturas.',
      badge:'bg-danger' },
    { id:5, icono:'🔧', titulo:'Restauración',
      descripcion:'Recuperación y mantenimiento especializado de figuras coleccionables dañadas.',
      badge:'bg-info text-dark' },
    { id:6, icono:'⭐', titulo:'Artículos Exclusivos',
      descripcion:'Piezas únicas de edición limitada para coleccionistas y aficionados al modelismo.',
      badge:'bg-secondary' }
];


// ================================================================
// ARREGLO 2 — Productos registrados por el usuario
// Crece con push() al registrar y se filtra con splice() al eliminar.
// ================================================================
var productosRegistrados = [];


// ================================================================
// Variable global: índice del producto pendiente de eliminar.
// Lo usa el modal de confirmación para saber cuál eliminar.
// ================================================================
var indiceAEliminar = -1;


// ================================================================
// Variable global: contador total de productos registrados
// ================================================================
var totalRegistros = 0;


// ================================================================
// ESPERAR A QUE EL DOM ESTÉ COMPLETAMENTE CARGADO
// DOMContentLoaded garantiza que todos los elementos existen
// antes de que JavaScript intente acceder a ellos.
// ================================================================
document.addEventListener('DOMContentLoaded', function () {

    // ------------------------------------------------------------
    // Referencias a elementos del formulario de gestión
    // ------------------------------------------------------------
    var formularioProducto = document.getElementById('formulario-producto');
    var campoNombre        = document.getElementById('campo-nombre');
    var campoDescripcion   = document.getElementById('campo-descripcion');
    var campoCategoria     = document.getElementById('campo-categoria');
    var alertaGlobal       = document.getElementById('alerta-global');
    var spinnerRegistro    = document.getElementById('spinner-registro');
    var listaProductos     = document.getElementById('lista-productos');
    var tablaCuerpo        = document.getElementById('tabla-cuerpo');
    var numeroRegistros    = document.getElementById('numero-registros');
    var contadorCaracteres = document.getElementById('contador-caracteres');

    // Referencias a elementos del formulario de contacto
    var formularioContacto = document.getElementById('formulario-contacto');
    var contactoNombre     = document.getElementById('contacto-nombre');
    var contactoCorreo     = document.getElementById('contacto-correo');
    var contactoAsunto     = document.getElementById('contacto-asunto');
    var contactoMensaje    = document.getElementById('contacto-mensaje');
    var alertaContacto     = document.getElementById('alerta-contacto');

    // Referencias a los modales Bootstrap (se instancian con bootstrap.Modal)
    var modalDetalle   = new bootstrap.Modal(document.getElementById('modalDetalleProducto'));
    var modalEliminar  = new bootstrap.Modal(document.getElementById('modalConfirmarEliminar'));

    // Botón de confirmación dentro del modal de eliminación
    var btnConfirmarEliminar = document.getElementById('btn-confirmar-eliminar');


    // ============================================================
    // FUNCIÓN: renderizarCatalogo()
    // Itera el arreglo catalogoServicios con forEach y crea
    // tarjetas Bootstrap con createElement + appendChild.
    // CONDICIÓN: si el arreglo está vacío muestra mensaje de aviso.
    // ============================================================
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


    // ============================================================
    // FUNCIÓN: actualizarContador()
    // Muestra el total actual de productos en el badge Bootstrap.
    // ============================================================
    function actualizarContador() {
        numeroRegistros.textContent = totalRegistros;
    }


    // ============================================================
    // FUNCIÓN: renderizarProductos()
    // Reconstruye la tabla Bootstrap y las tarjetas de detalle
    // leyendo el arreglo productosRegistrados con forEach.
    // CONDICIÓN: arreglo vacío → fila de aviso en la tabla.
    // ============================================================
    function renderizarProductos() {

        // --- Reconstruir tabla Bootstrap ---
        tablaCuerpo.innerHTML = '';

        // CONDICIÓN: sin productos → fila de aviso Bootstrap
        if (productosRegistrados.length === 0) {
            var fila  = document.createElement('tr');
            var celda = document.createElement('td');
            celda.colSpan = 4;
            celda.className = 'text-center text-secondary fst-italic py-3';
            celda.textContent = 'No hay productos registrados. Usa el formulario para agregar.';
            fila.appendChild(celda);
            tablaCuerpo.appendChild(fila);
        } else {
            // ESTRUCTURA REPETITIVA: forEach crea una fila por producto
            productosRegistrados.forEach(function (producto, indice) {

                var fila = document.createElement('tr');

                // Celda: número de orden
                var cNum = document.createElement('td');
                cNum.className = 'text-center fw-bold text-info';
                cNum.textContent = indice + 1;

                // Celda: nombre del producto
                var cNombre = document.createElement('td');
                cNombre.textContent = producto.nombre;

                // Celda: badge Bootstrap con la categoría
                var cCat   = document.createElement('td');
                var badgeCat = document.createElement('span');
                badgeCat.className = 'badge bg-secondary';
                badgeCat.textContent = producto.categoria;
                cCat.appendChild(badgeCat);

                // Celda: botones Detalles y Eliminar (Bootstrap btn btn-info / btn-danger)
                var cAccion = document.createElement('td');
                cAccion.className = 'text-center';

                // Botón "Detalles" — abre modalDetalleProducto con los datos del producto
                var btnDetalle = document.createElement('button');
                btnDetalle.type      = 'button';
                btnDetalle.className = 'btn btn-info btn-sm text-dark me-1';
                btnDetalle.textContent = '🔍 Detalles';

                // Al hacer clic llena el modal Bootstrap con los datos y lo abre
                btnDetalle.addEventListener('click', function () {
                    document.getElementById('modal-nombre-producto').textContent    = producto.nombre;
                    document.getElementById('modal-descripcion-producto').textContent = producto.descripcion;
                    document.getElementById('modal-categoria-producto').textContent = producto.categoria;
                    modalDetalle.show();
                });

                // Botón "Eliminar" — abre modalConfirmarEliminar Bootstrap
                var btnEliminar = document.createElement('button');
                btnEliminar.type      = 'button';
                btnEliminar.className = 'btn btn-danger btn-sm';
                btnEliminar.textContent = '🗑 Eliminar';

                // Guarda el índice y el nombre en el modal y lo abre
                btnEliminar.addEventListener('click', function () {
                    indiceAEliminar = indice;
                    document.getElementById('modal-nombre-eliminar').textContent = producto.nombre;
                    modalEliminar.show();
                });

                cAccion.appendChild(btnDetalle);
                cAccion.appendChild(btnEliminar);

                fila.appendChild(cNum);
                fila.appendChild(cNombre);
                fila.appendChild(cCat);
                fila.appendChild(cAccion);
                tablaCuerpo.appendChild(fila);
            });
        }

        // --- Reconstruir tarjetas Bootstrap de detalle ---
        listaProductos.innerHTML = '';

        // ESTRUCTURA REPETITIVA: forEach crea una card Bootstrap por producto
        productosRegistrados.forEach(function (producto, indice) {

            var col = document.createElement('div');
            col.className = 'col-12';

            // Card Bootstrap: card card-producto shadow-sm
            var card     = document.createElement('div');
            card.className = 'card card-producto shadow-sm';

            var cardBody = document.createElement('div');
            cardBody.className = 'card-body d-flex justify-content-between align-items-start flex-wrap gap-2';

            var textoDiv = document.createElement('div');
            textoDiv.className = 'flex-grow-1';

            var titulo = document.createElement('h6');
            titulo.className = 'card-title mb-1 text-info fw-bold';
            titulo.textContent = '📦 ' + producto.nombre;

            var desc = document.createElement('p');
            desc.className = 'card-text small mb-2';
            desc.textContent = producto.descripcion;

            var badgeCat = document.createElement('span');
            badgeCat.className = 'badge bg-secondary me-2';
            badgeCat.textContent = producto.categoria;

            textoDiv.appendChild(titulo);
            textoDiv.appendChild(desc);
            textoDiv.appendChild(badgeCat);

            // CONDICIÓN: descripción larga → badge "Descripción detallada"
            if (producto.descripcion.length > 80) {
                var etiqueta = document.createElement('span');
                etiqueta.className = 'badge bg-info text-dark';
                etiqueta.textContent = '✔ Descripción detallada';
                textoDiv.appendChild(etiqueta);
            }

            // Botones Bootstrap en la tarjeta
            var btnsDiv = document.createElement('div');
            btnsDiv.className = 'd-flex flex-column gap-2 align-self-center';

            // Botón Detalles de la tarjeta
            var btnDetalleTarjeta = document.createElement('button');
            btnDetalleTarjeta.type      = 'button';
            btnDetalleTarjeta.className = 'btn btn-outline-info btn-sm';
            btnDetalleTarjeta.textContent = '🔍 Ver';
            btnDetalleTarjeta.addEventListener('click', function () {
                document.getElementById('modal-nombre-producto').textContent     = producto.nombre;
                document.getElementById('modal-descripcion-producto').textContent = producto.descripcion;
                document.getElementById('modal-categoria-producto').textContent  = producto.categoria;
                modalDetalle.show();
            });

            // Botón Eliminar de la tarjeta (abre modal de confirmación)
            var btnEliminarTarjeta = document.createElement('button');
            btnEliminarTarjeta.type      = 'button';
            btnEliminarTarjeta.className = 'btn btn-outline-danger btn-sm';
            btnEliminarTarjeta.textContent = '🗑 Eliminar';
            btnEliminarTarjeta.addEventListener('click', function () {
                indiceAEliminar = indice;
                document.getElementById('modal-nombre-eliminar').textContent = producto.nombre;
                modalEliminar.show();
            });

            btnsDiv.appendChild(btnDetalleTarjeta);
            btnsDiv.appendChild(btnEliminarTarjeta);
            cardBody.appendChild(textoDiv);
            cardBody.appendChild(btnsDiv);
            card.appendChild(cardBody);
            col.appendChild(card);
            listaProductos.appendChild(col);
        });
    }

    // Mostrar tabla inicial con fila de aviso (arreglo vacío)
    renderizarProductos();


    // ============================================================
    // EVENTO: Confirmar eliminación desde el modal Bootstrap
    // Al hacer clic en "Sí, eliminar" se usa splice() sobre el arreglo,
    // se actualiza el contador y se re-renderiza todo.
    // ============================================================
    btnConfirmarEliminar.addEventListener('click', function () {
        if (indiceAEliminar >= 0) {
            productosRegistrados.splice(indiceAEliminar, 1);  // Eliminar del arreglo
            indiceAEliminar  = -1;                            // Resetear índice
            totalRegistros   = productosRegistrados.length;
            actualizarContador();
            renderizarProductos();  // Re-renderizar tabla y tarjetas
            modalEliminar.hide();   // Cerrar modal Bootstrap
        }
    });


    // ============================================================
    // SEMANA 6 — FUNCIONES DE VALIDACIÓN (conservadas íntegras)
    // ============================================================

    // Aplica clase Bootstrap is-valid + muestra mensaje de éxito
    function marcarValido(campo, idOk, mensaje) {
        campo.classList.remove('is-invalid');
        campo.classList.add('is-valid');
        if (idOk) {
            var div = document.getElementById(idOk);
            if (div) div.textContent = mensaje;
        }
    }

    // Aplica clase Bootstrap is-invalid + muestra mensaje de error
    function marcarInvalido(campo, idError, mensaje) {
        campo.classList.remove('is-valid');
        campo.classList.add('is-invalid');
        if (idError) {
            var div = document.getElementById(idError);
            if (div) div.textContent = mensaje;
        }
    }

    // Quita las clases de validación (estado neutro)
    function limpiarEstado(campo) {
        campo.classList.remove('is-valid', 'is-invalid');
    }

    // Muestra alerta Bootstrap y la oculta automáticamente a los 5 segundos
    function mostrarAlertaGlobal(divAlerta, tipo, texto) {
        divAlerta.className = 'alert alert-' + tipo;
        divAlerta.textContent = texto;
        setTimeout(function () {
            divAlerta.className = 'alert d-none';
            divAlerta.textContent = '';
        }, 5000);
    }

    // Valida nombre: obligatorio + mínimo 3 caracteres
    function validarNombre() {
        var valor = campoNombre.value.trim();
        if (valor === '') {
            marcarInvalido(campoNombre, 'error-nombre', 'El nombre del producto es obligatorio.');
            return false;
        }
        if (valor.length < 3) {
            marcarInvalido(campoNombre, 'error-nombre', 'El nombre debe tener al menos 3 caracteres.');
            return false;
        }
        marcarValido(campoNombre, 'ok-nombre', '✓ Nombre válido.');
        return true;
    }

    // Valida descripción: obligatoria + mínimo 10 caracteres
    function validarDescripcion() {
        var valor = campoDescripcion.value.trim();
        if (valor === '') {
            marcarInvalido(campoDescripcion, 'error-descripcion', 'La descripción es obligatoria.');
            return false;
        }
        if (valor.length < 10) {
            marcarInvalido(campoDescripcion, 'error-descripcion', 'La descripción debe tener al menos 10 caracteres.');
            return false;
        }
        marcarValido(campoDescripcion, 'ok-descripcion', '✓ Descripción válida.');
        return true;
    }

    // Valida categoría: debe seleccionarse una opción válida
    function validarCategoria() {
        var valor = campoCategoria.value;
        if (valor === '') {
            marcarInvalido(campoCategoria, 'error-categoria', 'Debes seleccionar una categoría.');
            return false;
        }
        marcarValido(campoCategoria, 'ok-categoria', '✓ Categoría seleccionada.');
        return true;
    }


    // ============================================================
    // SEMANA 6 — EVENTOS input Y blur (tiempo real)
    // ============================================================

    // Evento input: valida mientras el usuario escribe
    campoNombre.addEventListener('input',      function () { validarNombre();      });
    campoCategoria.addEventListener('input',   function () { validarCategoria();   });
    campoDescripcion.addEventListener('input', function () {
        contadorCaracteres.textContent = campoDescripcion.value.length;
        validarDescripcion();
    });

    // Evento blur: valida al salir del campo sin completarlo
    campoNombre.addEventListener('blur',       function () { validarNombre();      });
    campoDescripcion.addEventListener('blur',  function () { validarDescripcion(); });
    campoCategoria.addEventListener('blur',    function () { validarCategoria();   });


    // ============================================================
    // EVENTO SUBMIT — Formulario de gestión
    // preventDefault() evita la recarga de la página.
    // Solo registra si las 3 validaciones son correctas.
    // Muestra spinner Bootstrap, luego alerta Bootstrap de éxito.
    // ============================================================
    formularioProducto.addEventListener('submit', function (evento) {
        evento.preventDefault();  // Evitar recarga de la página

        var nombreValido      = validarNombre();
        var descripcionValida = validarDescripcion();
        var categoriaValida   = validarCategoria();

        // CONDICIÓN: todos los campos válidos → registrar
        if (nombreValido && descripcionValida && categoriaValida) {

            var nuevoProducto = {
                nombre:      campoNombre.value.trim(),
                descripcion: campoDescripcion.value.trim(),
                categoria:   campoCategoria.value
            };

            // Deshabilitar botón y mostrar SPINNER Bootstrap (proceso simulado)
            document.getElementById('btn-registrar').disabled = true;
            spinnerRegistro.classList.remove('d-none');

            // Simular proceso de 1.2 segundos (carga) antes de registrar
            setTimeout(function () {

                // Agregar objeto al arreglo
                productosRegistrados.push(nuevoProducto);
                totalRegistros = productosRegistrados.length;
                actualizarContador();
                renderizarProductos();

                // Ocultar spinner Bootstrap y rehabilitar botón
                spinnerRegistro.classList.add('d-none');
                document.getElementById('btn-registrar').disabled = false;

                // Mostrar ALERTA Bootstrap de éxito (alert-success)
                mostrarAlertaGlobal(
                    alertaGlobal,
                    'success',
                    '✅ Producto "' + nuevoProducto.nombre + '" registrado. Total: ' + totalRegistros
                );

                // Limpiar formulario y estados de validación
                formularioProducto.reset();
                limpiarEstado(campoNombre);
                limpiarEstado(campoDescripcion);
                limpiarEstado(campoCategoria);
                contadorCaracteres.textContent = '0';

            }, 1200); // 1.2 segundos de proceso simulado

        } else {
            // CONDICIÓN: hay errores → alerta Bootstrap de error (alert-danger)
            mostrarAlertaGlobal(
                alertaGlobal,
                'danger',
                '⚠️ Corrige los errores indicados antes de registrar.'
            );
        }
    });


    // ============================================================
    // SEMANA 6 — EVENTO SUBMIT del formulario de contacto
    // preventDefault() + validaciones + alerta Bootstrap
    // ============================================================
    formularioContacto.addEventListener('submit', function (evento) {
        evento.preventDefault();

        var nombre   = contactoNombre.value.trim();
        var correo   = contactoCorreo.value.trim();
        var asunto   = contactoAsunto.value.trim();
        var mensaje  = contactoMensaje.value.trim();
        var hayError = false;

        var reCorreo = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

        if (nombre === '') {
            marcarInvalido(contactoNombre, 'error-contacto-nombre', 'El nombre es obligatorio.');
            hayError = true;
        } else { marcarValido(contactoNombre, null, ''); }

        if (correo === '') {
            marcarInvalido(contactoCorreo, 'error-contacto-correo', 'El correo es obligatorio.');
            hayError = true;
        } else if (!reCorreo.test(correo)) {
            marcarInvalido(contactoCorreo, 'error-contacto-correo', 'Ingresa un correo electrónico válido.');
            hayError = true;
        } else { marcarValido(contactoCorreo, null, ''); }

        if (asunto === '') {
            marcarInvalido(contactoAsunto, 'error-contacto-asunto', 'El asunto es obligatorio.');
            hayError = true;
        } else { marcarValido(contactoAsunto, null, ''); }

        if (mensaje === '') {
            marcarInvalido(contactoMensaje, 'error-contacto-mensaje', 'El mensaje es obligatorio.');
            hayError = true;
        } else { marcarValido(contactoMensaje, null, ''); }

        if (!hayError) {
            // Alerta Bootstrap alert-success
            mostrarAlertaGlobal(
                alertaContacto, 'success',
                '✅ Mensaje enviado. ¡Gracias, ' + nombre + '! Te contactaremos pronto.'
            );
            formularioContacto.reset();
            limpiarEstado(contactoNombre);
            limpiarEstado(contactoCorreo);
            limpiarEstado(contactoAsunto);
            limpiarEstado(contactoMensaje);
        } else {
            // Alerta Bootstrap alert-danger
            mostrarAlertaGlobal(
                alertaContacto, 'danger',
                '⚠️ Por favor completa correctamente todos los campos.'
            );
        }
    });

    // Validaciones blur del formulario de contacto (Semana 6)
    var reCorreoBlur = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

    contactoNombre.addEventListener('blur', function () {
        if (contactoNombre.value.trim() === '') {
            marcarInvalido(contactoNombre, 'error-contacto-nombre', 'El nombre es obligatorio.');
        } else { marcarValido(contactoNombre, null, ''); }
    });

    contactoCorreo.addEventListener('blur', function () {
        var val = contactoCorreo.value.trim();
        if (val === '') {
            marcarInvalido(contactoCorreo, 'error-contacto-correo', 'El correo es obligatorio.');
        } else if (!reCorreoBlur.test(val)) {
            marcarInvalido(contactoCorreo, 'error-contacto-correo', 'Ingresa un correo válido.');
        } else { marcarValido(contactoCorreo, null, ''); }
    });

    contactoAsunto.addEventListener('blur', function () {
        if (contactoAsunto.value.trim() === '') {
            marcarInvalido(contactoAsunto, 'error-contacto-asunto', 'El asunto es obligatorio.');
        } else { marcarValido(contactoAsunto, null, ''); }
    });

    contactoMensaje.addEventListener('blur', function () {
        if (contactoMensaje.value.trim() === '') {
            marcarInvalido(contactoMensaje, 'error-contacto-mensaje', 'El mensaje es obligatorio.');
        } else { marcarValido(contactoMensaje, null, ''); }
    });

}); // ← Fin de DOMContentLoaded