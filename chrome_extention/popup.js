let saveLink = document.getElementById('saveLink');
let saveEmail = document.getElementById('saveEmail');
let emailForm = document.getElementById('emailForm');

saveLink.onclick = function(element) {
  chrome.tabs.query({'active': true, 'lastFocusedWindow': true}, function (tabs) {
      var url = tabs[0].url;
      saveLink.innerHTML= url;
  });
};

function init(){
  chrome.storage.sync.get(['emailAddress'], function(items ){
    console.log(items.emailAddress);
      if(typeof(items.emailAddress) !== "string"){
        saveLink.style.display = 'none';
        emailForm.style.display = 'block';
      }

  });  
}

saveEmail.onclick = function(emailAddress) {
    emailAddress = document.getElementById('emailInput').value;
    console.log(emailAddress);
    chrome.storage.sync.set({'emailAddress': emailAddress});
};

init();