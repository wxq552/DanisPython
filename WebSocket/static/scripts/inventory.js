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
    var host = 'ws://localhost:8000/cart/status';

    var websocket = new WebSocket(host);

    websocket.onopen = function (evt) { };
    websocket.onmessage = function(evt) {
    	obj = $.parseJSON(evt.data);
        var content = "";
        	for(var i= 0;i<obj.length;i++){
        		content +="<div style='width:386px;height:auto;border:1px solid #dadata'><h4>"+obj[i].title+"</h4>";
        		content +="<div>"+obj[i].content+"</div></div>";
        	}
        	$("#message_list").html("");
        	$("#message_list").append(content);
        	//setTimeout(requestInventory, 0);
    };
    websocket.onerror = function (evt) { };
}