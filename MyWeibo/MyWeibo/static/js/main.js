$(function(){
	$(".comments").click(function(){
		weibo_id = $(this).attr("type");
		url = "/getcomments/"+weibo_id+"/";
	    if($("#tb_"+weibo_id).css("display") == "none"){
	    	$.get(url,{},function(data,status){
		 var obj = eval("("+data+")");
		 var content = "<tr><td colspan='2' align='right'><input type='text' style='width:495px;height:15px;border:1px solid #dadada;'/><input type='button' style='color:#666' value='回复'></td></tr>";
		   for(var i=0;i<obj.length;i++){
		   	 content +="<tr><td width='30' valign='top'><img src='"+obj[i].user.profile_image_url+"' width='30' height='30'/></td><td width='560' align='left'><table width='100%'><tr><td align='left'>";
		   	 content +="<a href='#' style='color:grey;font-size:13px;'>"+obj[i].user.screen_name+":</a>";
		   	 content +="<span>"+obj[i].text+"</span><span>(";
		   	 content +=obj[i].created_at+")</span></td></tr>";
		   	 content +="<tr><td align='right'><a href='javascript:void(0);' type='"+obj[i].id;
		   	 content +="' index='"+weibo_id; 
		   	 content +="' style='font-size:12px;color:grey;' class='reply'>回复</a><td></tr>";
		   	 content +="</table></td></tr>";
		   	 content +="<tr style='display:none;'><td colspan='2' align='right'><input type='text' style='width:495px;height:15px;border:1px solid #dadada;'/><input type='button' style='color:#666' value='回复'></td></tr>";
		   }
		   content +="<tr><td colspan='2' align='center'><a href=''>查看更多</a></td></tr>";
		   $("#tb_"+weibo_id).html("");
		   $("#tb_"+weibo_id).append(content);
		   $(".reply").each(function(e){
		   	  var wid = $(this).attr("index");
		   	  var cid = $(this).attr("type");
		   	  $(this).click(function(){
		   	  	var target = $(this).parents("tr").eq(1).next();
		   	  	target.toggle();
		   	  	target.children("td").eq(0).children("input").eq(1).click(function(){
		   	  		//alert(wid);
		   	  		//alert(cid);
		   	  		var data = target.children("td").eq(0).children("input").eq(0).val();
		   	  		var url = "/post_comment/";
		   	  		$.post(url,{wid:wid,cid:cid,data:data},function(data,status){
		   	  			
		   	  			var obj = eval("("+data+")");
							 var content = "<tr><td colspan='2' align='right'><input type='text' style='width:495px;height:15px;border:1px solid #dadada;'/><input type='button' style='color:#666' value='回复'></td></tr>";
							   for(var i=0;i<obj.length;i++){
							   	 content +="<tr><td width='30' valign='top'><img src='"+obj[i].user.profile_image_url+"' width='30' height='30'/></td><td width='560' align='left'><table width='100%'><tr><td align='left'>";
							   	 content +="<a href='#' style='color:grey;font-size:13px;'>"+obj[i].user.screen_name+":</a>";
							   	 content +="<span>"+obj[i].text+"</span><span>(";
							   	 content +=obj[i].created_at+")</span></td></tr>";
							   	 content +="<tr><td align='right'><a href='javascript:void(0);' type='"+obj[i].id;
							   	 content +="' index='"+weibo_id; 
							   	 content +="' style='font-size:12px;color:grey;' class='reply'>回复</a><td></tr>";
							   	 content +="</table></td></tr>";
							   	 content +="<tr style='display:none;'><td colspan='2' align='right'><input type='text' style='width:495px;height:15px;border:1px solid #dadada;'/><input type='button' style='color:#666' value='回复'></td></tr>";
							   }
							   content +="<tr><td colspan='2' align='center'><a href=''>查看更多</a></td></tr>";
							   $("#tb_"+wid).html("");
							   $("#tb_"+wid).append(content);
		   	  			
		   	  			
		   	  	   });
		   	  	});
		   	  	
		   	  });
		   });
		   
		});
	    }
		
		$("#tb_"+weibo_id).toggle();
		
	});
	
	$(".zfclass").click(function(){
		weibo_id = $(this).attr("type");
	    $("#zf_"+weibo_id).toggle();
	});
	
	$(".btn").click(function(){
		url = "/repost/";
		weibo_id = $(this).attr("alt");
		content = $(this).siblings("textarea").val();
		$.post(url,{weibo_id:weibo_id,content:content},function(data,status){
			document.location.href = "/access_login/?"+data;
		});
	});

	
});
