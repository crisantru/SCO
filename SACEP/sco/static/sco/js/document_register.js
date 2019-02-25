var materia = document.getElementById("Materias");
var submateria = document.getElementById("subMaterias");

//URGENT DEBUGGUER
function insertItems() {
  console.log("entra a insertItems: " + materia);

  var materia = document.getElementById("Materias").value;
  var submateria = document.getElementById("subMaterias");
  var subPensioAlim = ["Inclusiones", "Cancelaciones", "Modificaciones"];
  var juicioAmparo = ["Informe_Previo", "Informe_Justificado"];

  if (materia == "Pensiones_Alimenticias"){
    submateria.disabled = false;

    if(submateria.length > 0){
      removeItems();
    }

    for(var i in subPensioAlim){
      document.getElementById("subMaterias").innerHTML +=
      "<option value ='" + subPensioAlim[i] + "'>" + subPensioAlim[i] +
      "</option>";
    }
  }else if (materia == "Juicios_Amparo"){
    submateria.disabled = false;
    if(submateria.length > 0){
      removeItems();
    }
    for(var i in juicioAmparo){
      document.getElementById("subMaterias").innerHTML +=
      "<option value ='" + juicioAmparo[i] + "'>" + juicioAmparo[i] +
      "</option>";

    }
  }else{
      submateria.readonly = true;
      submateria.setAttribute("value", "None");
      removeItems();
  }

  definirRespuestaDias(materia);

  function removeItems(){
    for(var i=submateria.length; i >= 0; i--){
      submateria.remove(i);
    }
  }
}

function definirRespuestaDias(materia){
  console.log("DEFINIR RESPUESTA DIAS: " + materia);
  var limite_respuesta = document.getElementById("limite_respuesta")

  var oficio = {
    // pensiones alimenticias
    Inclusiones:"5",
    Cancelaciones:"5",
    Modificaciones:"5",
    // juicios de amparo
    Informe_Previo: "2",
    Informe_Justificado: "15",
    // oficios en gral.
    Asuntos_Administrativos: "10",
    Asuntos_Civiles: "9",
    Asuntos_Penales: "3",
    Depositaria_Infiel: "30",
    Expedientes_Penales: "3",
    Informes_Autoridad: "15",
    //Juicio_de_Amparo: "10",
    Juicios_Civiles: "9",
    Negativa_Peritos: "15",
    Oficios_Varios: "30",
    Recuperacion_Fianzas: "7",
  }

  dias = oficio[materia];
  console.log(dias);
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
  if(document.getElementById("datosPensiones")){
    console.log("datosPensiones : ON");
    var input_pension = document.getElementById("id_pension_type");

    if(subtype.value == "Inclusiones"){
      console.log("entra if");
      input_pension.value = "Inclusión";
      input_pension.setAttribute("value", "Inclusión")
    }else if(subtype.value == "Modificaciones"){
      input_pension.value = "Modificación";
      input_pension.setAttribute("value", "Modificación")
    }else{
      input_pension.value = "Cancelación";
      input_pension.setAttribute("value", "Cancelación")
    }

  }
}
//fecha de termnio
function set_end_days(dias){
  console.log("Entra a set Days");
  var days = parseInt(dias);
  var date = new Date();
  date.setDate(date.getDate() + days);
  console.log("date default: " + date);
  //var formatDate = date.toLocaleDateString();
  var formatDate = date.toISOString().substring(0, 10);
  console.log("formatDate: " + formatDate);
  var termino = document.getElementById("termino");
  termino.setAttribute("value", formatDate);
}
