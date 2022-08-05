function Login(){
    let email = document.getElementById("email").value;
    let password = document.getElementById("pword").value;

    var request = new XMLHttpRequest();
    request.open("GET","http://127.0.0.1:8000/user/validate/",true);
    request.setRequestHeader("Authorization", "Basic " + btoa(email + ":" + password));
    request.setRequestHeader("Content-Type", "application/json");
    request.setRequestHeader("Accept","application/json");
    request.onload = () =>{
        const status = request.status
        json = JSON.parse(request.responseText);

        if (status == 202) {
            alert("Inicio Correcto");
            window.location.replace("/bienvenida.html"); 
        }
        else{
            alert(json.detail);
        }
    };
   request.send();
};