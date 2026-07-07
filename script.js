// ================================================================
// script.js — Narvi Collector Scale Models
// Semana 7: Arreglos, renderizado dinámico y estructura de plantilla
// Conserva todas las validaciones de Semana 6
// Estudiante: Nancy Campos Basurto
// ================================================================


// ================================================================
// 1. ARREGLO DE DATOS — Catálogo de servicios del emprendimiento
//    Representa los datos del proyecto como objetos dentro de un arreglo.
//    Cada objeto tiene: id, icono, titulo, descripcion y color del badge.
//    Este arreglo evita repetir manualmente bloques HTML en el index.html.
// ================================================================
var catalogoServicios = [
    {
        id: 1,
        icono: '🎭',
        titulo: 'Figuras Coleccionables',
        descripcion: 'Figuras de anime y personajes exclusivos pintadas a mano para coleccionistas exigentes.',
        badge: 'bg-primary'
    },
    {
        id: 2,
        icono: '🪖',
        titulo: 'Modelos a Escala',
        descripcion: 'Réplicas y modelos militares elaborados con gran detalle y precisión histórica.',
        badge: 'bg-success'
    },
    {
        id: 3,
        icono: '🖨️',
        titulo: 'Impresiones 3D',
        descripcion: 'Diseños personalizados mediante tecnología de impresión 3D de alta resolución.',
        badge: 'bg-warning text-dark'
    },
    {
        id: 4,
        icono: '🎨',
        titulo: 'Pintura Profesional',
        descripcion: 'Acabados de alta calidad con aerógrafo y pintura acrílica para miniaturas.',
        badge: 'bg-danger'
    },
    {
        id: 5,
        icono: '🔧',
        titulo: 'Restauración',
        descripcion: 'Recuperación y mantenimiento especializado de figuras coleccionables dañadas.',
        badge: 'bg-info text-dark'
    },
    {
        id: 6,
        icono: '⭐',
        titulo: 'Artículos Exclusivos',
        descripcion: 'Piezas únicas de edición limitada para coleccionistas y aficionados al modelismo.',
        badge: 'bg-secondary'
    }
];


// ================================================================
// 2. ARREGLO DE PRODUCTOS REGISTRADOS
//    Almacena dinámicamente los productos que el usuario agrega.
//    Cada vez que se registra un producto se hace push() al arreglo.
//    Cuando se elimina, se filtra con splice().
// ================================================================
var productosRegistrados = [];


// ================================================================
// 3. CONTADOR GLOBAL de productos registrados
// ================================================================
var totalRegistros = 0;


