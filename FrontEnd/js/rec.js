const tableContainer = document.querySelector(".table-container");
const recNum = JSON.parse(localStorage.getItem("rec_number"));
const recStart = JSON.parse(localStorage.getItem("rec_start"));
const recNbr = JSON.parse(localStorage.getItem("rec_nbr"));
const recNbrK = JSON.parse(localStorage.getItem("rec_nbr_kwh"));
const recNbrM= JSON.parse(localStorage.getItem("rec_nbr_montant"));
const recStartK = JSON.parse(localStorage.getItem("rec_start_kwh"));
const recStartM = JSON.parse(localStorage.getItem("rec_start_montant"));
const recNumberK = JSON.parse(localStorage.getItem("rec_number_kwh"));
const recNumberM = JSON.parse(localStorage.getItem("rec_number_montant"));
const transactions = JSON.parse(localStorage.getItem("total"));

tableContainer.innerHTML = `
<table class="table table-bordered">
<thead>
    <tr>
        <th></th>
        <th>Nombre de transactions</th>
        <th>KWH</th>
        <th>Montant(FCFA)</th>


    </tr>
</thead>
<tbody>
    <tr>
        <td>Transactions total</td>
        <td id="total-transactions">${recStart.start}</td>
        <td >${recStartK.start_kwh}</td>
        <td >${recStartM.start_montant}</td>

    </tr>
    <tr>
        <td>Transactions Réconciliées</td>
        <td>${recNbr.nbr}</td>
        <td>${recNbrK.nbr_kwh}</td>
        <td>${recNbrM.nbr_montant}</td>
    </tr>
    <tr>
        <td>Transactions Non Réconciliées</td>
        <td >${recNum.number}</td>        
        <td >${recNumberK.number_kwh}</td>
        <td>${recNumberM.number_montant}</td>
    </tr>
    <!-- Ajouter plus de lignes si nécessaire -->
</tbody>
</table>
`




