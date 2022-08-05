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
        const data = JSON.parse(response);
        console.log(data.token);

        if (status == 202) {
            alert("Bienvenid@, este es tu token para realizar operaciones CRUD");
            alert(data.token)
            sessionStorage.setItem("id",data.token);
            window.location.replace("/get_list.html"); 
            
        }
        else{
            alert(json.detail);
        }
    };
   request.send();
};