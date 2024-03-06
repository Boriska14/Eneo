document.getElementById('login').addEventListener(
    'submit',function(event){
        event.preventDefault();
        var username = document.getElementById('username').value;
        var password = document.getElementById('password').value;

        fetch("http://localhost:8000/login/", {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify({
              username: username,
              password: password,
            }),
          })
            .then(async (response) => {
              if (response.ok) {
                const data = await response.json();

                const userRole = data.role;
                if (userRole === 'admin') {
                    window.location.href = 'dashboard.html';
                  } else if (userRole === 'utilisateur') {
                    window.location.href = '/utilisateur';
                  } else {
                    // Afficher un message d'erreur
                    alert("Rôle utilisateur non reconnu.");
                  }
              
                document.getElementById("login").reset();
              } else {
                throw new Error("Une erreur s/'est produite lors de la connexion");

              }
            })
            .catch((error) => {
              alert(error.message);
            });
    
         

    });