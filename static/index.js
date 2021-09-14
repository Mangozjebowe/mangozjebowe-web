function printodcinki(odcinki, id, coltype){
    for(i in odcinki){
      // $( "#"+id ).append("<div class='"+ coltype + ' anime>'+"<a href='"+"/anime/"+odcinki[i]["id"]+'">'+"<div class='card'>"+"<img class='img-top plakat' src='"+odcinki[i]["image_url"]+"'"+"</img>"+"<div class='card-header'>"+odcinki[i]["title"]+"</div></div></div>");
      $( "#"+id ).append("<div class='"+coltype+"'>"+"<a href='"+"/anime/"+odcinki[i]["id"]+"'>"+"<div class='card'>"+"<img class='img-top plakat' src='"+odcinki[i]["image_url"]+"'"+"</img>"+"<div class='card-header'>"+odcinki[i]["title"]+"</div></div></div>");
      $( ".loading" ).hide();
      }}
function getpage(page){
    var page
    offset=30*(page-1)
    fetch('/api/series'+"?limit=30"+"&offset="+offset)
      .then(response => response.json())
      .then(data => function(data){
      $("#wszystkieanime").find(".anime").remove()
      printodcinki(data["serie"], "wszystkieanime", "col-md-3 col-6 anime");
          printpages(data["pages"], page)
        }(data));
        $(".pagination").show();
        $(".minianimebox").show();
    }
    function printpages(pages, currentpage){
      $(".page-item").remove();
      var pages
      for(i = 1; i < pages+1; i++){
        $( ".pagination" ).append('<a' + ' id=page'+i+ ' class="page-item page-link">'+i+'</a>')
      }
    }
    function search(search){
      $("#lastadded").hide()
      $(".minianimebox").hide();
      var odcinki
      $("#wszystkieanime").find(".anime").remove()
      fetch('/api/series/search/'+search)
      .then(response => response.json())
      .then(data => printodcinki(data, "wszystkieanime", "col-md-3 col-6 anime"))
      console.log(odcinki)
    }
    $(document).on('click', '.page-link', function() {
      getpage(this.innerHTML);
      id = this.innerHTML;
      $( this ).css( "background-color", "yellow" );
    });
    function searchonclick() {
      $(".pagination").hide()
      $("#wszystkieanime").find(".anime").remove()
      var fraza = $( "#search" ).val();
      $(".loading").show()
      search(fraza)
      if(fraza == ""){
        getpage(1);
        $("#page1").click()
      }
    }
    function getlastadded(){
      fetch("/api/series/lastadded?limit=4")
      .then(response=>response.json())
      .then(data=>printodcinki(data, "lastadded", "col-md-2 col-6 anime"))
    }
    $(document).ready(function(){
      getpage(1)
      getlastadded();
    }())