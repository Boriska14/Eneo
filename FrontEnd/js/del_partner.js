document.getElementById('del_partner').addEventListener(
    'submit',function(event){
        event.preventDefault();
        var name = document.getElementById('name').value;

        fetch("http://localhost:8000/partners_delete/", {
            method: "DELETE",
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify({
              name: name,
            }),
          })
            .then((response) => {
              if (response.ok) {
                alert("Partenaire supprimé avec succès!");
                document.getElementById("del_partner").reset();
              } else {
                throw new Error("Une erreur s/'est produite lors de la suppression du partenaire");
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