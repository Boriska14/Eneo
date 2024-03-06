document.getElementById('del_user').addEventListener(
    'submit',function(event){
        event.preventDefault();
        var username = document.getElementById('username').value;

        fetch("http://localhost:8000/users/", {
            method: "DELETE",
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify({
              username: username,
            }),
          })
            .then((response) => {
              if (response.ok) {
                alert("utilisateur supprimé avec succès!");
                document.getElementById("del_user").reset();
              } else {
                throw new Error("Une erreur s/'est produite lors de la suppression de l'utilisateur");
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