
	var $j = jQuery.noConflict();

	$j(document).ready(function(){
	//rule for validate select
	$j.validator.addMethod("valueNotEquals", function(value, element, arg){
  // I use element.value instead value here, value parameter was always null
	    return arg != element.value;
	}, "Value must not equal arg.");
	//validate fields form
	$j('#form-update').validate({
		rules:{
			//field on form
			status:{
				valueNotEquals: "Seleccion",
			},
      file_pdf:{
        required: true,
      },
      observations:{
        required: true,
      }
		},
		//messages for Selects
		messages: {
        status: { valueNotEquals: "Por favor selecciona un elemento" },
    },
    //when submit button
		/*submitHandler: function(form){
			$j('#form-update').on('submit', function(event){
				event.preventDefault();
				console.log("form submitted!");

				$.ajax({
					url: $j(this).attr('action'),
					type: $j(this).attr('method'),	//type POST
					//data from id form
					data: $j("#form-update").serialize(),

					success: function(json){
						console.log("json: " + json.result);
						//clean fields input
						//$j("input:text").val('');
						//$j("input:password").val('');
						//change values of Select
						$j("select").val("Seleccion");
						//show alert in browser
						alert(json.result)
						console.log("success");
            //refresh the page
            location.reload(true);
					},

				});
			});
		}*/
	});
});
