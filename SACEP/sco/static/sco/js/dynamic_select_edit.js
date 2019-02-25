
	var submateria = document.getElementById("subMaterias");

	//URGENT DEBUGGUER
	function insertItems() {
		//console.log("entra a insertItems: " + materia);

		var materia = document.getElementById("Materias").value;
		var submateria = document.getElementById("subMaterias");
		var subPensioAlim = ["Inclusiones", "Cancelaciones", "Modificaciones"];
		var juicioAmparo = ["Incidente_Suspension", "Informe_Justificado"];

		/*if(materia == "Seleccion"){
				document.getElementById("Materias").remove(0);
		}*/

		definirRespuestaDias(materia);

		if (materia == "Pensiones Alimenticias") {

			submateria.disabled = false;

			if(submateria.length > 0){
				removeItems();
			}

			for(var i in subPensioAlim){
				document.getElementById("subMaterias").innerHTML +=
				"<option value ='" + subPensioAlim[i] + "'>" + subPensioAlim[i] +
				"</option>";

			}




		}else if (materia == "Juicio de Amparo") {
			submateria.disabled = false;
			if(submateria.length > 0){
				removeItems();
			}
			for(var i in juicioAmparo){
				document.getElementById("subMaterias").innerHTML +=
				"<option value ='" + juicioAmparo[i] + "'>" + juicioAmparo[i] +
				"</option>";

			}
		}else {
		    submateria.readonly = true;
				submateria.setAttribute("value", "None");
				removeItems();
		}

		function removeItems(){
			for(var i=submateria.length; i >= 0; i--){
				submateria.remove(i);
			}
		}
	}

	function definirRespuestaDias(materia){
		var limite_respuesta = document.getElementById("limite_respuesta")

		var oficio = {
			// pensiones alimenticias
			Inclusiones:"5",
			Cancelaciones:"5",
			Modificaciones:"5",
			// juicios de amparo
			Incidente_Suspension: "2",
			Informe_Justificado: "15",
			// oficios en gral.
			informe_autoridad: "15",
			dictamen_incobrabilidad: "30",
			oficios_varios: "30",
			negativa_peritos: "15",
			juicios_civiles: "9",
			asuntos_penales: "3",
			recuperacion_fianzas: "7",
			depositaria_infiel: "30",
		}

		dias = oficio[materia];
		document.getElementById("limite_respuesta").value = dias;
		console.log(document.getElementById("limite_respuesta").value);
		limite_respuesta.setAttribute("value", dias);
		set_end_days(dias);

		return dias;
	}

	function submaterias(){
		var submateria = document.getElementById("subMaterias").value;
		var subtype = document.getElementById("subMaterias");
		definirRespuestaDias(submateria)
		subtype.setAttribute("value", subtype.value)

		console.log(subtype.value);
	}

	//fecha de termnio
	function set_end_days(dias){
		var days = parseInt(dias);
		var date = new Date();
		date.setDate(date.getDate() + days);
		var formatDate = date.toLocaleDateString();
		document.getElementById("termino").value = formatDate;

	}
