function JT_close(linkId){
    $('#JT_'+linkId).remove();
}
function JT_show(linkId,title,content){
	if(!title){
        title = "";
    }
    if(!content){
        content = "";
    }
	var de = document.documentElement;
	var w = self.innerWidth || (de&&de.clientWidth) || document.body.clientWidth;
	var hasArea = w - getAbsoluteLeft(linkId);
	var clickElementy = getAbsoluteTop(linkId) - 3; //set y position
	
	var tip_width = 180;
	
	if(hasArea>(tip_width+75)){
		$("body").append("<div id='JT_"+linkId+"' class='JT_css' style='width:"+tip_width+"px'><div id='JT_arrow_left'></div><div id='JT_close_left'>"+title+"</div><div id='JT_copy'>"+content+"</div></div>");//right side
		var arrowOffset = getElementWidth(linkId) + 11;
		var clickElementx = getAbsoluteLeft(linkId) + arrowOffset; //set x position
	}else{
		$("body").append("<div id='JT_"+linkId+"' class='JT_css' style='width:"+tip_width+"px'><div id='JT_arrow_right' style='left:"+(tip_width+1)+"px'></div><div id='JT_close_right'>"+title+"</div><div id='JT_copy'>"+content+"</div></div>");//left side
		var clickElementx = getAbsoluteLeft(linkId) - (tip_width + 15); //set x position
	}
	
	$('#JT_'+linkId).css({left: clickElementx+"px", top: clickElementy+"px"});
	$('#JT_'+linkId).show();
}

// $(window).scroll(function(){
    // console.info("scroll");
    // JT_scroll();
// });
function JT_scroll(){
    $(".JT_css").each(function(i,item){
        var linkId = this.id;
        var de = document.documentElement;
        var w = self.innerWidth || (de&&de.clientWidth) || document.body.clientWidth;
        var hasArea = w - getAbsoluteLeft(linkId);
        var clickElementy = getAbsoluteTop(linkId) - 3; //set y position
        
        var tip_width = 180;
        
        if(hasArea>(tip_width+75)){
            var arrowOffset = getElementWidth(linkId) + 11;
            var clickElementx = getAbsoluteLeft(linkId) + arrowOffset; //set x position
        }else{
            var clickElementx = getAbsoluteLeft(linkId) - (tip_width + 15); //set x position
        }
        $('#JT_'+linkId).css({left: clickElementx+"px", top: clickElementy+"px"});
    });
}

function getElementWidth(objectId) {
	x = document.getElementById(objectId);
	return x.offsetWidth;
}

function getAbsoluteLeft(objectId) {
	// Get an object left position from the upper left viewport corner
	o = document.getElementById(objectId)
	oLeft = o.offsetLeft            // Get left position from the parent object
	while(o.offsetParent!=null) {   // Parse the parent hierarchy up to the document element
		oParent = o.offsetParent    // Get parent object reference
		oLeft += oParent.offsetLeft // Add parent left position
		o = oParent
	}
	return oLeft
}

function getAbsoluteTop(objectId) {
	// Get an object top position from the upper left viewport corner
	o = document.getElementById(objectId)
	oTop = o.offsetTop            // Get top position from the parent object
	while(o.offsetParent!=null) { // Parse the parent hierarchy up to the document element
		oParent = o.offsetParent  // Get parent object reference
		oTop += oParent.offsetTop // Add parent top position
		o = oParent
	}
	return oTop
}

