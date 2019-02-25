var $j = jQuery.noConflict();

$j(function(){
   $j("#authority_name").autocomplete({
    source: "{% url 'get_authorities' %}",
    select: function (event, ui) { //item selected
      AutoCompleteSelectHandler(event, ui)
    },
    minLength: 1,
  });
 });

function AutoCompleteSelectHandler(event, ui){
  var selectedObj = ui.item;
}

window.onload = function(){
     var materia = document.getElementById("Materias");
     var submateria = document.getElementById("subMaterias");

     materia.addEventListener('change', function(){

       if(document.getElementById('datosPesiones')){
         final_content.nextElementSibling.remove();
       }

       if(materia.value == "Pensiones_Alimenticias"){
         //alert("entra a nuevo div");
         let final_content = document.getElementById("final_content");
         let juicio_ord = "{{form5.ordinary_judg|escapejs}}"
         let beneficiary = "{{form5.beneficiary|escapejs}}"
         let disposition_type = "{{form5.disposition_type|escapejs}}"
         let pension_type = "{{form5.pension_type|escapejs}}"
         let date_efect = "{{form5.date_efect|escapejs}}"
         //DIV
         var divDatosPensiones = document.createElement("DIV");
         divDatosPensiones.setAttribute("class", "container-fluid");
         divDatosPensiones.setAttribute("id", "datosPesiones");
         divDatosPensiones.innerHTML = "<br><h5>DATOS PROPIOS DEL OFICIO<br>(PENSIONES ALIMENTICIAS)</h5><hr>"
         + "<div class=" + "label" + ">Juicio Ordinario: </div>"
         + "<div class=" + "input" + ">" + juicio_ord + "</div>"
         + "<div class=" + "label" + ">Beneficiario: </div>"
         + "<div class=" + "input" + ">" + beneficiary + "</div>"
         + "<div class=" + "label" + ">Tipo de Disposición: </div>"
         + "<div class=" + "input" + ">" + disposition_type + "</div>"
         + "<div class=" + "label" + ">Tipo de Pensión: </div>"
         + "<div class=" + "input" + ">" + pension_type + "</div>"
         + "<br><br><br>";
         insertAfter(final_content, divDatosPensiones);
       }else{
         //final_content.nextElementSibling.remove();
       }
     });

     function insertAfter(e,i){
         if(e.nextSibling){
             e.parentNode.insertBefore(i,e.nextSibling);
         } else {
             e.parentNode.appendChild(i);
         }
     }

   }
