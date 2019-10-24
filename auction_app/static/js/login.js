var login = function() {
	username = document.querySelector('#username').value;
	password = document.querySelector('#password').value;
	console.log(username);
	if (username === "") {
		document.querySelector('#username').placeholder = "Input Username";
		return;
	}
	else {
		var loginUrl = `http://${location.hostname}:8000/login/?username=${username}&password=${password}`;
		fetch(loginUrl)
			.then(conversion => conversion.json() )
			.then( conversion => {
				if (conversion.hasOwnProperty('error')) {
					console.log(conversion.error);
					document.querySelector('#message').textContent = conversion.error;
				}
				else if (isNaN(pricePerToz)) {
					console.log(pricePerToz);
					document.querySelector('#result').textContent = "Something wrong with quandl number";
				}
				else if (isNaN(conversion['value'])) {
					console.log(conversion['value']);
					console.log(conversion);
					document.querySelector('#result').textContent = "Something wrong with value number";
				}
				else {
					let dollarAmount = pricePerToz * conversion['value'];
					// stack overflow gave me toFixed() for precision
					document.querySelector('#result').textContent = "Your weight in gold is worth $" + dollarAmount.toFixed(2);
				}
			});
	}
}