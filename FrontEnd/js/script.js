
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
const form = document.getElementById('rec_token_form');
const responseDiv = document.getElementById('response');
 

form.addEventListener('submit', async (event) => {
  event.preventDefault();

  const formData = new FormData(form);

  try {
    const response = await fetch('http://localhost:8000/rec_token', {
      method: 'POST',
      body: formData,
    });

    if (!response.ok) {
      throw new Error(`Error: ${response.statusText}`);
    }

    const data = await response.json();
    responseDiv.textContent = `Number of elements: ${data[0]}`; // Access the first element (number)
    responseDiv.innerHTML += `<br>Data List:`;
    responseDiv.innerHTML += `<ul>`;
    for (const item of data[1]) {
      // Assuming data[1] is a list of objects
      responseDiv.innerHTML += `<li>${item.name} (other properties)</li>`; // Access properties of each item
    }
    responseDiv.innerHTML += `</ul>`;
  } catch (error) {
    console.error('Error:', error);
    responseDiv.textContent = `Error: ${error.message}`;
  }
});