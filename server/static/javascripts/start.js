function openToggle() {
    // document.getElementById("sidebar").style.width = "250px";
    // document.getElementById("sidebar").style.paddingTop = "2rem";
    // document.getElementById("sidebar").style.paddingBottom = "2rem";
    document.getElementById("sidebar").style.visibility="visible";
    document.getElementById("sidebar").style.transition="all s0.1s";
    document.getElementById("sidebar").style.opacity="1";
    document.getElementById("sidebar").style.borderRight="2px solid rgba(173,168,168,0.5)";
  }
  
  function closeToggle() {
    // document.getElementById("sidebar").style.width = "0";
    // document.getElementById("sidebar").style.paddingTop = "0";
    // document.getElementById("sidebar").style.paddingBottom = "0";
    document.getElementById("sidebar").style.visibility="hidden";
    document.getElementById("sidebar").style.transition="all 0.1s";
    document.getElementById("sidebar").style.opacity="0";
  }

const navBtn = document.querySelector(".nav_bar_button");
const sidebarMenu = document.querySelector(".sidebar-menu");
const closeBtn = document.querySelector(".closeBtn");
const logo= document.querySelector(".logo-container");
const introContainer = document.querySelector(".introduction-container");
const introContainerReverse = document.querySelector(".introduction-container-reverse");

navBtn.addEventListener("click", () => {
  openToggle();
});

closeBtn.addEventListener("click", () => {
  closeToggle();
});

sidebarMenu.addEventListener("click", (e) => {
  closeToggle();
});

logo.addEventListener("click", (e) => {
  closeToggle();
});
introContainer.addEventListener("click", (e) => {
  closeToggle();
});
introContainerReverse.addEventListener("click", (e) => {
  closeToggle();
});