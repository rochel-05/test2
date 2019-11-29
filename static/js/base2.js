$(document).ready(function () {
   $('#dtBasicExample').DataTable({
   "pagingType": "simple" // "simple" option for 'Previous' and 'Next' buttons only
   });
   $('.dataTables_length').addClass('bs-select');
});

function timer(n)
{
  $(".bar").css("width", n + "%");
  if(n < 100){
      setTimeout(function(){timer(n + 10);}, 200);
   }
   }$(function (){
   $("#animer").click(function(){
      timer(0);});
    });
   $(function (){
       $("#animer2").click(function(){
        timer(0);});
   });


