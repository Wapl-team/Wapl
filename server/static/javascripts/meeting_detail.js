function openToggle() {
    // document.getElementById("sidebar").style.width = "250px";
    // document.getElementById("sidebar").style.paddingTop = "2rem";
    // document.getElementById("sidebar").style.paddingBottom = "2rem";
    document.getElementById("sidebar").style.visibility="visible";
    document.getElementById("sidebar").style.transition="all 0.1s";
    document.getElementById("sidebar").style.opacity="1";
    document.getElementById("sidebar").style.paddingTop="1rem";
    document.getElementById("sidebar").style.paddingBottom="3rem";
  }
  
  function closeToggle() {
    // document.getElementById("sidebar").style.width = "0";
    // document.getElementById("sidebar").style.paddingTop = "0";
    // document.getElementById("sidebar").style.paddingBottom = "0";
    document.getElementById("sidebar").style.visibility="hidden";
    document.getElementById("sidebar").style.transition="all 0.1s";
    document.getElementById("sidebar").style.opacity="0";
  }
  const navBtn = document.querySelector(".nav-side");
  const sidebarMenu = document.querySelector(".sidebar-menu");
  const closeBtn = document.querySelector(".closeBtn");
  const detailInfo = document.querySelector(".detail__info")
  
  
  navBtn.addEventListener("click", () => {
    openToggle();
  });
  
  closeBtn.addEventListener("click", () => {
    closeToggle();
  });
  
  detailInfo.addEventListener("click", (e) => {
    closeToggle();
  });
  
  sidebarMenu.addEventListener("click", (e) => {
    closeToggle();
  });