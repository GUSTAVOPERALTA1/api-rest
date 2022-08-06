function deleteClientes(){
    var query = window.location.search.substring(1);
    var token = sessionStorage.getItem('id');
    console.log(token)
    console.log("id_cliente: " + query);
    var request = new XMLHttpRequest();
    request.open("DELETE","http://127.0.0.1:8000/clientes/?"+ query,true);
    request.setRequestHeader("Authorization", "Bearer " + token);
    request.setRequestHeader("Content-Type","application/json");
    request.setRequestHeader("Accept","application/json");


    request.onload = () =>{
        const response = request.responseText;
        const json = JSON.parse(response);
        const status = request.status;
    
        console.log("Response: " + response);
        console.log("JSON: " + json);
        console.log("Status: " + status);
        
        if(status == 202){
            console.log("Eliminar")
            alert(json.message);
            window.location.replace("/get_list.html");
        }
    };
    request.send();
};
    