function putCliente(){
    var id_cliente = window.location.search.substring(1);
    let id_clientecap = id_cliente;
    let nombre = document.getElementById("nombre");
    let email  = document.getElementById("email");
    let payload = {
        "id_cliente": id_clientecap,
        "nombre": nombre.value,
        "email" : email.value,
    }

    console.log("id_cliente: " + id_cliente);
    console.log("nombre: " + nombre.value);
    console.log("email: "  + email.value);
    console.log(payload);
    var token = sessionStorage.getItem('id');
    console.log(token)
    var request = new XMLHttpRequest();
    request.open('PUT', "http://127.0.0.1:8000/clientes/",true);
    request.setRequestHeader("Authorization", "Bearer " + token);
    request.setRequestHeader("Accept", "application/json");
    request.setRequestHeader("content-type", "application/json");

    request.onload = () => {
        
        const response = request.responseText;
        const json = JSON.parse(response);     
        const status = request.status;

        if (request.status === 401 || request.status === 403) {
            alert(json.detail);
        }

        else if (request.status == 202){

            console.log("Response: " + response);
            console.log("JSON: " + json);
            console.log("Status: " + status);

            alert(json.message);
            window.location.replace("get_list.html")
        }
    };
    request.send(JSON.stringify(payload));
}