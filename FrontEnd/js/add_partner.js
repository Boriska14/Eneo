document.getElementById('partner_form').addEventListener(
    'submit',function(event){
        event.preventDefault();
        var name = document.getElementById('name').value;
        var description = document.getElementById('description').value;

        fetch("http://localhost:8000/partners_create", {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify({
              name: name,
              description: description,
            }),
          })
            .then((response) => {
              if (response.ok) {
                alert("Partenaire ajouté avec succès!");
                document.getElementById("partner_form").reset();
              } else {
                throw new Error("Une erreur s/'est produite lors de l/'ajout du partenaire");
              }
            })
            .catch((error) => {
              alert(error.message);
            });
      

        fetch("http://172.20.176.1:8000/").then((Response) => {
            return Response.json()
        }).then((data) => {
            console.log(data);
        })


    });