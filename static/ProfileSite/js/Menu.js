function moveDiv() {
  var div = document.getElementById("myDiv");

  if (div.style.left === "-250px") {
    div.style.left = "0";
  } else {
    div.style.left = "-250px";
  }
}
