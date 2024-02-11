// For bootstrap 5 popovers https://getbootstrap.com/docs/5.0/components/popovers/
var popoverTriggerList = [].slice.call(
  document.querySelectorAll('[data-bs-toggle="popover"]')
);
var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
  return new bootstrap.Popover(popoverTriggerEl);
});

// For the 'Go back' buttons to go back 1 page in the browser.
function goBack() {
  window.history.back();
}