// ================================================================
// 4. ESPERAR A QUE EL DOM ESTÉ CARGADO COMPLETAMENTE
//    DOMContentLoaded garantiza que todos los elementos HTML existen
//    antes de que JavaScript intente acceder a ellos.
// ================================================================
document.addEventListener('DOMContentLoaded', function () {

    // ------------------------------------------------------------
    // Referencias a elementos del formulario de gestión
    // ------------------------------------------------------------
    var formularioProducto  = document.getElementById('formulario-producto');
    var campoNombre         = document.getElementById('campo-nombre');
    var campoDescripcion    = document.getElementById('campo-descripcion');
    var campoCategoria      = document.getElementById('campo-categoria');
    var alertaGlobal        = document.getElementById('alerta-global');
    var listaProductos      = document.getElementById('lista-productos');
    var tablaCuerpo         = document.getElementById('tabla-cuerpo');
    var numeroRegistros     = document.getElementById('numero-registros');
    var contadorCaracteres  = document.getElementById('contador-caracteres');

    // Referencias a elementos del formulario de contacto
    var formularioContacto  = document.getElementById('formulario-contacto');
    var contactoNombre      = document.getElementById('contacto-nombre');
    var contactoCorreo      = document.getElementById('contacto-correo');
    var contactoAsunto      = document.getElementById('contacto-asunto');
    var contactoMensaje     = document.getElementById('contacto-mensaje');
    var alertaContacto      = document.getElementById('alerta-contacto');


    // ============================================================
    // 5. RENDERIZAR CATÁLOGO DESDE EL ARREGLO catalogoServicios
    //    Se usa forEach() para iterar el arreglo y crear una tarjeta
    //    por cada servicio con createElement + appendChild.
    //    CONDICIÓN: si el arreglo está vacío, muestra un mensaje.
    // ============================================================
    function renderizarCatalogo() {
        var contenedor = document.getElementById('contenedor-catalogo');
        contenedor.innerHTML = ''; // Limpiar antes de renderizar

        // CONDICIÓN: verificar si hay servicios disponibles en el arreglo
        if (catalogoServicios.length === 0) {
            // Si no hay datos, mostrar mensaje condicional
            var msgVacio = document.createElement('p');
            msgVacio.className = 'text-center text-warning';
            msgVacio.textContent = '⚠️ No hay servicios disponibles en este momento.';
            contenedor.appendChild(msgVacio);
            return; // Salir de la función
        }

        // Estructura repetitiva: forEach itera cada servicio del arreglo
        catalogoServicios.forEach(function (servicio) {

            // Crear columna responsiva Bootstrap
            var col = document.createElement('div');
            col.className = 'col-md-4 col-sm-6';

            // Crear tarjeta del servicio
            var card = document.createElement('div');
            card.className = 'card h-100 shadow-sm card-catalogo';

            // Cuerpo de la tarjeta
            var cardBody = document.createElement('div');
            cardBody.className = 'card-body';

            // Icono + título
            var titulo = document.createElement('h5');
            titulo.className = 'card-title';
            titulo.textContent = servicio.icono + ' ' + servicio.titulo;

            // Descripción del servicio
            var descripcion = document.createElement('p');
            descripcion.className = 'card-text small';
            descripcion.textContent = servicio.descripcion;

            // Badge con color según categoría
            var badge = document.createElement('span');
            badge.className = 'badge ' + servicio.badge + ' mt-2';
            badge.textContent = 'Servicio #' + servicio.id;

            // Ensamblar tarjeta con appendChild
            cardBody.appendChild(titulo);
            cardBody.appendChild(descripcion);
            cardBody.appendChild(badge);
            card.appendChild(cardBody);
            col.appendChild(card);
            contenedor.appendChild(col);
        });
    }

    // Llamar a la función al cargar la página para mostrar el catálogo
    renderizarCatalogo();


    // ============================================================
    // 6. ACTUALIZAR CONTADOR DE PRODUCTOS
    //    Muestra el total actual en el badge #numero-registros.
    // ============================================================
    function actualizarContador() {
        numeroRegistros.textContent = totalRegistros;
    }


    // ============================================================
    // 7. RENDERIZAR TABLA Y TARJETAS DESDE EL ARREGLO productosRegistrados
    //    Estructura repetitiva: forEach recorre el arreglo completo
    //    y reconstruye la tabla y las tarjetas cada vez que hay un cambio.
    //    CONDICIÓN: si no hay productos, muestra una fila de aviso.
    // ============================================================
    function renderizarProductos() {

        // --- Reconstruir tabla ---
        tablaCuerpo.innerHTML = '';

        // CONDICIÓN: si el arreglo está vacío, mostrar fila de aviso
        if (productosRegistrados.length === 0) {
            var filaVacia = document.createElement('tr');
            var celdaVacia = document.createElement('td');
            celdaVacia.colSpan = 4;
            celdaVacia.className = 'text-center text-secondary fst-italic';
            celdaVacia.textContent = 'No hay productos registrados aún. Usa el formulario para agregar.';
            filaVacia.appendChild(celdaVacia);
            tablaCuerpo.appendChild(filaVacia);
        } else {
            // Estructura repetitiva: recorrer el arreglo para crear filas
            productosRegistrados.forEach(function (producto, indice) {
                var fila = document.createElement('tr');

                // Celda: número de orden
                var celdaNum = document.createElement('td');
                celdaNum.textContent = indice + 1;

                // Celda: nombre del producto
                var celdaNombre = document.createElement('td');
                celdaNombre.textContent = producto.nombre;

                // Celda: categoría con badge
                var celdaCategoria = document.createElement('td');
                var badgeCat = document.createElement('span');
                badgeCat.className = 'badge bg-secondary';
                badgeCat.textContent = producto.categoria;
                celdaCategoria.appendChild(badgeCat);

                // Celda: botón eliminar de la tabla
                var celdaAccion = document.createElement('td');
                var btnEliminarFila = document.createElement('button');
                btnEliminarFila.type = 'button';
                btnEliminarFila.className = 'btn btn-outline-danger btn-sm';
                btnEliminarFila.textContent = '🗑 Eliminar';

                // Evento click: eliminar del arreglo por índice y re-renderizar
                btnEliminarFila.addEventListener('click', function () {
                    eliminarProducto(indice);
                });

                celdaAccion.appendChild(btnEliminarFila);
                fila.appendChild(celdaNum);
                fila.appendChild(celdaNombre);
                fila.appendChild(celdaCategoria);
                fila.appendChild(celdaAccion);
                tablaCuerpo.appendChild(fila);
            });
        }

        // --- Reconstruir tarjetas de detalle ---
        listaProductos.innerHTML = '';

        // Estructura repetitiva: forEach para tarjetas de detalle
        productosRegistrados.forEach(function (producto, indice) {

            var col = document.createElement('div');
            col.className = 'col-12';

            var card = document.createElement('div');
            card.className = 'card card-producto shadow-sm';

            var cardBody = document.createElement('div');
            cardBody.className = 'card-body d-flex justify-content-between align-items-start flex-wrap gap-2';

            var textoDiv = document.createElement('div');
            textoDiv.className = 'flex-grow-1';

            var titulo = document.createElement('h6');
            titulo.className = 'card-title mb-1 text-info fw-bold';
            titulo.textContent = producto.nombre;

            var desc = document.createElement('p');
            desc.className = 'card-text small mb-2';
            desc.textContent = producto.descripcion;

            var badge = document.createElement('span');
            badge.className = 'badge bg-secondary me-2';
            badge.textContent = producto.categoria;

            // CONDICIÓN: mostrar etiqueta especial si la descripción es larga
            if (producto.descripcion.length > 80) {
                var etiquetaDetalle = document.createElement('span');
                etiquetaDetalle.className = 'badge bg-info text-dark';
                etiquetaDetalle.textContent = '✔ Descripción detallada';
                textoDiv.appendChild(titulo);
                textoDiv.appendChild(desc);
                textoDiv.appendChild(badge);
                textoDiv.appendChild(etiquetaDetalle);
            } else {
                textoDiv.appendChild(titulo);
                textoDiv.appendChild(desc);
                textoDiv.appendChild(badge);
            }

            // Botón eliminar de la tarjeta
            var btnEliminar = document.createElement('button');
            btnEliminar.type = 'button';
            btnEliminar.className = 'btn btn-outline-danger btn-sm align-self-center';
            btnEliminar.textContent = '🗑 Eliminar';

            // Evento click: eliminar por índice y re-renderizar todo
            btnEliminar.addEventListener('click', function () {
                eliminarProducto(indice);
            });

            cardBody.appendChild(textoDiv);
            cardBody.appendChild(btnEliminar);
            card.appendChild(cardBody);
            col.appendChild(card);
            listaProductos.appendChild(col);
        });
    }

    // Llamar al cargar para mostrar el estado inicial (tabla vacía con aviso)
    renderizarProductos();


    // ============================================================
    // 8. ELIMINAR PRODUCTO DEL ARREGLO
    //    Se usa splice() para quitar el elemento en el índice dado,
    //    luego se actualiza el contador y se re-renderiza todo.
    // ============================================================
    function eliminarProducto(indice) {
        productosRegistrados.splice(indice, 1);
        totalRegistros = productosRegistrados.length;
        actualizarContador();
        renderizarProductos(); // Re-renderizar tabla y tarjetas
    }


    // ============================================================
    // SEMANA 6 — FUNCIONES DE VALIDACIÓN (se conservan íntegras)
    // ============================================================

    // Aplica clase is-valid + muestra mensaje de éxito
    function marcarValido(campo, idOk, mensaje) {
        campo.classList.remove('is-invalid');
        campo.classList.add('is-valid');
        if (idOk) {
            var div = document.getElementById(idOk);
            if (div) div.textContent = mensaje;
        }
    }

    // Aplica clase is-invalid + muestra mensaje de error
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

    // Muestra alerta Bootstrap global y la oculta a los 5 segundos
    function mostrarAlertaGlobal(divAlerta, tipo, texto) {
        divAlerta.className = 'alert alert-' + tipo;
        divAlerta.textContent = texto;
        setTimeout(function () {
            divAlerta.className = 'alert d-none';
            divAlerta.textContent = '';
        }, 5000);
    }

    // Valida campo nombre: obligatorio + mínimo 3 caracteres
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
    // SEMANA 6 — EVENTOS EN TIEMPO REAL (input) Y BLUR
    // ============================================================

    // Evento input: validar mientras el usuario escribe
    campoNombre.addEventListener('input', function () { validarNombre(); });

    // Evento input: actualizar contador de caracteres + validar descripción
    campoDescripcion.addEventListener('input', function () {
        contadorCaracteres.textContent = campoDescripcion.value.length;
        validarDescripcion();
    });

    // Evento input: validar categoría al cambiar selección
    campoCategoria.addEventListener('input', function () { validarCategoria(); });

    // Evento blur: validar al salir de cada campo sin completarlo
    campoNombre.addEventListener('blur',      function () { validarNombre(); });
    campoDescripcion.addEventListener('blur', function () { validarDescripcion(); });
    campoCategoria.addEventListener('blur',   function () { validarCategoria(); });


    // ============================================================
    // EVENTO SUBMIT — Formulario de gestión de productos
    //    preventDefault() evita la recarga de la página.
    //    Solo se registra si las 3 validaciones son correctas.
    //    El nuevo producto se agrega al arreglo con push().
    // ============================================================
    formularioProducto.addEventListener('submit', function (evento) {
        evento.preventDefault(); // Evitar recarga de la página

        // Ejecutar todas las validaciones
        var nombreValido      = validarNombre();
        var descripcionValida = validarDescripcion();
        var categoriaValida   = validarCategoria();

        // CONDICIÓN: solo registrar si todos los campos son válidos
        if (nombreValido && descripcionValida && categoriaValida) {

            // Crear objeto con los datos del nuevo producto
            var nuevoProducto = {
                nombre:      campoNombre.value.trim(),
                descripcion: campoDescripcion.value.trim(),
                categoria:   campoCategoria.value
            };

            // Agregar el objeto al arreglo productosRegistrados
            productosRegistrados.push(nuevoProducto);

            // Actualizar el contador total
            totalRegistros = productosRegistrados.length;
            actualizarContador();

            // Re-renderizar tabla y tarjetas con el nuevo dato
            renderizarProductos();

            // Mostrar alerta de éxito
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

        } else {
            // CONDICIÓN: hay errores → mostrar alerta de error
            mostrarAlertaGlobal(
                alertaGlobal,
                'danger',
                '⚠️ Corrige los errores indicados antes de registrar.'
            );
        }
    });


    // ============================================================
    // SEMANA 6 — EVENTO SUBMIT del formulario de contacto
    //    preventDefault() + validaciones + alerta de resultado.
    // ============================================================
    formularioContacto.addEventListener('submit', function (evento) {
        evento.preventDefault();

        var nombre  = contactoNombre.value.trim();
        var correo  = contactoCorreo.value.trim();
        var asunto  = contactoAsunto.value.trim();
        var mensaje = contactoMensaje.value.trim();
        var hayError = false;

        var formatoCorreo = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

        // Validar nombre
        if (nombre === '') {
            marcarInvalido(contactoNombre, 'error-contacto-nombre', 'El nombre es obligatorio.');
            hayError = true;
        } else {
            marcarValido(contactoNombre, null, '');
        }

        // Validar correo con expresión regular
        if (correo === '') {
            marcarInvalido(contactoCorreo, 'error-contacto-correo', 'El correo es obligatorio.');
            hayError = true;
        } else if (!formatoCorreo.test(correo)) {
            marcarInvalido(contactoCorreo, 'error-contacto-correo', 'Ingresa un correo electrónico válido.');
            hayError = true;
        } else {
            marcarValido(contactoCorreo, null, '');
        }

        // Validar asunto
        if (asunto === '') {
            marcarInvalido(contactoAsunto, 'error-contacto-asunto', 'El asunto es obligatorio.');
            hayError = true;
        } else {
            marcarValido(contactoAsunto, null, '');
        }

        // Validar mensaje
        if (mensaje === '') {
            marcarInvalido(contactoMensaje, 'error-contacto-mensaje', 'El mensaje es obligatorio.');
            hayError = true;
        } else {
            marcarValido(contactoMensaje, null, '');
        }

        // CONDICIÓN: sin errores → éxito; con errores → alerta de error
        if (!hayError) {
            mostrarAlertaGlobal(
                alertaContacto,
                'success',
                '✅ Mensaje enviado. ¡Gracias, ' + nombre + '! Te contactaremos pronto.'
            );
            formularioContacto.reset();
            limpiarEstado(contactoNombre);
            limpiarEstado(contactoCorreo);
            limpiarEstado(contactoAsunto);
            limpiarEstado(contactoMensaje);
        } else {
            mostrarAlertaGlobal(
                alertaContacto,
                'danger',
                '⚠️ Por favor completa correctamente todos los campos.'
            );
        }
    });

    // Validaciones blur para el formulario de contacto (Semana 6)
    contactoNombre.addEventListener('blur', function () {
        if (contactoNombre.value.trim() === '') {
            marcarInvalido(contactoNombre, 'error-contacto-nombre', 'El nombre es obligatorio.');
        } else { marcarValido(contactoNombre, null, ''); }
    });

    var reCorreo = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    contactoCorreo.addEventListener('blur', function () {
        var val = contactoCorreo.value.trim();
        if (val === '') {
            marcarInvalido(contactoCorreo, 'error-contacto-correo', 'El correo es obligatorio.');
        } else if (!reCorreo.test(val)) {
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