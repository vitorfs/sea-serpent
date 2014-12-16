$(function () {

  $(".btn-price-history").click(function () {
    var url = $(this).attr("href");
    var row = $(this).closest("tr");
    var title = $("td:eq(1)", row).text();
    $.ajax({
      url: url,
      cache: false,
      type: 'get',
      beforeSend: function () {
        $("#historico .modal-title").text(title);
        $("#historico .modal-body").html("<p>Carregando...</p>");
        $("#historico").modal();
      },
      success: function (data) {
        $("#historico .modal-body").html(data);
      },
      error: function () {
        $("#historico .modal-body").html("<p>Não foi possível recuperar o histórico deste produto :(</p>");
      }
    });
    return false;

  });

})