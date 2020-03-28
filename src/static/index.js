document.addEventListener('DOMContentLoaded', () => {

    document.querySelector('#form').onsubmit = () => {

        // Initialize new request
        //const request = new XMLHttpRequest();
        //const name = document.querySelector('#agency_name').value;
        //const url = document.querySelector('#agency_url').value;
        //const description = document.querySelector('#agency_description').value;
        //const fil = document.querySelector('#agency_logo')[0]
        request.open('POST', '/add_agency');

        // Callback function for when request completes
        request.onload = () => {

            // Extract JSON data from request
            const data = JSON.parse(request.responseText);

            // Update the result div
            if (data.success) {
               alert("successfully uploaded")
            }
            else {
                alert("Failed")
            }
        }

        // Add data to send with request
        const data = new FormData( document.querySelector('#form')[3]);
        //data.append('name', name);
        //data.append('url', url);
        //data.append('description', description);


        // Send request
        request.send(data);
        return false;
    };

});