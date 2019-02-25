window.onload = function(){
  console.log("entra a rellenar");
  var ipt_name_person = document.getElementById("id_name_person").setAttribute('value', "{{document.name_person|escapejs}}");
  var ipt_num_folio = document.getElementById("id_num_folio").setAttribute('value', "{{document.num_folio|escapejs}}");
  //var ipt_type_name = document.getElementById("name").setAttribute('value', "{{document.type.name|escapejs}}");




  for(var field in document){
    //name_person.value(field.name_person);

  }



}
