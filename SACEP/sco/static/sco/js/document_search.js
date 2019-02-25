console.log("static search")

$(document).ready(function(){
	//name from form
	$("#search_document").submit(function(e){
		e.preventDefault();

		$.ajax({
			url: $(this).attr('action'),
			type: $(this).attr('method'),
			data: $("#search_document").serialize(),

			success: function(json){

				console.log(json);
				var str;
				$(json).each(function(){
					  str +=  '<tr>'
						+ '<td>' + this.id_document + '</td>'
						+ '<td>' + this.num_folio + '</td>'
						+ '<td>' + this.name_person + '</td>'
						+ '<td>' + this.process_manager + '</td>'
						+ '<td>' + this.derivate_area + '</td>'
						+ '<td>' + this.document_type + '</td>'
						+ '<td>' + this.type_end_days + '</td>'
						+ '<td id=' + 'status_value' + '>' + this.process_status + '</td>'
						+ '<td class="table-danger"><a href="/sco/oficio/' + this.id_document + '/"><span style="color: green"><i class="fas fa-info-circle fa-2x"></i></span></a></td>'
						+ '<td class="table-danger"><a href="/sco/oficio/' + this.id_document + '/editar"><span style="color: green"><i class="fas fa-pencil-alt fa-2x"></i></span></a></td></a></td>'
						+ '<td id=' + 'status_icon' +' class="table-danger"><a href="/sco/oficio/' + this.id_document + '/actualizar"><span style="color: green"><i class="fas fa-exchange-alt fa-2x"></i></span></a></td>'
						+ '</tr>';
				});
				$("#table-search > tbody ").append(str);

				//condiciones para mostrar iconos de status and pdf
				let status_value = $("#status_value").text();
				console.log(status_value);

			}
		})
	})

	$("#cleaner").click(function(e){
		e.preventDefault();
		console.log("limpiar");
		$("#table-search > tbody > tr" ).remove();
		$("input:text").val('');
	})

})
