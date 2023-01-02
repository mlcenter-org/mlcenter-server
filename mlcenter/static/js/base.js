let cbcopy_items = document.querySelectorAll('.cbcopy');
if (cbcopy_items.length > 0) {
  //add clipboard icon to .cbcopy
  cbcopy_items.forEach(function (el) {
    // copy data from data-value to clipboard
    el.addEventListener('click', function (e) {
      let data = el.getAttribute('data-value');
      navigator.clipboard.writeText(data);
    });
  });
}

$(document).ready(function () {
  // Specific JS goes HERE
  $.ajaxSetup({ 
      beforeSend: function(xhr, settings) {
          function getCookie(name) {
              var cookieValue = null;
              if (document.cookie && document.cookie != '') {
                  var cookies = document.cookie.split(';');
                  for (var i = 0; i < cookies.length; i++) {
                      var cookie = jQuery.trim(cookies[i]);
                      // Does this cookie string begin with the name we want?
                      if (cookie.substring(0, name.length + 1) == (name + '=')) {
                          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                          break;
                      }
                  }
              }
              return cookieValue;
          }
          if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
              // Only send the token to relative URLs i.e. locally.
              xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
          }
      } 
 });
 
});