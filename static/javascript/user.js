const url = new URL(window.location.href);
const userUrl = url.href;
const string = url.pathname;
const userId = string.replace('/user/', '');
const userApi = '/api/user';
const urlApi = '/api/url';
let userName = document.querySelector('#user-name');
let userData = null;
let urlData = null;

window.onload = () => {
  init();
};

async function init() {
	userData = await getUserData();
	if (userData.data === null) {
	  location.href = '/';
	} else if (userData.error) {
	  location.href = '/';
	} else if (userId != String(userData.data.id)) {
		location.href = '/';
	} else {
		let shortUrl = document.querySelector('#short-url');
		userName.textContent = userData.data.name
		if(userData.data.pathName === null || userData.data.pathName === '') {
		}
		else {
			shortUrl.href = `/short-url/${userData.data.pathName}`;
			shortUrl.textContent = `http://54.221.150.42/short-url/${userData.data.pathName}`;
		}
	}
}

function getUserData() {
	return fetch(userApi)
	  .then((response) => {
		return response.json();
	  })
	  .then((result) => {
		return result;
	  });
}

function signOut(){
	let headers = {
		'Content-Type': 'application/json',
		'Accept': 'application/json'
	}
	fetch(userApi,{
		method: 'DELETE',
		headers: headers,
	}).then(function(response){
		return response.json();
	}).then(function(result){
		userData = result
		location.href = '/' 
	})
}

function generateUrl() {
	let headers = {
		'Content-Type': 'application/json',
		'Accept': 'application/json'
	}
	let body = {
		'userId': userData.data.id,
		'longUrl': userUrl
	}
	fetch(urlApi,{
		method: 'POST',
		headers: headers,
		body: JSON.stringify(body)
	}).then(function(response){
		return response.json();
	}).then(function(result){
		urlData = result
		if(urlData.ok) {
			let shortUrl = document.querySelector('#short-url');
			shortUrl.href = `/short-url/${urlData.pathName}`;
			shortUrl.textContent = `http://54.221.150.42/short-url/${urlData.pathName}`;
		}
	})
}

function modifyBtn() {
	let showInput = document.querySelector('#modify-url');
	showInput.style.display = 'block';
}

function modifyUrl() {
	let pathName = document.querySelector('#path-name');
	let headers = {
		'Content-Type': 'application/json',
		'Accept': 'application/json'
	}
	let body = {
		'userId': userData.data.id,
		'newPathName': pathName.value
	}
	fetch(urlApi, {
		method: 'PATCH',
		headers: headers,
		body: JSON.stringify(body)
	}).then(function(response){
		return response.json();
	}).then(function(result){
		if(result.ok) {
			window.location.replace(location.href) 
		}else {
			let failedMessage = document.querySelector('#failed-message');
			failedMessage.textContent = result.message
		}
	})
}

function deleteUrl() {
	let headers = {
		'Content-Type': 'application/json',
		'Accept': 'application/json'
	}
	let body = {
		'userId': userData.data.id
	}
	fetch(urlApi, {
		method: 'DELETE',
		headers: headers,
		body: JSON.stringify(body)
	}).then(function(response){
		return response.json();
	}).then(function(result){
		urlData = result
		if(urlData.ok) {
			window.location.replace(location.href) 
		}
	})
}