function printpinned(data){
    for(i in data){
    $( "#pinned" ).append("<div " + "id='" + data[i]["id"] + "' class='col-md-2 col-6 anime'>"+"<div class='card'>"+"<img class='img-top plakat' src='"+data[i]["image_url"]+"'"+"</img>"+"<div class='card-header'>"+"<a href='"+"/anime/"+data[i]["id"]+"'>"+data[i]["title"]+"</a><button class='btn btn-primary' onclick='unpin("+data[i]["id"]+")' "+ "' >Odepnij</button>"+"</div></div></div>");
    $( ".loading" ).hide();
    }}
function pinned(){
    fetch("/api/pinned?limit=4")
    .then(response=>response.json())
    .then(data=>(printpinned(data)));
}
function unpin(id){
    // console.log(id)
    // $("#"+id).remove()
    fetch("/anime/"+id+"/unpin")
    $("#pinned").find(".anime").remove()
    pinned()    
}
$(document).ready(function(){
    pinned()
}())