
fetch("http://localhost:8000/partners")
            .then(response => response.json())
            .then(partners => {
                partners.forEach(partner => {
                    let option = document.createElement("option");
                    option.value = partner.name;
                    option.text = partner.name;
                    document.getElementById("partners").appendChild(option);
                });
 });
const form = document.getElementById('rec_token_form');
const dateInput = document.getElementById('date');
const partnerSelect = document.getElementById('partners');
const responseDiv = document.getElementById('response');

localStorage.setItem("rec_data", JSON.stringify({hello: "world"}));

form.addEventListener('submit', async (event) => {
  event.preventDefault();
  const formData = new FormData();
  const date = dateInput.value;
  const partner = partnerSelect.value;
  formData.append('date', date);
  formData.append('partner_name', partner);
  localStorage.setItem("date", JSON.stringify({date}));
  localStorage.setItem("partner_name", JSON.stringify({partner}));



  try {
    const response = await fetch("http://localhost:8000/rec_token", {
      method: 'POST',
      body: formData 
    });

    if (!response.ok) {
      throw new Error(`Error: ${response.statusText}`);
    }
    const data = await response.json();
    const start = data[0];
    const start_montant=data[1]
    const start_kwh=data[2]
    let nbr;
    let nbr_montant;
    let nbr_kwh;
    const number= data[6];
    const number_montant= data[7];
    const number_kwh= data[8];
    const transactions = data[9];
    if (nbr === null) {
      nbr="element not found"// L'élément est null
    } else {
      nbr=data[3]// L'élément n'est pas null
    }
    if (nbr_montant === null) {
      nbr_montant="element not found"// L'élément est null
    } else {
      nbr_montant=data[4]// L'élément n'est pas null
    }
    if (nbr_kwh === null) {
      nbr_kwh="element not found"// L'élément est null
    } else {
      nbr_kwh=data[5]// L'élément n'est pas null
    }
    localStorage.setItem("rec_start", JSON.stringify({start}));
    localStorage.setItem("rec_start_montant", JSON.stringify({start_montant}));
    localStorage.setItem("rec_start_kwh", JSON.stringify({start_kwh}));
    localStorage.setItem("rec_nbr", JSON.stringify({nbr}));
    localStorage.setItem("rec_nbr_montant", JSON.stringify({nbr_montant}));
    localStorage.setItem("rec_nbr_kwh", JSON.stringify({nbr_kwh}));
    localStorage.setItem("rec_number", JSON.stringify({number}));
    localStorage.setItem("rec_number_montant", JSON.stringify({number_montant}));
    localStorage.setItem("rec_number_kwh", JSON.stringify({number_kwh}));
    localStorage.setItem("total", JSON.stringify({transactions}));
    window.location.href = "./dashboard.html"
  } catch (error) {
    console.error('Error:', error);
    responseDiv.textContent = `Error: ${error.message}`;
  }
});