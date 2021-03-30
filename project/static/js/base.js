messages = document.querySelector(".messages");

if (messages){
  var items = messages.getElementsByTagName("li");

for (item of items) {
  setTimeout(function () {
    item.classList.add("hide");
  }, 5000);
}}

carousel_1 = document.querySelector('#heroCarousel').firstElementChild.classList.add('active')

document.querySelector('.highest_rated').firstElementChild.classList.add('active')

