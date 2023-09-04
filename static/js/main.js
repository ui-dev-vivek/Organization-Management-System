var currentPageURL = window.location.href;
var menuItems = document.querySelectorAll(".menu-item");
menuItems.forEach(function (menuItem) {  
  var link = menuItem.querySelector("a");
  var href = link.getAttribute("href");
   if (currentPageURL.indexOf(href) !== -1) {    
    menuItem.classList.add("active");
    var menuToggleParent = findNearestParentWithClass(menuItem, "menu-items");
    if (menuToggleParent) {
      menuToggleParent.classList.add("active");
      menuToggleParent.classList.add("open");
    }
  }
});
function findNearestParentWithClass(element, className) {
  while (element) {
    if (element.classList.contains(className)) {
      return element;
    }
    element = element.parentElement;
  }
  return null; 
}