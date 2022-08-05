function getCliente(){
    var id_cliente = window.location.search.substring(1);
    console.log("id_cliente: " + id_cliente);

    var token = sessionStorage.getItem('id');
    console.log(token)
    var request = new XMLHttpRequest();
    request.open("GET","http://127.0.0.1:8000/clientes/" + id_cliente,true);
    request.setRequestHeader("Authorization", "Bearer " + token);
    request.setRequestHeader("Accept","application/json");
    

    

    request.onload = () => {
        const response = request.responseText;
        const json = JSON.parse(response);
        const status = request.status;

        console.log("Response: " + response);
        console.log("JSON: " + json);
        console.log("Status: " + status);
        
        
        if(status == 200){
            let nombre = document.getElementById("nombre");
            let email = document.getElementById("email");
            nombre.value = json.nombre;
            email.value = json.email;

        }
        else if (status == 404){
            let nombre = document.getElementById("nombre");
            let email = document.getElementById("email");
            nombre.value = "None";
            email.value = "None";
            alert(json.detail);
        }
    };
    request.send();
};