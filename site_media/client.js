var lastAdd = -1;
var startingDiv;
var handDiv;
var playDiv;
var discardDiv;
var dragging = false;

$(document).ready(function(){
	resync();
});

function resync(){
	if(dragging){
		$(document).stopTime();
		sync();
		return;
	}
	var url = window.location.pathname + " #Table";
	$("#Load").load(url, function(){
		rebind();
	});
}

function rebind(){
	imagepop();
	handDiv = $(".HandArea");
	playDiv = $(".PlayArea");
	discardDiv = $(".DiscardArea");
	$(".draggable").draggable({
		containment:(".Table"),
		start: function(event, ui){
			dragging = true;
			startMove(event, ui);
		},
		stop: function(event, ui){
			dragging = false;
			sendMove(event, ui)
		}		
	});
	$(".droppable").droppable({
		drop: function(event, ui){
			changeLoc(event, ui);
		}
	});
	$("#draw").click(function(){
		var url = document.location.href + "draw/";
		$.ajax({ url:url });
	});
	$(".upside").rotate(180);
	sync();
}

function startMove(event, ui){
	startingDiv = event.target.parentElement;	
}

function changeLoc(event, ui){
	if( event.target != startingDiv){
		var newDiv = $(event.target);
		var card = ui.draggable;
	//	newDiv.append(card);
		var id = card.attr('id');
		var letter;
		if (newDiv.attr('class') == playDiv.attr('class')){
			letter = '/t/';
		} else if (newDiv.attr('class') == handDiv.attr('class')){
			letter = '/h/';
		} else if (newDiv.attr('class') == discardDiv.attr('class')){
			letter = '/s/';
		}
		var url = "/game/changeArea/" + id + letter; 
		$.ajax({ url:url });
	}
}

function sendMove(event, ui){
	var id = event.target.id;
	var x = event.target.style.left;
	x = x.replace("px", "");
	var y = event.target.style.top;
	y = y.replace("px", "");
	var url = "/game/move/" + id + "/x" + x + "/y" + y + "/z1";
	$.ajax({ url: url });
}

function syncData(data){
	for(var i = 0; i < data.length; i++){
		if(data[i].type == "card"){
			moveCard(data[i].id, data[i].x, data[i].y);
		}
	}	
}

function moveCard(id, x, y){
	var cardID = '#' + id;
	$(cardID).css("top", y);
	$(cardID).css("left", x);	
}

function sync(){
	$.ajax({
		type: 'POST',
		url:document.location.href + 'sync',
		dataType: 'json',
		success: function(json){
			if(lastAdd != json[0].lastUpdate){
				lastAdd = json[0].lastUpdate;
				$(document).stopTime();
				resync();
				return;
			}
			
			if(!dragging) syncData(json[1].data);
		}
	});
	$(document).oneTime(2000, function(i){
		sync();
	});
}

function imagepop(){
	// deletes all orphaned popups
       	$("#thumbPopup").remove();
	$("img[src*='.jpg']").thumbPopup();
}

(function($) {
        $.fn.thumbPopup = function(options)
        {
                //Combine the passed in options with the default settings
                settings = jQuery.extend({
                        popupId: "thumbPopup",
                        popupCSS: {},
                        imgSmallFlag: "_t.jpg",
                        imgLargeFlag: "_s.jpg",
                        cursorTopOffset: 15,
                        cursorLeftOffset: 15,
                        loadingHtml: "<span style='padding: 5px;'>Loading</span>"
                }, options);
                
                //Create our popup element
                popup =
                $("<div />")
                .css(settings.popupCSS)
                .attr("id", settings.popupId)
                .css("position", "absolute")
                .appendTo("body").hide();
                
                //Attach hover events that manage the popup
                $(this)
                .hover(setPopup)
                .mousemove(updatePopupPosition)
                .mouseout(hidePopup);
                
                function setPopup(event)
                {
                        var fullImgURL = $(this).attr("src").replace(settings.imgSmallFlag, settings.imgLargeFlag);
                        
                        $(this).data("hovered", true);
                        
                        //Load full image in popup
                        $("<img />")
                        .bind("load", {thumbImage: this}, function(event)
                        {
                                //Only display the larger image if the thumbnail is still being hovered
                                if ($(event.data.thumbImage).data("hovered") == true) {
                                        $(popup).empty().append(this);
                                        updatePopupPosition(event);
                                        $(popup).show();
                                        updatePopupPosition(event);
                                }
                                $(event.data.thumbImage).data("cached", true);
                        })
                        .attr("src", fullImgURL);
                        
                        //If no image has been loaded yet then place a loading message
                        if ($(this).data("cached") != true) {
                                $(popup).append($(settings.loadingHtml));
                                $(popup).show();
                        }
                        
                        updatePopupPosition(event);                     
                }
                
                function updatePopupPosition(event)
                {
                        var windowSize = getWindowSize();
                        var popupSize = getPopupSize();
                        if (windowSize.width + windowSize.scrollLeft < event.pageX + popupSize.width + settings.cursorLeftOffset){
                                $(popup).css("left", event.pageX - popupSize.width - settings.cursorLeftOffset);
                        } else {
                                $(popup).css("left", event.pageX + settings.cursorLeftOffset);
                        }
                        if (windowSize.height + windowSize.scrollTop < event.pageY + popupSize.height + settings.cursorTopOffset){
                                $(popup).css("top", event.pageY - popupSize.height - settings.cursorTopOffset);
                        } else {
                                $(popup).css("top", event.pageY + settings.cursorTopOffset);
                        }
                }
                
                function hidePopup(event)
                {
                        $(this).data("hovered", false);
                        $(popup).empty().hide();
                }
                
                function getWindowSize() {
                        return {
                                scrollLeft: $(window).scrollLeft(),
                                scrollTop: $(window).scrollTop(),
                                width: $(window).width(),
                                height: $(window).height()
                        };
                }
                
                function getPopupSize() {
                        return {
                                width: $(popup).width(),
                                height: $(popup).height()
                        };
                }

                //Return original selection for chaining
                return this;
        };
})(jQuery);
