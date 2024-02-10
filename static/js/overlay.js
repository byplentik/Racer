const showOverlay = () => {
  document.getElementById("custom-overlay").style.display = "flex";

  document
    .getElementById("custom-overlay")
    .addEventListener("click", closeModalOnOverlayClick);
};

const closeModal = () => {
  document.getElementById("custom-overlay").style.display = "none";

  document
    .getElementById("custom-overlay")
    .removeEventListener("click", closeModalOnOverlayClick);
};

const closeModalOnOverlayClick = (event) => {
  if (event.target.id === "custom-overlay") {
    closeModal();
  }
};
