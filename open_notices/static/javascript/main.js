$(document).ready(function(){
  $(document).foundation();
});

function getUrlParameter(key){
  url = window.location.href;
  if (url.includes(key)){
    results = new RegExp('[\?&]' + key + '=([^&#]*)').exec(url);
    return results[1] || 0;
  }else{
    return 0;
  }
}
