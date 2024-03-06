document.getElementById('add_user').addEventListener(
    'submit',function(event){
        event.preventDefault();
        var username = document.getElementById('username').value;
        var password = document.getElementById('password').value;
        var role = document.querySelector('input[name="role"]:checked').value;

        fetch("http://localhost:8000/register/", {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify({
              username: username,
              password: password,
              role:role,
            }),
          })
            .then((response) => {
              if (response.ok) {
                alert("Partenaire ajouté avec succès!");
                document.getElementById("add_user").reset();
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