function form_handler(){
    event.preventDefault();
}
function send_data(){
    document.querySelector('form').addEventListener('submit', form_handler);

    var fd = new FormData(document.querySelector('form'));

    var xhr = new XMLHttpRequest();

    xhr.open('POST', '/predict', true);
    document.getElementById('prediction').innerHTML='Wait! Predicting Price ...';
    // sleep(0.3s)

    xhr.onreadystatechange = function(){
        if(xhr.readyState == XMLHttpRequest.DONE){
            document.getElementById('prediction').innerHTML="Prediction : " + xhr.responseText ;
        }
    }
    xhr.onload = function(){};
    xhr.send(fd);


}


self.addEventListener('install', function(event) {
    event.waitUntil(
      caches.open('pwa-cache').then(function(cache) {
        return cache.addAll([
          '/',
          '/static/css/style.css',  // Your CSS files
          '/static/script/script.js',     // Your JS files
          '/static/icons/icon-192x192.png',  // Icons for PWA
          '/static/icons/icon-512x512.png'
        ]);
      })
    );
  });
  
  self.addEventListener('fetch', function(event) {
    event.respondWith(
      caches.match(event.request).then(function(response) {
        return response || fetch(event.request);
      })
    );
  });
  