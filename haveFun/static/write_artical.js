
 $(document).ready(function(){
	$("a[data-action='redo']").each(function(index,item){
	   $(this).bind("click",function(){
	    	$('#content').val("");
		});
	});



    $("a[data-action='trigger-save']").each(function(index,item){
	   $(this).bind("click",function(){
	   		var title = $("#note_title").val();                 //获得form中用户输入sql语句注意 与你html中input的id一致  
            var content = $("#content").val(); 
	   		 
            
          $.ajax({  
              type:"POST",  
              data: {'title':title,'content':content},  
              url: "http://localhost:8000/haveFun/artical_draft_save/", //后台处理函数的url 这里用的是static url 需要与urls.py中的name一致,或者直接写http地址               
              success: function(response,status,xhr){
                  alert(response); 
             },  
             error: function(error){  
                 alert(error.statusText);  
             }  
         });  
                  
        });  
		
	});
});

