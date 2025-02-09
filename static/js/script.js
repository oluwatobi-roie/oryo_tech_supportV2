// toggle forms in admin to display project and product forms
function toggleForm(formId, fetchData = false){
    var form = document.getElementById(formId)
    var isHidden = form.style.display === 'none' || form.style.display === '';
    form.style.display = isHidden ? 'block' : 'none'
    console.log(fetchData, formId)
    if (isHidden && fetchData){
        fetchCustomerData();
    }
}

// gets the list of customers from backend
function fetchCustomerData(){
    fetch('/admin/projects')
    .then(response=> response.json())
    .then(data => {
        const customerSelect = document.getElementById('customer_id');
        customerSelect.innerHTML = '';

    data.forEach(customer => {
        const option = document.createElement('option');
        option.value = customer.id;
        option.textContent = customer.name;
        customerSelect.appendChild(option);
    })
    })
    .catch(error => console.error('Error fetching customers: ', error))
}




// select Product table
const productSelect = document.getElementById("product_id");
const dynamicFieldsContainer = document.getElementById("dynamicFields");

function generateFields(fields, containerName) {
    console.log(fields);
    containerName.innerHTML = ""; // Clear previous fields

    // Loop through each field and its respective input type
    Object.entries(fields).forEach(([field, inputType]) => {
        let div = document.createElement("div");
        div.className = "mb-2";

        // Generate the appropriate input element based on inputType
        let inputElement;
        switch (inputType) {
            case "checkbox":
                inputElement = `
                    <select id="${field}" name="${field}" class="form-control required">
                        <option value="Yes">Yes</option>
                        <option value="No">No</option>
                    </select>`;
                break;
            case "text":
                inputElement = `<input type="text" id="${field}" name="${field}" class="form-control" required>`;
                break;
            case "number":
                inputElement = `<input type="number" id="${field}" name="${field}" class="form-control" required>`;
                break;
            case "datetime-local":
                inputElement = `<input type="datetime-local" id="${field}" name="${field}" class="form-control" required>`;
                break;
            case "file":
                inputElement = `<input type="file" id="${field}" name="${field}" class="form-control" required>`;
                break;
            default:
                inputElement = `<input type="text" id="${field}" name="${field}" class="form-control" required>`;
        }

        // Generate the HTML for the field with the appropriate input type
        div.innerHTML = `
            <label for="${field}" class="form-label">${field.replace(/_/g, " ")}</label>
            ${inputElement}
        `;
        
        containerName.appendChild(div);
    });
}



// tech support edit modal class
// Handle button click to open modal
// Handle button click to open modal
document.querySelectorAll('.support-edit-btn').forEach(button => {
    button.addEventListener('click', function() {
        // Get the data from the button's attributes
        const installationId = this.getAttribute('data-id');
        const productId = this.getAttribute('data-product_id');
        const stageId = +this.getAttribute('data-stage_id')+1 ;
        const productDescription = this.getAttribute('data-product');
        const technician = this.getAttribute('data-technician');
        const deviceImei = this.getAttribute('data-deviceImei');
        const tabletestContainer = document.getElementById("dynamicFields_tabletest");

        // Populate the modal form with the data
        document.getElementById('technician').value = technician;
        document.getElementById('installationId').value = installationId
        document.getElementById('stageId').value = stageId
 
        // Update the modal title dynamically
        const modalTitle = document.getElementById('editTaskLabel');
        modalTitle.textContent = `${productDescription}: ${deviceImei} Task ID: ${installationId} `;

        if(installationId){
            console.log(deviceImei)
            fetch(`/support/addtask/get_product_fields/${productId}/${stageId}`)
            .then(response => response.json())

            .then(data => {
                if (data.fields) {
                    generateFields(data.fields, tabletestContainer)
                }
            })
            .catch(error => console.error("Error Fetching product fields: ", error))
        }

        // Show the modal
        const modal = new bootstrap.Modal(document.getElementById('editTask'), {focus:true});
        modal.show();
    });
});


