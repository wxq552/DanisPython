$(document).ready(function() {
    //获取页面的唯一标识
    document.session = $('#session').val();
    //暂停100毫秒之后发出请求建立长连接
    setTimeout(requestInventory, 100);

    $('#send-button').click(function(event) {
    	title =$("#topic").val();
    	content = $("#content").val();
        jQuery.ajax({
            url: '//localhost:8000/cart',
            type: 'POST',
            data: {
            	session: document.session,
                title: title,
                content: content
            },
            beforeSend: function(xhr, settings) {
                //$(event.target).attr('disabled', 'disabled');
            },
            success: function(data, status, xhr) {
            	//alert(data);
                //$('#add-to-cart').hide();
                //$('#remove-from-cart').show();
                //$(event.target).removeAttr('disabled');
            }
        });
    });

    $('#remove-button').click(function(event) {
        jQuery.ajax({
            url: '//localhost:8000/cart',
            type: 'POST',
            data: {
                session: document.session,
                action: 'remove'
            },
            dataType: 'json',
            beforeSend: function(xhr, settings) {
                $(event.target).attr('disabled', 'disabled');
            },
            success: function(data, status, xhr) {
                $('#remove-from-cart').hide();
                $('#add-to-cart').show();
                $(event.target).removeAttr('disabled');
            }
        });
    });
});
//Ajax方式发出长轮询请求，建立长连接
function requestInventory() {
    jQuery.getJSON('//localhost:8000/cart/status', {session: document.session},
        function(data, status, xhr) {
            var content = "";
        	for(var i= 0;i<data.length;i++){
        		content +="<div style='width:386px;height:auto;border:1px solid #dadata'><h4>"+data[i].title+"</h4>";
        		content +="<div>"+data[i].content+"</div></div>";
        	}
        	$("#message_list").html("");
        	$("#message_list").append(content);
            setTimeout(requestInventory, 0); //上一次长连接取得服务器推送过来的消息以后，立即建立下次长连接
        }
    );
}