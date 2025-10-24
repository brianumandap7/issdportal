window.addEventListener("load", function() {
  setTimeout(function() {
    document.getElementById("loader").style.display = "none";
    document.getElementById("page-content").style.visibility = "visible";
  }, 2000); // 2 seconds
});

