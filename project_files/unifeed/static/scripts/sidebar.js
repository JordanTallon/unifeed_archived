function toggleSidebar() {
  var leftSidebar = document.getElementById("left-sidebar");
  leftSidebar.classList.toggle("hidden");

  var overlay = document.getElementById("overlay");
  overlay.classList.toggle("hidden");

  var menuToggle = document.getElementById("menu-toggle");
  menuToggle.classList.toggle("closed");
}
