var chat_room_id = undefined;
var last_received = 0;
var lastSend = new Date();
var refreshDelay = 1000;
/**
 * Initialize chat:
 * - Set the room id
 * - Generate the html elements (chat box, forms & inputs, etc)
 * - Sync with server
 * @param chat_room_id the id of the chatroom
 * @param html_el_id the id of the html element where the chat html should be placed
 * @return
 */
function init_chat(chat_id, html_el_id) {
        chat_room_id = chat_id;
        layout_and_bind(html_el_id);
        sync_messages();
}

var img_dir = "/static/img/";

/**
 * Asks the server which was the last message sent to the room, and stores it's id.
 * This is used so that when joining the user does not request the full list of
 * messages, just the ones sent after he logged in. 
 * @return
 */
function sync_messages() {
    $.ajax({
        type: 'POST',
        data: {id:window.chat_room_id},
        url:'/chat/sync/',
                dataType: 'json',
                success: function (json) {
                last_received = json.last_message_id;
                }        
    });
        
        setTimeout("get_messages()", refreshDelay);
}

/**
 * Generate the Chat box's HTML and bind the ajax events
 * @param target_div_id the id of the html element where the chat will be placed 
 */
function layout_and_bind(html_el_id) {
      // layout stuff
	var html = '<div id="chat-messages-container">'+
                '<div id="chat-messages"> </div>'+
                '<div id="chat-last"> </div>'+
                '</div>'+
                '<form id="chat-form">'+
                '<input name="message" type="text" class="message" autocomplete="off"/>'+
                '<input type="submit" value="Say!!!"/>'+
                '</form>';
                
        $("#"+html_el_id).append(html);
                
        // event stuff
        $("#chat-form").submit( function () {
        	if(new Date().getTime() - lastSend.getTime() < 500){
			return false;
		}
		var $inputs = $(this).children('input');
		var values = {};
		
          	$inputs.each(function(i,el) { 
              		values[el.name] = $(el).val();
            	});
            	values['chat_room_id'] = window.chat_room_id;
            	values['message'] = trim_message(values['message']);    
            	$.ajax({
               		data: values,
                	dataType: 'json',
                	type: 'post',
                	url: '/chat/send/'
           	});
            	$('#chat-form .message').val('');
		lastSend = new Date();
            return false;
        });
};

/**
 * Gets the list of messages from the server and appends the messages to the chatbox
 */
function get_messages() {
    $.ajax({
        type: 'POST',
        data: {id:window.chat_room_id, offset: window.last_received},
        url:'/chat/receive/',
                dataType: 'json',
                success: function (json) {
                        var scroll = false;
                
                        // first check if we are at the bottom of the div, if we are, we shall scroll once the content is added
                        var $containter = $("#chat-messages-container");
                        if ($containter.scrollTop() == $containter.attr("scrollHeight") - $containter.height())
                                scroll = true;
                        
                        // add messages
                        $.each(json, function(i,m){
                                // filter message for bad bad stuff (XSS injections for instance)
                                m.message = clean_message(m.message);
                                // depending on the message type, present it in a different manner
                                if (m.type == 's')
                                        $('#chat-messages').append('<div class="system">' + m.message + '</div>');
                                else if (m.type == 'm')         
                                        $('#chat-messages').append('<div class="message"><div class="author">'+m.author+'</div>'+m.message + '</div>');
                                else if (m.type == 'j')         
                                        $('#chat-messages').append('<div class="join">'+m.author+' has joined</div>');
                                else if (m.type == 'l')         
                                        $('#chat-messages').append('<div class="leave">'+m.author+' has left</div>');
                                        
                                last_received = m.id;
                        })
                        
                        // scroll to bottom
                        if (scroll)
                                $("#chat-messages-container").animate({ scrollTop: $("#chat-messages-container").attr("scrollHeight") }, 500);
                }        
    });
    
    // wait for next
    setTimeout("get_messages()", refreshDelay);
}

/**
 * Tells the chat app that we are joining
 */
function chat_join() {
        $.ajax({
                async: false,
        type: 'POST',
        data: {chat_room_id:window.chat_room_id},
        url:'/chat/join/',
    });
}

/**
 * Tells the chat app that we are leaving
 */
function chat_leave() {
        $.ajax({
                async: false,
        type: 'POST',
        data: {chat_room_id:window.chat_room_id},
        url:'/chat/leave/',
    });
}

// attach join and leave events
$(window).load(function(){chat_join()});
$(window).unload(function(){chat_leave()});


/**
 * Trims messages to 300 characters.
 */
function trim_message(text) {
	text = jQuery.trim(text).substring(0,300);
        return text;
}

/**
 * Clean unwanted characters from message string to prevent code injection
 */ 
function clean_message(text) {
        return text.replace(/</g,"&lt;").replace(/>/g,"&gt;")
}

