function Login(){
    let email = document.getElementById("email").value;
    let password = document.getElementById("pword").value;

    var request = new XMLHttpRequest();
    request.open("GET","http://127.0.0.1:8000/user/validate/",true);
    request.setRequestHeader("Authorization", "Basic " + btoa(email + ":" + password));
    request.setRequestHeader("Content-Type", "application/json");
    request.setRequestHeader("Accept","application/json");
    request.onload = () =>{
        const response = request.responseText;
        const status = request.status
        const json = JSON.parse(request.responseText,response);
        console.log("Response: " + response);
        console.log("JSON: " + json);

        if (status == 202) {
            alert("Bienvenid@, copia el siguiente TOKEN para realizar operaciones CRUD");
            alert(response)
            window.location.replace("/get_list.html"); 
            
        }
        else{
            alert(json.detail);
        }
    };
   request.send();
};