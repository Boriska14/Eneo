
        // JS pour récupérer les partenaires et les afficher dans le select
        fetch("http://localhost:8000/partners")
            .then(response => response.json())
            .then(partners => {
                partners.forEach(partner => {
                    let option = document.createElement("option");
                    option.value = partner.id;
                    option.text = partner.name;
                    document.getElementById("partners").appendChild(option);
                });
            });

        // JS pour envoyer le formulaire
        document.getElementById('partnerForm').addEventListener('submit', function(event) {
            event.preventDefault(); // Empêche l'envoi du formulaire par défaut
          
            // Récupère les données du formulaire
            const file = document.getElementById('file').files[0];
            const partnerId = document.getElementById('partners').value;
          
            // Crée une instance de FormData pour envoyer les données multipart au serveur
            const formData = new FormData();
            formData.append('partner_id', partnerId);
            formData.append('file', file);
          
            // Envoie les données au serveur
            fetch('http://localhost:8000/process_and_insert_file/', {
              method: 'POST',
              body: formData
            })
            .then(response => response.json())
            .then(data => {
              console.log(data);
              alert('Fichier envoyé avec succès !');
            })
            .catch(error => {
              console.error(error);
              alert('Une erreur s\'est produite lors de l\'envoi du fichier.');
            });
          });
          