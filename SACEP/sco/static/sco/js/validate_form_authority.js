
	var $j = jQuery.noConflict();

	$j(document).ready(function(){
	//rule for validate select
	$j.validator.addMethod("valueNotEquals", function(value, element, arg){
  // I use element.value instead value here, value parameter was always null
	    return arg != element.value;
	}, "Value must not equal arg.");
	//validate fields form
	$j('#post_authority').validate({
		rules:{
			//field on form
			category:{
				required:true,
				valueNotEquals: "Seleccion",
			},
			//field on form
			name_authority:{
				required: true,
				minlength: 25,
			},
			//field on form
			city:{
				required:true,
				valueNotEquals: "Seleccion",
			},
		},
		//messages for Selects
		messages: {
        category: { valueNotEquals: "Por favor selecciona un elemento" },
				city: { valueNotEquals: "Por favor selecciona un elemento" },
    },
		//when submit button
		submitHandler: function(form){
			$j('#post_authority').on('submit', function(event){
				event.preventDefault();
				console.log("form submitted!");

				$.ajax({
					url: $j(this).attr('action'),
					type: $j(this).attr('method'),	//type POST
					//data from id form
					data: $j("#post_authority").serialize(),

					success: function(json){
						console.log("json: " + json.result);
						//clean fields input
						$j("input:text").val('');
						//change values of Select
						$j("select").val("Seleccion");
						//show alert in browser
						alert(json.result + "\n" + json.authority)
						console.log("success");
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
