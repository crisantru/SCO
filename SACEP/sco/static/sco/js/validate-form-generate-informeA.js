
	var $j = jQuery.noConflict();

	$j(document).ready(function(){
	//rule for validate select
	$j.validator.addMethod("valueNotEquals", function(value, element, arg){
  // I use element.value instead value here, value parameter was always null
	    return arg != element.value;
	}, "Value must not equal arg.");
	//validate fields form
	$j('#generate-informeA').validate({
		rules:{
			date_redaction:{
				required: true,
			},
			//field on form
			judge_type:{
				required:true,
				minlength:4,
			},
			//field on form
			info_answer:{
				required: true,
				valueNotEquals: "0",
			},
			//field on form
			observaciones:{
				required: true,
			},

		},
		//messages for Selects
		messages: {
        info_answer: { valueNotEquals: "Por favor selecciona un elemento" },
    },
		//when submit button
		/*submitHandler: function(form){
			$j('#generate-informeA').on('submit', function(event){
				event.preventDefault();
				console.log("form submitted!");

				$.ajax({
					url: $j(this).attr('action'),
					type: $j(this).attr('method'),	//type POST
					//data from id form
					data: $j("#generate-informeA").serialize(),

					success: function(json){
						console.log("json: " + json.result);
						//clean fields input
						$j("input:text").val('');
						//$j("input:password").val('');
						//change values of Select
						$j("select").val("Seleccion");
						//show alert in browser
						alert(json.result)
						console.log("success");
					},

				});
			});
		}*/
	});
});
