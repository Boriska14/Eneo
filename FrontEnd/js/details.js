
const tableContainer = document.querySelector(".table-container");
const date = JSON.parse(localStorage.getItem("date")).date;
const partner = JSON.parse(localStorage.getItem("partner_name")).partner;

if(!date || !partner) {
  window.location.href = "./date.html";
}

let content = "";

fetch(`http://localhost:8000/details?date=${date}&partner=${partner}`, {
  method: 'GET',
  headers: {
    'Content-Type': 'application/json'
  }
})
.then(response => response.json())
.then(data => {
  // Display the objects in the list
  const detailsList = document.getElementById('details-list');
  data.forEach(transaction => {
    content += 
    ` <tr>
        <td>${transaction.pos}</td>
        <td>${transaction.token}</td>
        <td>${transaction.montant}</td>
        <td>${transaction.kwh}</td>
        <td>${transaction.date}</td>
        <td>${transaction.meter_no}</td>
      </tr>
    ` 
  });

  tableContainer.innerHTML = `
<table class="table table-bordered">
<thead>
    <tr>
        <th>POS</th>
        <th>TOKEN</th>
        <th>MONTANT</th>
        <th>KWH</th>
        <th>DATE</th>
        <th>METER_NO</th>
    </tr>
</thead>
<tbody>
    ${content}
</tbody>
</table>
`
})
.catch(error => console.error('Error fetching data:', error));

