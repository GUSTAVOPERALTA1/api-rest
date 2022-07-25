function Login(){
    let email = document.getElementById("email");
    let password = document.getElementById("pword");
     
    var request = new XMLHttpRequest();
    request.open("GET","http://127.0.0.1:8000/user/validate",true);
    request.setRequestHeader("Authorization","Basic", +btoa(email.value+":"+password.value)); 
    request.setRequestHeader('Content-Type', 'application/json');
    request.setRequestHeader('Accept', 'application/json');
 
     request.onload = function(){
        const status = request.status
        json = JSON.parse(request.responseText);
        
        if(status == 202){
            getInformation(json.token);
            window.location.replace("/bienvenida.html");
        }
        else{
            alert(json.detail);
        }
     };
     request.send();
    };
