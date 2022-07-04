function getProductos(){
    var query = window.location.search.substring(1);
    console.log("Query: "+query)

    //Conectar Backend con Frontend
    var request = new XMLHttpRequest();
    request.open("GET","http://127.0.0.1:8000/clientes/",true);
    request.setRequestHeader("Accept","application/json")
    request.onload = () =>{
        const response = request.responseText;
        const json = JSON.parse(response);

        console.log("Response: " + response);
        console.log("JSON: " + json);

        var tbody = document.getElementById("tbody_clientes");
        for(let row=0; row<json.length; row++){
            var tr = document.createElement("tr");
            var tr_id_cliente = document.createElement("td");
            var tr_nombre = document.createElement("td");
            var tr_email = document.createElement("td");
            
            tr_id_cliente.innerHTML = json[row].id_cliente;
            tr_nombre.innerHTML = json[row].nombre;
            tr_email.innerHTML = json[row].email;

            tr.appendChild(tr_id_cliente);
            tr.appendChild(tr_nombre);
            tr.appendChild(tr_email);

            tbody.appendChild(tr);

        }
    };
    request.send();
};
