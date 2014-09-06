$(document).ready(function(){
				$("#btn").click(function(){
					info = $("#question").val();
					url = "/anwser/";
					data = {"info":info};
					content = "<div style='width:100%;height:auto;padding: 5px;text-align:right;'><span style='width:150px;display:inline-block;background:grey;border-radius:8px;border: 1px solid #dadada;padding:10px;text-align:left;'>";
					content +=info+"</span></div>";
					$("#main").append(content);
					$.get(url,data,function(result){
						obj = eval("("+result+")");
						content = "<div style='width:100%;height: auto;padding:5px;'>";
					    content += "<span style='width:250px;display:inline-block;background:green;border-radius:8px;border: 1px solid #dadada;padding:5px;'>"+obj.text+"</span></div>";
					    $("#main").append(content);
					});
				});
			});