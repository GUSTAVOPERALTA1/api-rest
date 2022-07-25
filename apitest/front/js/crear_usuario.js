function postUsuario(){
    var email = document.getElementById("email").value;
    var password = document.getElementById("password").value;
 
     var  datos ={
         "email": email,
         "password": password,
     }
     var request = new XMLHttpRequest();
 
     request.open("POST","http://127.0.0.1:8000/user",true); 
     request.setRequestHeader("Accept", "application/json");
     request.setRequestHeader("Content-Type", "application/json");
 
     request.onload = ()=>{
        const status = request.status
 
         if (status == 202){
             alert("Usuario Creado");
             window.location.replace("/index.html");
 
         }
         else if(status == 422){
             
             alert("Error");
         
             
         }
     };
     request.send(JSON.stringify(datos));
 };