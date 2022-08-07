const userApi = '/api/user';
let userData = null;

let login = document.querySelector('.login');
let loginEmail = document.querySelector('#login-email');
let loginPassword = document.querySelector('#login-password');
let loginFailed = document.querySelector('#login-failed');

let register = document.querySelector('.register');
let registerName = document.querySelector('#register-name');
let registerEmail = document.querySelector('#register-email');
let registerPassword = document.querySelector('#register-password');
let registerFailed = document.querySelector('#register-failed');

function checkLogin(){
	if(loginEmail.value && loginPassword.value){
		let headers = {'Content-Type': 'application/json'}
		let body = {
			'email': loginEmail.value,
			"password": loginPassword.value
		}
		fetch(userApi,{
			method: 'PATCH',
			headers: headers,
			body: JSON.stringify(body)
		}).then(function(response){
			return response.json();
		}).then(function(result){
			userData = result
			if(userData.error === true){
				loginFailed.textContent = userData.message;
			}else{
				location.href = `/user/${userData.userId}`
			}
		})
	}else{
		loginFailed.textContent = '請輸入電子信箱和密碼';
	}
}

function checkRegister(){
	if(registerEmail.value.match(/^([\w\.\-]){1,64}\@([\w\.\-]){1,64}$/) && registerPassword.value.match(/^[0-9a-zA-Z_]+$/)){
		let headers = {
			'Content-Type': 'application/json',
			'Accept': 'application/json'
		}
		let body = {
			'name': registerName.value,
			'email': registerEmail.value,
			'password': registerPassword.value
		}
		fetch(userApi,{
			method: 'POST',
			headers: headers,
			body: JSON.stringify(body)
		}).then(function(response){
			return response.json();
		}).then(function(result){
			userData = result
		if(userData.error === true){
			registerFailed.textContent = userData.message
		}else{
			registerFailed.textContent = '註冊成功，請登入會員帳號'
		}
		})
	}else if(registerName.value === '' || registerEmail.value === '' || registerPassword.value === ''){
		registerFailed.textContent = '請輸入姓名、電子郵件和密碼';
	}else if(!registerEmail.value.match(/^([\w\.\-]){1,64}\@([\w\.\-]){1,64}$/)){
		registerFailed.textContent = '電子信箱格式須包含「@」';
	}else{
		registerFailed.textContent = '請勿在密碼輸入特殊符號';
	}
}