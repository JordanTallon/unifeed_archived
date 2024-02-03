function toggleSidebar() {
  var leftSidebar = document.getElementById("left-sidebar");
  leftSidebar.classList.toggle("hidden");

  var overlay = document.getElementById("overlay");
  overlay.classList.toggle("hidden");

  var menuToggle = document.getElementById("menu-toggle");
  menuToggle.classList.toggle("closed");
}

/* var leftSidebar = document.getElementById("left-sidebar");
  var elementsToToggle = document.querySelectorAll(".toggle-text");

  // Check if the elements currently have the 'd-none' class
  // If so, this means that the sidebar is currently hidden
  var isHidden = Array.from(elementsToToggle).some((element) =>
    element.classList.contains("d-none")
  );

  // If the sidebar is hidden
  if (isHidden) {
    var beforeWidth = leftSidebar.offsetWidth;

    // Unhide each hidden element
    elementsToToggle.forEach(function (element) {
      element.classList.toggle("d-none");
    });

    // Use requestAnimationFrame to allow for the browser to reflow if necessary
    requestAnimationFrame(function () {
      var afterWidth = leftSidebar.offsetWidth;
      var diffWidth = afterWidth - beforeWidth;

      // If the diffWidth is greater than 0, it means the sidebar became wider,
      // so we need to adjust the marginRight, to make the page content go underneath the sidebar.
      if (diffWidth > 0) {
        leftSidebar.style.marginRight = `-${diffWidth}px`;
      }

      // zIndex is the 'depth' of the element, the order in which they are rendered. higher index = rendered above.
      leftSidebar.style.zIndex = 9999;
    });
  } else {
    // The menu is open, so the user is closing the menu.
    // Toggle hidden back on
    elementsToToggle.forEach(function (element) {
      element.classList.toggle("d-none");
    });

    // Reset the margin to 0
    leftSidebar.style.marginRight = `0px`;
  } */
