'use strict'

var materia = document.getElementById("Materias");
var rdb_status = document.getElementById("document_status");
var rdb_status2 = document.getElementById("document_status2");

//validate radio buttons filter
/*materia.addEventListener('change', function(){
  if(materia.value == "Pensiones_Alimenticias"){
      rdb_status.disabled = true;
      rdb_status.checked = false;
      rdb_status2.disabled = true;
      rdb_status2.checked = false;
  }else{
    rdb_status.disabled = false;
    rdb_status2.disabled = false;
  }

});*/

function insertItems() {
  var materia = document.getElementById("Materias").value;
  var submateria = document.getElementById("subMaterias");
  let subPensioAlim = ["Inclusión", "Cancelación", "Modificación"];
  //var juicioAmparo = ["Informe_Previo", "Informe_Justificado"];

  if (materia == "Informes_Autoridad"){

  }

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

  }else{
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

//asigna value a subtype pensiones_alimenticias
function submaterias(){
  let subtype = document.getElementById("subMaterias");
  subtype.setAttribute("value", subtype.value)
  console.log(subtype.value);
}
