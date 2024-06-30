const hamBurger = document.querySelector(".toggle-btn");

hamBurger.addEventListener("click", function () {
  document.querySelector("#sidebar").classList.toggle("expand");
});


button_dados = document.querySelector(".buttonDados");

button_dados.onclick = function() {
    this.innerHTML = "<div class='loader'></div>";
    setTimeout(() => {
      this.innerHTML = "Dowload Concluído"
      this.style = "background: #f1f5f4; color: #333;pointer-events: none";
    }, 2000);
}
