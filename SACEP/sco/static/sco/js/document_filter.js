console.log("enable filter")

$(document).ready(function(){




	//var json_length = document.getElementById('json_length')
	$("#filter_document_type").submit(function(e){
		e.preventDefault();

		$.ajax({
			url: $(this).attr('action'),
			type: $(this).attr('method'),
			//data from id form
			data: $("#filter_document_type").serialize(),

			success: function(json){

				console.log("json: " + json);
				console.log(Object.keys(json).length);
				len = Object.keys(json).length;
				len = len.toString();
				$("#json_length").text(len);



				var str;
				$(json).each(function(){
					  str +=  '<tr>'
						//+ '<td>' + this.id_document + '</td>'
						//+ '<td>' + this.num_folio + '</td>'
						+ '<td>' + this.name_person + '</td>'
						+ '<td>' + this.register_date+ '</td>'
						+ '<td>' + this.date_delivery	 + '</td>'
						+ '<td>' + this.process_status + '</td>'
						+ '<td class="table-danger"><a href="/sco/oficio/' + this.id_document + '/">Ver Más</a></td>'
						//+ '<td class="table-danger"><a href="/sco/oficio/' + this.id_document + '/editar">Editar</a></td>'
						//+ '<td class="table-danger"><a href="/sco/oficio/' + this.id_document + '/actualizar">STATUS</a></td>'
						+ '</tr>';
				});
				$("#table_filter_type > tbody ").append(str);
			}

		})
	})

	$("#cleaner").click(function(e){
		e.preventDefault();
		console.log("limpiar");
		$("#table_filter_type > tbody > tr" ).remove();
		$("input:text").val('');
		$("p").empty();
	})

})
