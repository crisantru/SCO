
	var $j = jQuery.noConflict();

	$j(document).ready(function(){
	//rule for validate select
	$j.validator.addMethod("valueNotEquals", function(value, element, arg){
  // I use element.value instead value here, value parameter was always null
	    return arg != element.value;
	}, "Value must not equal arg.");
	//validate fields form
	$j('#post_document').validate({
		rules:{
			//field on form
			name_person:{
				required:true,
				minlength:20,
			},
			//field on form
			num_folio:{
				required: true,
				minlength: 2,
				maxlength: 4,
				digits: true,
			},
			//field on form
			consecutive:{
				required: true,
				digits: true,
				minlength: 4,
				maxlength: 4,
			},
			//field on form
			name:{
				required:true,
				valueNotEquals: "Seleccion",
			},
			//field on form
			limit_answer:{
				required: true,
				digits: true,
			},
			//field on form
			name_authority :{
				required: true,
				valueNotEquals: "Seleccion",
			},
			//field on form
			status:{
				required:true,
				valueNotEquals: "Seleccion",
			},
			//field on form
			manager_process:{
				required:true,
				valueNotEquals: "Seleccion",
			},
			//field on form
			derivate_area:{
				required:true,
				valueNotEquals: "Seleccion",
			},
			//fields special for pensiones_alimenticias
			ordinary_judg:{
				required: true,
				minlength: 11,
				maxlength: 14,

			},
			beneficiary:{
				required: true,
				minlength: 10,

			},
			disposition_type:{
				required: true,
				valueNotEquals: "Seleccion",
			},
			pension_type:{
				required: true,
			}
		},
		//messages for Selects
		messages: {
        name: { valueNotEquals: "Por favor selecciona un elemento" },
				name_authority : { valueNotEquals: "Por favor selecciona un elemento" },
				status: { valueNotEquals: "Por favor selecciona un elemento" },
				manager_process: { valueNotEquals: "Por favor selecciona un elemento" },
				derivate_area: { valueNotEquals: "Por favor selecciona un elemento" },
				disposition_type: { valueNotEquals: "Por favor selecciona un elemento" },
    },
		//when submit button
		submitHandler: function(form){
			$j('#post_document').on('submit', function(event){
				event.preventDefault();
				console.log("form submitted!");

				$.ajax({
					url: $j(this).attr('action'),
					type: $j(this).attr('method'),	//type POST
					//data from id form
					data: $j("#post_document").serialize(),

					success: function(json){
						console.log("json: " + json.result);
						//clean fields input
						$j("input:text").val('');
						//change values of Select
						$j("select").val("Seleccion");
						//show alert in browser
						alert(json.result)
						//alert(json.result + "\n" + json.document)
						console.log("success");
						//refresh the page
						location.reload(true);
					},
					/*error : function(xhr, errmsg, err){
						console.log("ERROR");
						$j('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
	                " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
	            console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
					}*/
				});
			});
		}
	});
});
