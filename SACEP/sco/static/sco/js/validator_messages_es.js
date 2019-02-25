var $j = jQuery.noConflict();

$j.extend( $j.validator.messages, {
	required: "Campo es Obligatorio.",
	remote: "Por favor, rellena este campo.",
	email: "Escribe una dirección de correo válida.",
	url: "Por favor, escribe una URL válida.",
	date: "Fecha Inválida.",
	dateISO: "Por favor, escribe una fecha (ISO) válida.",
	number: "Por favor, escribe un número válido.",
	digits: "Sólo se admiten dígitos.",
	creditcard: "Por favor, escribe un número de tarjeta válido.",
	equalTo: "Por favor, escribe el mismo valor de nuevo.",
	extension: "Por favor, escribe un valor con una extensión aceptada.",
	maxlength: $j.validator.format( "No más de {0} caracteres." ),
	minlength: $j.validator.format( "Al menos {0} caracteres." ),
	rangelength: $j.validator.format( "Por favor, escribe un valor entre {0} y {1} caracteres." ),
	range: $j.validator.format( "Por favor, escribe un valor entre {0} y {1}." ),
	max: $j.validator.format( "Por favor, escribe un valor menor o igual a {0}." ),
	min: $j.validator.format( "Por favor, escribe un valor mayor o igual a {0}." ),
	nifES: "Por favor, escribe un NIF válido.",
	nieES: "Por favor, escribe un NIE válido.",
	cifES: "Por favor, escribe un CIF válido."

} );
