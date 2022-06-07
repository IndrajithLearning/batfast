
$("#videoBtn").click(function(){
  $("#watchVideo").trigger('play');
});
$("#videoClose").click(function(){
  $("#watchVideo").trigger('pause');
});




  $("#getScroll").click(function() {
    $([document.documentElement, document.body]).animate({
        scrollTop: $("#getSection").offset().top
    }, 100);
});

/*menu bar*/
$(".menuBar").click(function(){
    $(this).toggleClass("active");
    $(".menuList").toggleClass("active");
});


$('.customerSlick').slick({
  slidesToShow: 3,
  slidesToScroll: 1,
  autoplay: true,
  autoplaySpeed: 1000,
  dots:true,
  arrows:false
});
	
/*ajax Call*/

$(".delTri").click(function(){
  $(".blinkAlert").removeClass('active');
});
$(".upPost").click(function(){
  $(".blinkAlertUpdate").removeClass('active');
});

/*Get Touch Ajax*/

$(document).ready(function() {
	$("#getSubmitBtn").click(function(event){
    var getName = $("#getName").val();
    var getEmail =  $("#getEmail").val();
    var getMsg = $("#getMsg").val();
  
		$.ajax({
			data : {
        getName :getName,
        getEmail :getEmail,
				getMsg :getMsg
			},
			type : 'POST',
			url : '/get-touch'
		})
		.done(function(data) {
      $("#getTouchForm").fadeOut();
      $("#getSucMsg").html("Thank you "+getName+"."+" We will get back to you soon.")
		});
		event.preventDefault();

	});

});

/*Delete Blog Ajax*/
$(document).ready(function() {
	$(".deleteBlogBtn").click(function(event){
    var del = $(this).val();
		$.ajax({
			data : {
				deblogId :del
			},
			type : 'POST',
			url : '/delete-blog'
		})
		.done(function(data) {
      $(".deleteBlogModal").modal('hide');
      $("."+data.deblogId).fadeOut();
      $(".blinkAlert").addClass('active');
		});

		event.preventDefault();

	});

}); 



/*Delete Blog Ajax*/
$(document).ready(function() {
	$(".updateBlogBtn").click(function(event){
    var upId = $(this).val();
    var upTitle = $(".upTitle"+upId).val()
    var upContent =  $(".upContent"+upId).val()
		$.ajax({
			data : {
				blogId :upId,
        blogTitle :upTitle,
        blogContent:upContent
			},
			type : 'POST',
			url : '/update-blog'
		})
		.done(function(data) {
      $(".updateBlogModal").modal('hide');
      $("."+data.blogId).children(".aftUp").html(data.blogTitle);
      $(".blinkAlertUpdate").addClass('active');
		});

		event.preventDefault();

	});

});

