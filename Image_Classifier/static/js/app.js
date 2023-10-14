// Function to handle image selection and encoding

/*function handleImage() {
    const imageInput = document.getElementById('imageInput');
    const encodeButton = document.getElementById('encodeButton');
    const encodedImage = document.getElementById('encodedImage');

    imageInput.addEventListener('change', function () {
        const selectedImage = imageInput.files[0];

        if (selectedImage) {
            const reader = new FileReader();
            reader.onload = function (event) {
                const base64String = event.target.result.split(',')[1];
                encodedImage.innerHTML = `<p>Base64-Encoded Image:</p><img src="data:image/jpeg;base64,${base64String}" />`;

                // You can send the base64String to the server via a POST request here
                sendImageToServer(base64String);
            };
            reader.readAsDataURL(selectedImage);
        }
    });

    encodeButton.addEventListener('click', function () {
        imageInput.click();
    });
}

// Call the function when the document is ready
document.addEventListener('DOMContentLoaded', handleImage);

// Function to send the base64 image data to the server
function sendImageToServer(base64Data) {
    $.ajax({
        url: "/home/",  // Update the URL to match your Django view URL
        type: 'POST',
        data: { image_data: base64Data },  // Sending image data as form data
        success: function (data, status) {
            if (data && data.length > 0) {
                // Assuming you are using AJAX to load 'result.html'
                $("#content").load("result.html", { result: data });
            } else {
                // Handle error
            }
        }
    });
}









/*Dropzone.autoDiscover = false;

$(document).ready(function() {
    console.log( "ready!" );
    $("#error").hide();
    $("#resultHolder").hide();
    $("#divClassTable").hide();

    init();
});

function init() {
    let dz = new Dropzone("#dropzone", {
        url: " ",
        maxFiles: 1,
        paramName: "image_data",
        addRemoveLinks: true,
        dictDefaultMessage: "Some Message",
        autoProcessQueue: false
    });
    
    dz.on("addedfile", function() {
        if (dz.files[1]!=null) {
            dz.removeFile(dz.files[0]);        
        }
    });

    dz.on("complete", function (file) {
        let image_data = file.dataURL;
        
        var url = "http://127.0.0.1:8000/";

        $.ajax({
            url: url,
            type: 'POST',
            data: JSON.stringify({ image_data: image_data }),  // Send data as JSON
            contentType: 'application/json',  // Set content type to JSON
            success: function (data, status) {
            
            console.log(data);
            if (!data || data.length==0) {
                $("#resultHolder").hide();
                $("#divClassTable").hide();                
                $("#error").show();
                return;
            }
            let players = ["Atif_Aslam", "Babar_Azam", "Emma_Watson", "James_Macvoy", "Momina_Mustehsan"];
            
            let match = null;
            let bestScore = -1;
            for (let i=0;i<data.length;++i) {
                let maxScoreForThisClass = Math.max(...data[i].class_probability);
                if(maxScoreForThisClass>bestScore) {
                    match = data[i];
                    bestScore = maxScoreForThisClass;
                }
            }
            if (match) {
                $("#error").hide();
                $("#resultHolder").show();
                $("#divClassTable").show();
                $("#resultHolder").html($(`[data-player="${match.class}"]`).html());
                let classDictionary = match.class_dictionary;
                for(let personName in classDictionary) {
                    let index = classDictionary[personName];
                    let proabilityScore = match.class_probability[index];
                    let elementName = "#score_" + personName;
                    $(elementName).html(proabilityScore);
                }
            }
            // dz.removeFile(file);            
        }});
    });

    $("#submitBtn").on('click', function (e) {
        dz.processQueue();		
    });
}
*/
