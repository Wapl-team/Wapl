const share = document.querySelector(".share");
const modal_share = document.querySelector(".modal-share");
const share_box = document.querySelector(".share-box");

share.addEventListener("click", () => {
  modal_share.classList.toggle("hidden");
});

modal_share.addEventListener("click", (e) => {
  if (e.target == modal_share) {
    modal_share.classList.toggle("hidden");
  }
});

const share_save = () => {
  const share_select = document.querySelectorAll(".share-select input");
  share_select.forEach((share) => {
    if (share.checked == true) {
      shareOBJ[share.id.split("-")[0]] = share.id.split("-")[1];
    }
  });
  modal_share.classList.add("hidden");
};
