$(document).ready(function(){
	
	/*var config = {
		siteURL		: 'genius.com',	// Change this to your site tutorialzine
		searchSite	: true,
		type		: 'web',
		append		: false,
		perPage		: 8,			// A maximum of 8 is allowed by Google
		page		: 0				// The start page
	}*/
	
	var config = {
		siteURL		: 'genius.com',	// Change this to your site tutorialzine
		domain		: 'song',
		type		: 'find',
		query 		: ''
	}
	
	// The small arrow that marks the active search icon:
	var arrow = $('<span>',{className:'arrow'}).appendTo('ul.icons');
	
	$('ul.icons li').click(function(){
		var el = $(this);
		
		if(el.hasClass('active')){
			// The icon is already active, exit
			return false;
		}
		
		el.siblings().removeClass('active');
		el.addClass('active');
		
		// Move the arrow below this icon
		arrow.stop().animate({
			left		: el.position().left,
			marginLeft	: (el.width()/2)-4
		});
		
		// Set the search type
		config.type = el.attr('data-searchType');
		$('#more').fadeOut();
	});
	
	// Adding the site domain as a label for the first radio button:
	$('#siteNameLabel').append(' '+config.siteURL);
	
	// Marking the Search tutorialzine.com radio as active:
	$('#searchSong').click(function(){
		config.domain = 'song'
	});
	
	$('#searchAlbum').click(function(){
		config.domain = 'album'
	});
	
	$('#searchArtist').click(function(){
		config.domain = 'artist'
	});
	
	// Marking the web search icon as active:
	$('li.web').click();
	
	// Focusing the input text box:
	$('#s').focus();

	$('#searchForm').submit(function(){
		config.query = $('#s').val()
		googleSearch();
		return false;
	});
	
	$('#searchSong,#searchAlbumn,#searchArtist').change(function(){
		// Listening for a click on one of the radio buttons.
		// config.searchSong is either true or false.
		
		config.searchSong = this.id == 'searchSong';
	});
	
	
	function googleSearch(settings){
		
		// If no parameters are supplied to the function,
		// it takes its defaults from the config object above:
		
		settings = $.extend({},config,settings);
		settings.term = settings.term || $('#s').val();
		
		if(settings.searchSong){
			// Using the Google site:example.com to limit the search to a
			// specific domain:
			settings.term = 'site:'+settings.siteURL+' '+settings.term;
		}
		
		// URL of Google's AJAX search API
		var apiURL = 'http://ajax.googleapis.com/ajax/services/search/'+settings.type+'?v=1.0&callback=?';
		var resultsDiv = $('#resultsDiv');
		var pageContainer = $('<div>',{className:'pageContainer'});
		
		
				
				
		$.getJSON('http://127.0.0.1:5000/getstuff',data={domain:config.domain,type:config.type,query:config.query} , function(r){
			console.log(r)	
			
			$('#more').remove();
			
			if(r.length){
				
				// If results were returned, add them to a pageContainer div,
				// after which append them to the #resultsDiv:
				
				var pageContainer = $('<div>',{className:'pageContainer'});
				
				for(var i=0;i<r.length;i++){
					if(config.domain == 'artist') {
							arr = [ 
							'<div class="webResult">',
							'<h2><a href="',r[i].url,'" target="_blank">',r[i].title,'</a></h2>', //r.title displays artist & title
							'<img src="',r[i].img_url,'">',
							'<p>',r[i].annotations,'</p>', //r.content is the description displayed
							'<c><a href="',r[i].artist_url,'" target="_blank">',r[i].artist_name,'</a></c>', //r.visibleUrl is the blue url link
							'</div>'
						];
						pageContainer.append(arr.join(''));
					}
					else {
						// Creating a new result object and firing its toString method:
						arr = [ 
							'<div class="webResult">',
							'<h2><a href="',r[i].url,'" target="_blank">\"',r[i].title,'\"</a> by ',r[i].artist_name,'</h2>', //r.title displays artist & title
							'<img src="',r[i].img_url,'">',
							'<p>',r[i].annotations,'</p>', //r.content is the description displayed
							'<c><a href="',r[i].artist_url,'" target="_blank">',r[i].artist_name,'</a></c>', //r.visibleUrl is the blue url link
							'</div>'
						];
						pageContainer.append(arr.join(''));
					}
				}
				
				if(!settings.append){
					// This is executed when running a new search, 
					// instead of clicking on the More button:
					resultsDiv.empty();
				}
				
				pageContainer.append('<div class="clear"></div>')
							 .hide().appendTo(resultsDiv)
							 .fadeIn('slow');
				
				/*var cursor = r.responseData.cursor;
				
				// Checking if there are more pages with results, 
				// and deciding whether to show the More button:
				
				if( +cursor.estimatedResultCount > (settings.page+1)*settings.perPage){
					$('<div>',{id:'more'}).appendTo(resultsDiv).click(function(){
						googleSearch({append:true,page:settings.page+1});
						$(this).fadeOut();
					});
				}*/
			}
			else {
				
				// No results were found for this search.
				
				resultsDiv.empty();
				$('<p>',{className:'notFound',html:'No Results Were Found!'}).hide().appendTo(resultsDiv).fadeIn();
			}
		});
				/*for(var i=0;i<results.length;i++){
					// Creating a new result object and firing its toString method:
					pageContainer.append('<div>results[i]</div>);
				}
				
				if(!settings.append){
					// This is executed when running a new search, 
					// instead of clicking on the More button:
					resultsDiv.empty();
				}
				
				pageContainer.append('<div class="clear"></div>')
							 .hide().appendTo(resultsDiv)
							 .fadeIn('slow');*/
				
		
		
		/*$.getJSON(apiURL,{q:settings.term,rsz:settings.perPage,start:settings.page*settings.perPage},function(r){
			
			var results = r.responseData.results;
			$('#more').remove();
			
			if(results.length){
				
				// If results were returned, add them to a pageContainer div,
				// after which append them to the #resultsDiv:
				
				var pageContainer = $('<div>',{className:'pageContainer'});
				
				for(var i=0;i<results.length;i++){
					// Creating a new result object and firing its toString method:
					pageContainer.append(new result(results[i]) + '');
				}
				
				if(!settings.append){
					// This is executed when running a new search, 
					// instead of clicking on the More button:
					resultsDiv.empty();
				}
				
				pageContainer.append('<div class="clear"></div>')
							 .hide().appendTo(resultsDiv)
							 .fadeIn('slow');
				
				var cursor = r.responseData.cursor;
				
				// Checking if there are more pages with results, 
				// and deciding whether to show the More button:
				
				if( +cursor.estimatedResultCount > (settings.page+1)*settings.perPage){
					$('<div>',{id:'more'}).appendTo(resultsDiv).click(function(){
						googleSearch({append:true,page:settings.page+1});
						$(this).fadeOut();
					});
				}
			}
			else {
				
				// No results were found for this search.
				
				resultsDiv.empty();
				$('<p>',{className:'notFound',html:'No Results Were Found!'}).hide().appendTo(resultsDiv).fadeIn();
			}
		});*/
	}
	
	function result(r){
		
		// This is class definition. Object of this class are created for
		// each result. The markup is generated by the .toString() method.
		
		var arr = [];
		
		// GsearchResultClass is passed by the google API
		switch(r.GsearchResultClass){
			
			case 'GwebSearch':
				arr = [
					'<div class="webResult">',
					'<h2><a href="',r.unescapedUrl,'" target="_blank">',r.title,'</a></h2>', //r.title displays artist & title
					'<p>',r.content,'</p>', //r.content is the description displayed
					'<a href="',r.unescapedUrl,'" target="_blank">',r.visibleUrl,'</a>', //r.visibleUrl is the blue url link
					'</div>'
				];
			break;
			case 'GimageSearch':
				arr = [
					'<div class="imageResult">',
					'<a target="_blank" href="',r.unescapedUrl,'" title="',r.titleNoFormatting,'" class="pic" style="width:',r.tbWidth,'px;height:',r.tbHeight,'px;">',
					'<img src="',r.tbUrl,'" width="',r.tbWidth,'" height="',r.tbHeight,'" /></a>',
					'<div class="clear"></div>','<a href="',r.originalContextUrl,'" target="_blank">',r.visibleUrl,'</a>',
					'</div>'
				];
			break;
			case 'GvideoSearch':
				arr = [
					'<div class="imageResult">',
					'<a target="_blank" href="',r.url,'" title="',r.titleNoFormatting,'" class="pic" style="width:150px;height:auto;">',
					'<img src="',r.tbUrl,'" width="100%" /></a>',
					'<div class="clear"></div>','<a href="',r.originalContextUrl,'" target="_blank">',r.publisher,'</a>',
					'</div>'
				];
			break;
			case 'GnewsSearch':
				arr = [
					'<div class="webResult">',
					'<h2><a href="',r.unescapedUrl,'" target="_blank">',r.title,'</a></h2>',
					'<p>',r.content,'</p>',
					'<a href="',r.unescapedUrl,'" target="_blank">',r.publisher,'</a>',
					'</div>'
				];
			break;
		}
		
		// The toString method.
		this.toString = function(){
			return arr.join('');
		}
	}
	
	
});
