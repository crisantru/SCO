
	var $j = jQuery.noConflict();

	$j(document).ready(function(){
	//rule for validate select
	$j.validator.addMethod("valueNotEquals", function(value, element, arg){
  // I use element.value instead value here, value parameter was always null
	    return arg != element.value;
	}, "Value must not equal arg.");
	//validate fields form
	$j('#myForm').validate({
		rules:{
			//field on form
			name:{
				required:true,
				minlength:4,
			},
			//field on form
			lastNameP:{
				required: true,
				minlength: 4,
			},
			//field on form
			lastNameM:{
				required: true,
				minlength: 4,
			},
			//field on form
			email:{
				required:true,
				email:true,
				//valueNotEquals: "Seleccion",
			},
			//field on form
			username:{
				required: true,
				minlength:5,
			},
			//field on form
			type_account:{
				required:true,
				valueNotEquals: "Seleccion",
			},
			//field on form
			password1:{
				required:true,
				minlength:8,
			},
			//field on form
			password2:{
				required:true,
				minlength:8,
			}
		},
		//messages for Selects
		messages: {
        type_account: { valueNotEquals: "Por favor selecciona un elemento" },
    },
		//when submit button
		submitHandler: function(form){
			$j('#myForm').on('submit', function(event){
				event.preventDefault();
				console.log("form submitted!");

				$.ajax({
					url: $j(this).attr('action'),
					type: $j(this).attr('method'),	//type POST
					//data from id form
					data: $j("#myForm").serialize(),

					success: function(json){
						console.log("json: " + json.result);
						//clean fields input
						$j("input:text").val('');
						$j("input:password").val('');
						//change values of Select
						$j("select").val("Seleccion");
						//show alert in browser
						alert(json.result)
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
