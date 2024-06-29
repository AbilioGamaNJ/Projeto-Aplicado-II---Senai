const inputs = document.querySelectorAll(".input");


function addcl(){
	let parent = this.parentNode.parentNode;
	parent.classList.add("focus");
}

function remcl(){
	let parent = this.parentNode.parentNode;
	if(this.value == ""){
		parent.classList.remove("focus");
	}
}


inputs.forEach(input => {
	input.addEventListener("focus", addcl);
	input.addEventListener("blur", remcl);
});


function ShowPassword(){
  var inputPass = document.getElementById('passwordI')
  var btnShowPass = document.getElementById('btn-password')

  if(inputPass.type === 'password'){
      inputPass.setAttribute('type', 'text')
      btnShowPass.classList.replace('bi-eye-fill', 'bi-eye-slash-fill')
  }else{
      inputPass.setAttribute('type', 'password')
      btnShowPass.classList.replace('bi-eye-slash-fill', 'bi-eye-fill',)
  }
}

function Logar() {
  window.location = "./dadoscolaborador.html"
}