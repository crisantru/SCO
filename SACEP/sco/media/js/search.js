$(document).ready(function(){
  $("#search_document").submit(function(e){
    e.preventDefault();

    $.ajax({
      url: $(this).attr('action'),
      type: $(this).attr('method'),
      data: $(this).document_serializer(),

      success: function(json){
        console.log(json);
      }

    })
  })
})
