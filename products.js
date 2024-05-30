const api = "http://127.0.0.1:5000";

window.onload = () => {
    // BEGIN CODE HERE

    // END CODE HERE
}

searchButtonOnClick = () => {
    // BEGIN CODE HERE

    // END CODE HERE
}

productFormOnSubmit = (event) => {
    // BEGIN CODE HERE


    //Getting the form element
    const form = document.getElementById('inputForms');
    //Extracting form data
    const name = form.elements['name'].value;
    const production_year = form.elements['production_year'].value;
    const price = form.elements['price'].value;
    const size = form.elements['size'].value;
    const color = form.elements['color'].value;

    //Checking if the data is valid
    if(!name || !production_year || !price || !size || !color)
    {
        alert("All attributes must have a value");
    }
    else if(production_year.match(/^[0-9]+$/) == null)
    {
        alert("production_year must only contain numbers");
    }
    else if(isNaN(parseFloat(price)))
    {
        alert("price must only contain '.' and digits");
    }
    else if(color != 1 && color != 2 && color != 3)
    {
        alert("color must be 1 or 2 or 3")
    }
    else if(size != 1 && size != 2 && size != 3 && size != 4)
    {
        alert("size must be 1 or 2 or 3 or 4")
    }
    else
    {
        //Creating the XMLHttpRequest object
        const res = new XMLHttpRequest();
        //Creating POST request to the /add-product endpoint
        res.open("POST", api + "/add-product");
        //Handling the response
        res.onreadystatechange = function() {
        if (res.readyState == 4) {
         if (res.status == 201 || res.status == 200)
         {
             //Alerting the user that the request was accepted
             alert("OK");
             //Clearing the text inputs
             form.elements['name'].value = '';
             form.elements['production_year'].value = '';
             form.elements['price'].value = '';
             form.elements['size'].value = '';
             form.elements['color'].value = '';
             }
             else
             {
             //Alerting the user that the request was not accepted
             alert("NOT OK");
             }
         }
        };
        res.setRequestHeader("Content-Type", "application/json;charset=UTF-8");


        //Calculating the id from the number of stored products
        var id = 0;
        //Creating a GET request to the /search endpoint
        var xhr = new XMLHttpRequest();
        xhr.open("GET", api + "/search", false);
        xhr.onreadystatechange = function() {
        if (xhr.readyState == 4) {
         if (xhr.status == 200)
         {
             //Setting the id of the new product
             id = JSON.parse(xhr.response).length + 1;
             }
             else
             {
             //Alerting the user that the request was not accepted
             alert("GET /search request not accepted");
             }
         }
        };
        xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
        //Sending GET request
        xhr.send();


        //Creating the JSON object with form data
        const data = {
         "id": id.toString(),
         "name": name,
         "production_year": parseInt(production_year),
         "price": parseFloat(price),
         "size": parseInt(size),
         "color": parseInt(color)
        };
        //Sending the POST request
        res.send(JSON.stringify(data));
    }


    // END CODE HERE
}