// Handle button to view Profile on tech support page
document.querySelectorAll('.support-edit-btn-verify').forEach(button =>{
    button.addEventListener('click', function(){
        const installationId = this.getAttribute('data-id')

        // Update the modal title dynamically
        const modalTitle = document.getElementById('installation-profile-heading');
        modalTitle.textContent = "This is Installation Profile"
    })

})

function validateFile(input) {
    const allowedExtensions = ["jpg", "jpeg", "png", "heif"];
    const file = input.files[0]; // Get the uploaded file

    if (file) {
        const fileExt = file.name.split('.').pop().toLowerCase(); // Get file extension
        if (!allowedExtensions.includes(fileExt)) {
            alert("Invalid file type. Only JPG, JPEG, PNG, and HEIF are allowed.");
            input.value = ""; // Reset the input field
        }
    }
}


// validate upload files are allowed.
document.getElementById("installation_Update_Form").addEventListener("change", function (event) {
    if (event.target.type === "file") {
        validateFile(event.target);
    }
});





// // Submitting update task button
document.getElementById("installation_Update_Form").addEventListener("submit", function (event) {
    event.preventDefault();

    let form = document.getElementById("installation_Update_Form");
    let formData = new FormData(form); // Collects all form fields, including files

    console.log("Sending Data:", formData); // Debugging

    document.querySelectorAll("#installation_Update_Form input, #installation_Update_Form select")
    .forEach((field)=> {
        let name = field.name;
        let value = field.value.trim();
        if (name) formData[name] = value;
    });


    $.ajax({
        url: "/support/addtask",
        type: "PUT",
        contentType: "application/json",
        data: formData,
        processData: false,  // Important: Prevent jQuery from converting `FormData` to a string
        contentType: false,  // Important: Let the browser set `multipart/form-data`
        success: function (response) {
            console.log("Response:", response);
            $("#message").html(
                `<div class="alert alert-success">${response.message}</div>`
            );
            // Close modal
            const modal = bootstrap.Modal.getInstance(document.getElementById('editTask'));
            modal.hide();
            $.ajax({
                url: "/support",
                type: "GET",
                success: function(updatedData){
                    $('#taskList').html($(updatedData).find('#taskList').html());
                }
            })
        },
        error: function (xhr) {
            console.error("Error:", xhr.responseJSON);
            $("#editTaskMessage").html(
                `<div class="alert alert-danger">${xhr.responseJSON.error}</div>`
            );
        },

    });
});



if (productSelect){
    productSelect.addEventListener("change", function () {
        let selectedProduct = productSelect.value;
    
        if (selectedProduct) {
            fetch(`/support/addtask/get_product_fields/${selectedProduct}/1`)
                .then(response => response.json())
                .then(data => {
                    if (data.fields) {
                        generateFields(data.fields, dynamicFieldsContainer);
                    }
                })
                .catch(error => console.error("Error fetching product fields:", error));
        } else {
            dynamicFieldsContainer.innerHTML = "";  // Clear fields if no product selected
        }
    });
}



// Submitting add task button
$(document).ready(function () {
    $("#taskForm").submit(function (event) {
        event.preventDefault();

        let formData = {};

        $("#taskForm")
            .find("input, select")
            .each(function () {
                let name = $(this).attr("name");
                let value = $(this).val();
                if (name) formData[name] = value; // Only add non-empty names
            });

        console.log("Sending Data:", formData); // Debugging

        $.ajax({
            url: "/support/addtask",
            type: "POST",
            contentType: "application/json",
            data: JSON.stringify(formData),
            success: function (response) {
                console.log("Response:", response);
                $("#message").html(
                    `<div class="alert alert-success">${response.message}</div>`
                );
                $("#taskForm")[0].reset();
                $("#dynamicFields").html(""); // Clear dynamic fields
            },
            error: function (xhr) {
                console.error("Error:", xhr.responseJSON);
                $("#message").html(
                    `<div class="alert alert-danger">${xhr.responseJSON.error}</div>`
                );
            },
        });
    });
}); 
