// ============================================================
// script.js — Narvi Collector Scale Models
// Semana 6: Validaciones dinámicas con JavaScript
// Estudiante: Nancy Campos Basurto
// ============================================================


// ============================================================
// VARIABLE GLOBAL: contador de productos registrados
// ============================================================
var totalRegistros = 0;


// ============================================================
// ESPERAR A QUE EL DOM ESTÉ COMPLETAMENTE CARGADO
// Esto garantiza que todos los elementos HTML existen
// antes de que JavaScript intente acceder a ellos
// ============================================================
document.addEventListener('DOMContentLoaded', function () {

    // ----------------------------------------------------------
    // REFERENCIAS A LOS ELEMENTOS DEL FORMULARIO DE GESTIÓN
    // ----------------------------------------------------------
    var formularioProducto   = document.getElementById('formulario-producto');
    var campoNombre          = document.getElementById('campo-nombre');
    var campoDescripcion     = document.getElementById('campo-descripcion');
    var campoCategoria       = document.getElementById('campo-categoria');
    var alertaGlobal         = document.getElementById('alerta-global');
    var listaProductos       = document.getElementById('lista-productos');
    var numeroRegistros      = document.getElementById('numero-registros');
    var contadorCaracteres   = document.getElementById('contador-caracteres');

    // ----------------------------------------------------------
    // REFERENCIAS A LOS ELEMENTOS DEL FORMULARIO DE CONTACTO
    // ----------------------------------------------------------
    var formularioContacto   = document.getElementById('formulario-contacto');
    var contactoNombre       = document.getElementById('contacto-nombre');
    var contactoCorreo       = document.getElementById('contacto-correo');
    var contactoAsunto       = document.getElementById('contacto-asunto');
    var contactoMensaje      = document.getElementById('contacto-mensaje');
    var alertaContacto       = document.getElementById('alerta-contacto');


    // ==========================================================
    // FUNCIONES DE UTILIDAD REUTILIZABLES
    // ==========================================================

    /**
     * marcarValido()
     * Aplica la clase Bootstrap is-valid a un campo
     * y muestra el mensaje de éxito debajo de él.
     *
     * @param {HTMLElement} campo   - El input, textarea o select
     * @param {string}      idOk    - ID del div de mensaje de éxito
     * @param {string}      mensaje - Texto a mostrar
     */
    function marcarValido(campo, idOk, mensaje) {
        campo.classList.remove('is-invalid');
        campo.classList.add('is-valid');
        if (idOk) {
            var divOk = document.getElementById(idOk);
            if (divOk) divOk.textContent = mensaje;
        }
    }

    /**
     * marcarInvalido()
     * Aplica la clase Bootstrap is-invalid a un campo
     * y muestra el mensaje de error debajo de él.
     *
     * @param {HTMLElement} campo   - El input, textarea o select
     * @param {string}      idError - ID del div de mensaje de error
     * @param {string}      mensaje - Texto a mostrar
     */
    function marcarInvalido(campo, idError, mensaje) {
        campo.classList.remove('is-valid');
        campo.classList.add('is-invalid');
        if (idError) {
            var divError = document.getElementById(idError);
            if (divError) divError.textContent = mensaje;
        }
    }

    /**
     * limpiarEstado()
     * Quita las clases de validación de un campo (estado neutro).
     *
     * @param {HTMLElement} campo - El input, textarea o select
     */
    function limpiarEstado(campo) {
        campo.classList.remove('is-valid', 'is-invalid');
    }

    /**
     * mostrarAlertaGlobal()
     * Muestra un mensaje de alerta Bootstrap debajo del formulario.
     * Se oculta automáticamente luego de 5 segundos.
     *
     * @param {HTMLElement} divAlerta - El div contenedor de la alerta
     * @param {string}      tipo      - 'success' | 'danger' | 'warning'
     * @param {string}      mensaje   - Texto a mostrar
     */
    function mostrarAlertaGlobal(divAlerta, tipo, mensaje) {
        divAlerta.className = 'alert alert-' + tipo;
        divAlerta.textContent = mensaje;
        // Ocultar después de 5 segundos
        setTimeout(function () {
            divAlerta.className = 'alert d-none';
            divAlerta.textContent = '';
        }, 5000);
    }

    /**
     * actualizarContador()
     * Actualiza el número visible en el badge del contador.
     */
    function actualizarContador() {
        numeroRegistros.textContent = totalRegistros;
    }


    // ==========================================================
    // FUNCIONES DE VALIDACIÓN INDIVIDUALES POR CAMPO
    // Cada función valida un campo y retorna true/false
    // ==========================================================

    /**
     * validarNombre()
     * Reglas: no vacío, mínimo 3 caracteres.
     */
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

    /**
     * validarDescripcion()
     * Reglas: no vacía, mínimo 10 caracteres.
     */
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

    /**
     * validarCategoria()
     * Regla: debe seleccionarse una opción distinta de la vacía.
     */
    function validarCategoria() {
        var valor = campoCategoria.value;

        if (valor === '') {
            marcarInvalido(campoCategoria, 'error-categoria', 'Debes seleccionar una categoría.');
            return false;
        }
        marcarValido(campoCategoria, 'ok-categoria', '✓ Categoría seleccionada.');
        return true;
    }


    // ==========================================================
    // EVENTOS EN TIEMPO REAL — evento "input"
    // Se disparan mientras el usuario escribe o cambia el valor
    // ==========================================================

    // Validar nombre mientras el usuario escribe
    campoNombre.addEventListener('input', function () {
        validarNombre();
    });

    // Validar descripción mientras el usuario escribe
    // y actualizar el contador de caracteres en tiempo real
    campoDescripcion.addEventListener('input', function () {
        contadorCaracteres.textContent = campoDescripcion.value.length;
        validarDescripcion();
    });

    // Validar categoría cuando el usuario cambia la selección
    campoCategoria.addEventListener('input', function () {
        validarCategoria();
    });


    // ==========================================================
    // EVENTOS AL PERDER EL FOCO — evento "blur"
    // Se disparan cuando el usuario sale de un campo sin completarlo
    // ==========================================================

    // Al salir del campo nombre sin escribir
    campoNombre.addEventListener('blur', function () {
        validarNombre();
    });

    // Al salir del campo descripción sin escribir
    campoDescripcion.addEventListener('blur', function () {
        validarDescripcion();
    });

    // Al salir del select sin seleccionar
    campoCategoria.addEventListener('blur', function () {
        validarCategoria();
    });


    // ==========================================================
    // EVENTO SUBMIT — Formulario de gestión de productos
    // Se dispara al hacer clic en "Agregar Producto"
    // ==========================================================
    formularioProducto.addEventListener('submit', function (evento) {

        // preventDefault() evita que la página se recargue
        evento.preventDefault();

        // Ejecutar todas las validaciones al enviar
        var nombreValido      = validarNombre();
        var descripcionValida = validarDescripcion();
        var categoriaValida   = validarCategoria();

        // Solo registrar si los tres campos son válidos
        if (nombreValido && descripcionValida && categoriaValida) {

            // Obtener los valores limpios de los campos
            var nombre      = campoNombre.value.trim();
            var descripcion = campoDescripcion.value.trim();
            var categoria   = campoCategoria.value;

            // Crear y agregar la tarjeta del producto a la lista
            crearTarjetaProducto(nombre, descripcion, categoria);

            // Incrementar y actualizar el contador
            totalRegistros = totalRegistros + 1;
            actualizarContador();

            // Mostrar alerta de éxito
            mostrarAlertaGlobal(
                alertaGlobal,
                'success',
                '✅ Producto "' + nombre + '" registrado correctamente. Total: ' + totalRegistros
            );

            // Limpiar el formulario y restablecer estados de validación
            formularioProducto.reset();
            limpiarEstado(campoNombre);
            limpiarEstado(campoDescripcion);
            limpiarEstado(campoCategoria);
            contadorCaracteres.textContent = '0';

        } else {
            // Si hay errores, mostrar alerta de error general
            mostrarAlertaGlobal(
                alertaGlobal,
                'danger',
                '⚠️ Por favor corrige los errores indicados antes de registrar.'
            );
        }
    });


    // ==========================================================
    // FUNCIÓN: Crear tarjeta de producto con createElement
    // y appendChild — agrega el nuevo producto a la lista
    // ==========================================================
    function crearTarjetaProducto(nombre, descripcion, categoria) {

        // Columna responsiva Bootstrap
        var columna = document.createElement('div');
        columna.className = 'col-12 mb-3';

        // Tarjeta con borde izquierdo de color primario
        var tarjeta = document.createElement('div');
        tarjeta.className = 'card shadow-sm border-start border-primary border-4';

        // Cuerpo de la tarjeta
        var cuerpo = document.createElement('div');
        cuerpo.className = 'card-body d-flex justify-content-between align-items-start flex-wrap gap-2';

        // Bloque de texto con nombre, descripción y categoría
        var textoDiv = document.createElement('div');
        textoDiv.className = 'flex-grow-1';

        var titulo = document.createElement('h5');
        titulo.className = 'card-title mb-1 text-primary';
        titulo.textContent = nombre;

        var desc = document.createElement('p');
        desc.className = 'card-text mb-2 text-muted';
        desc.textContent = descripcion;

        var badge = document.createElement('span');
        badge.className = 'badge bg-secondary';
        badge.textContent = categoria;

        // Agregar elementos al bloque de texto usando appendChild
        textoDiv.appendChild(titulo);
        textoDiv.appendChild(desc);
        textoDiv.appendChild(badge);

        // Botón eliminar — type="button" evita que dispare el submit del form
        var btnEliminar = document.createElement('button');
        btnEliminar.type = 'button';
        btnEliminar.className = 'btn btn-outline-danger btn-sm align-self-center';
        btnEliminar.textContent = 'Eliminar';

        // Evento click para eliminar el registro de la lista
        btnEliminar.addEventListener('click', function () {
            listaProductos.removeChild(columna);
            totalRegistros = totalRegistros - 1;
            actualizarContador();
        });

        // Ensamblar la tarjeta completa con appendChild
        cuerpo.appendChild(textoDiv);
        cuerpo.appendChild(btnEliminar);
        tarjeta.appendChild(cuerpo);
        columna.appendChild(tarjeta);

        // Agregar la tarjeta al contenedor de la lista
        listaProductos.appendChild(columna);
    }


    // ==========================================================
    // EVENTO SUBMIT — Formulario de contacto
    // ==========================================================
    formularioContacto.addEventListener('submit', function (evento) {

        // Evitar recarga de la página
        evento.preventDefault();

        var nombre  = contactoNombre.value.trim();
        var correo  = contactoCorreo.value.trim();
        var asunto  = contactoAsunto.value.trim();
        var mensaje = contactoMensaje.value.trim();

        var hayError = false;

        // Validar campo nombre de contacto
        if (nombre === '') {
            marcarInvalido(contactoNombre, 'error-contacto-nombre', 'El nombre es obligatorio.');
            hayError = true;
        } else {
            marcarValido(contactoNombre, null, '');
        }

        // Validar campo correo con expresión regular
        var formatoCorreo = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (correo === '') {
            marcarInvalido(contactoCorreo, 'error-contacto-correo', 'El correo es obligatorio.');
            hayError = true;
        } else if (!formatoCorreo.test(correo)) {
            marcarInvalido(contactoCorreo, 'error-contacto-correo', 'Ingresa un correo electrónico válido.');
            hayError = true;
        } else {
            marcarValido(contactoCorreo, null, '');
        }

        // Validar campo asunto
        if (asunto === '') {
            marcarInvalido(contactoAsunto, 'error-contacto-asunto', 'El asunto es obligatorio.');
            hayError = true;
        } else {
            marcarValido(contactoAsunto, null, '');
        }

        // Validar campo mensaje
        if (mensaje === '') {
            marcarInvalido(contactoMensaje, 'error-contacto-mensaje', 'El mensaje es obligatorio.');
            hayError = true;
        } else {
            marcarValido(contactoMensaje, null, '');
        }

        // Si no hay errores, mostrar éxito y limpiar
        if (!hayError) {
            mostrarAlertaGlobal(
                alertaContacto,
                'success',
                '✅ Mensaje enviado correctamente. ¡Gracias, ' + nombre + '! Te contactaremos pronto.'
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

    // Validación en tiempo real para los campos de contacto (evento blur)
    contactoNombre.addEventListener('blur', function () {
        if (contactoNombre.value.trim() === '') {
            marcarInvalido(contactoNombre, 'error-contacto-nombre', 'El nombre es obligatorio.');
        } else {
            marcarValido(contactoNombre, null, '');
        }
    });

    contactoCorreo.addEventListener('blur', function () {
        var formatoCorreo = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        var val = contactoCorreo.value.trim();
        if (val === '') {
            marcarInvalido(contactoCorreo, 'error-contacto-correo', 'El correo es obligatorio.');
        } else if (!formatoCorreo.test(val)) {
            marcarInvalido(contactoCorreo, 'error-contacto-correo', 'Ingresa un correo válido.');
        } else {
            marcarValido(contactoCorreo, null, '');
        }
    });

    contactoAsunto.addEventListener('blur', function () {
        if (contactoAsunto.value.trim() === '') {
            marcarInvalido(contactoAsunto, 'error-contacto-asunto', 'El asunto es obligatorio.');
        } else {
            marcarValido(contactoAsunto, null, '');
        }
    });

    contactoMensaje.addEventListener('blur', function () {
        if (contactoMensaje.value.trim() === '') {
            marcarInvalido(contactoMensaje, 'error-contacto-mensaje', 'El mensaje es obligatorio.');
        } else {
            marcarValido(contactoMensaje, null, '');
        }
    });

}); // ← Fin de DOMContentLoaded