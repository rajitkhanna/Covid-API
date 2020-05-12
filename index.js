const URL = "https://gt-covid-api.herokuapp.com";
const method = "POST";
const body = {
	age: 100,
	conditions: ["Cardiovascular disease"]
};
fetch(URL , {
    method: method,
    headers:  {
        Accept: 'application/json',
        'Content-Type': 'application/json'
      },
    body: JSON.stringify(body)
})
    .then(data => {return data.json()})
    .then(json => {document.getElementById("request").innerHTML = json["probability"]})
    .catch(error => {console.error(error)})