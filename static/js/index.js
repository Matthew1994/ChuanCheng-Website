$(document).ready(function(){
    editor = CKEDITOR.replace('content');
    var show = document.getElementById("show");
	$("#preview").click(function(){
	    var context = editor.getData()
	    $("#editArticleForm").hide();
	    $("#previewBox").show();
        $("#preArea").html(context);
	});

	$("#backToEdit").click(function(){
	    $("#previewBox").hide();
	    $("#editArticleForm").show();
	});
})