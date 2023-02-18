const member = document.querySelector(".meeting__members");
const modal__member = document.querySelector(".modal-member");

member.addEventListener("click",()=>{
  modal__member.classList.remove("hidden")
});

modal__member.addEventListener("click",(e)=>{
  modal__member.classList.add("hidden");
});