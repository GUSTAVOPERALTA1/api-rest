    function postCliente(){
        let nombre = document.getElementById("nombre");
        let email = document.getElementById("email");
        
        let payload = {
            "nombre": nombre.value,
            "email": email.value
        }
        console.log("nombre: " + nombre.value);
        console.log("email: " + email.value);

        var request = new XMLHttpRequest();
        request.open("POST","http://127.0.0.1:8000/clientes/",true);
        request.setRequestHeader("Content-Type","application/json");
        request.setRequestHeader("Accept","application/json");

        request.onload = () => {
            const response = request.responseText;
            const json = JSON.parse(response);
            const status = request.status;

            console.log("Response: "+ response);
            console.log("JSON: " + json);
            console.log("Status: " + status);

            if(status == 200){
                alert(json.message);
                window.location.replace("/get_productos.html");
            }
        };
        request.send(JSON.stringify(payload));
    };