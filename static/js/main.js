$("#videoBtn").click(function() {
    $("#watchVideo").play();
  });
  $("#videoClose").click(function() {
    $("#watchVideo").pause();
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
    var upImage = $(".upImage"+upId)[0].files[0]
		$.ajax({
			data : {
				blogId :upId,
        blogTitle :upTitle,
        blogContent:upContent,
        blogImage:upImage,
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

