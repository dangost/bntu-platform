
async function addFile() {
    let input = document.createElement("input");
    input.type = 'file';


    input.onchange = e => {
        let file = e.target.files[0];
        let filename = file.name;
        let reader = new FileReader();
        reader.readAsDataURL(file); // this is reading as data url
       // here we tell the reader what to do when it's done reading...
       reader.onload = readerEvent => {
           let content = readerEvent.target.result; // this is the content!
           let writing = false;
           let cutBase64 = "";
           for (let i = 0; i < content.length; i++) {
               if (writing) {
                   cutBase64 += content[i];
               }
               else {
                   if (content[i] === ','){
                       writing = true;
                   }
               }
           }
           let current_image = document.getElementById("current_image");

            const response = postRequest(
                "/api/files/upload-image",
                {
                    "filename": filename,
                    "base64": cutBase64
                }
            ).then(async response => {
                let data = await response.json();
                current_image.alt = data.file_id;
            });

           current_image = document.getElementById("current_image");
           current_image.src = content;
       }

    }
    input.click();
}


async function sendMenu()  {
    let current_image = document.getElementById("current_image");
    let file_id = current_image.alt;

    let payload = {"image": `/api/files/images/${file_id}`};

    const response = await postRequest("/api/canteens/update", payload);

    alert("Меню вашей столовой было обновлено")

}