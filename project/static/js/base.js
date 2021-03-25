messages = document.querySelector(".messages");
var items = messages.getElementsByTagName("li");

for (item of items) {
  setTimeout(function () {
    item.classList.add("hide");
  }, 5000);
}
