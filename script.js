// script.js — Narvi Collector Scale Models

var totalRegistros = 0;

function actualizarContador() {
    document.getElementById('numero-registros').textContent = totalRegistros;
}

function eliminarProducto(columna) {
    columna.parentNode.removeChild(columna);
    totalRegistros = totalRegistros - 1;
    actualizarContador();
}

function registrarProducto() {
    var nombre      = document.getElementById('campo-nombre').value.trim();
    var descripcion = document.getElementById('campo-descripcion').value.trim();
    var categoria   = document.getElementById('campo-categoria').value;
    var alerta      = document.getElementById('mensaje-validacion');

    if (nombre === '' || descripcion === '' || categoria === '') {
        alerta.className = 'alert alert-danger';
        alerta.textContent = '⚠️ Todos los campos son obligatorios.';
        setTimeout(function(){ alerta.className = 'alert d-none'; }, 4000);
        return false;
    }

    // Crear columna
    var columna = document.createElement('div');
    columna.className = 'col-12 mb-3';

    // Crear tarjeta
    var tarjeta = document.createElement('div');
    tarjeta.className = 'card shadow-sm border-start border-primary border-4';

    var cuerpo = document.createElement('div');
    cuerpo.className = 'card-body d-flex justify-content-between align-items-start flex-wrap gap-2';

    var textoDiv = document.createElement('div');
    textoDiv.className = 'flex-grow-1';

    var titulo = document.createElement('h5');
    titulo.className = 'card-title mb-1 text-primary';
    titulo.textContent = nombre;

    var desc = document.createElement('p');
    desc.className = 'card-text mb-1';
    desc.textContent = descripcion;

    var badge = document.createElement('span');
    badge.className = 'badge bg-secondary';
    badge.textContent = categoria;

    textoDiv.appendChild(titulo);
    textoDiv.appendChild(desc);
    textoDiv.appendChild(badge);

    var btnEliminar = document.createElement('button');
    btnEliminar.type = 'button';
    btnEliminar.className = 'btn btn-outline-danger btn-sm';
    btnEliminar.textContent = 'Eliminar';
    btnEliminar.onclick = function() { eliminarProducto(columna); };

    cuerpo.appendChild(textoDiv);
    cuerpo.appendChild(btnEliminar);
    tarjeta.appendChild(cuerpo);
    columna.appendChild(tarjeta);

    document.getElementById('lista-productos').appendChild(columna);

    // Actualizar contador
    totalRegistros = totalRegistros + 1;
    actualizarContador();

    // Limpiar formulario
    document.getElementById('campo-nombre').value = '';
    document.getElementById('campo-descripcion').value = '';
    document.getElementById('campo-categoria').value = '';

    // Mensaje éxito
    alerta.className = 'alert alert-success';
    alerta.textContent = '✅ Producto "' + nombre + '" registrado. Total: ' + totalRegistros;
    setTimeout(function(){ alerta.className = 'alert d-none'; }, 4000);

    return false;
}

function enviarContacto() {
    var nombre  = document.getElementById('contacto-nombre').value.trim();
    var correo  = document.getElementById('contacto-correo').value.trim();
    var asunto  = document.getElementById('contacto-asunto').value.trim();
    var mensaje = document.getElementById('contacto-mensaje').value.trim();
    var alerta  = document.getElementById('mensaje-contacto');

    if (nombre === '' || correo === '' || asunto === '' || mensaje === '') {
        alerta.className = 'alert alert-danger';
        alerta.textContent = '⚠️ Por favor completa todos los campos.';
        setTimeout(function(){ alerta.className = 'alert d-none'; }, 4000);
        return false;
    }

    var formatoCorreo = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!formatoCorreo.test(correo)) {
        alerta.className = 'alert alert-warning';
        alerta.textContent = '⚠️ El correo electrónico no es válido.';
        setTimeout(function(){ alerta.className = 'alert d-none'; }, 4000);
        return false;
    }

    alerta.className = 'alert alert-success';
    alerta.textContent = '✅ Mensaje enviado. ¡Gracias, ' + nombre + '!';
    setTimeout(function(){ alerta.className = 'alert d-none'; }, 4000);

    document.getElementById('formulario-contacto').reset();
    return false;
}