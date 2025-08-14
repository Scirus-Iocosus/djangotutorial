let x1, r, v, g, b, redscore, greenscore, yellowscore, bluescore;

// Recupera i punteggi principali
fetch('/api/punteggi/')
.then(response => response.json())
.then(data => {
    let punteggi = data.punteggi;

    // Ordinare i punteggi in ordine crescente
    x1 = punteggi[3]?.punteggio || 1;

    return Promise.all([
    fetch('/api/punteggi-rossi/').then(res => res.json()),
    fetch('/api/punteggi-verdi/').then(res => res.json()),
    fetch('/api/punteggi-gialli/').then(res => res.json()),
    fetch('/api/punteggi-blu/').then(res => res.json()),
    ]);
})
.then(([redData, greenData, yellowData, blueData]) => {
    // Assegniamo i punteggi
    redscore = redData.somma_punteggi;
    greenscore = greenData.somma_punteggi;
    yellowscore = yellowData.somma_punteggi;
    bluescore = blueData.somma_punteggi;

    // Calcoliamo le percentuali
    r = (redscore / x1) * 100;
    v = (greenscore / x1) * 100;
    g = (yellowscore / x1) * 100;
    b = (bluescore / x1) * 100;

    // Creiamo un array con i div e i valori
    let teams = [
    { id: "Rossi", valore: r, punteggio: redscore },
    { id: "Verdi", valore: v, punteggio: greenscore },
    { id: "Gialli", valore: g, punteggio: yellowscore },
    { id: "Blu", valore: b, punteggio: bluescore }
    ];

    // Ordiniamo i team in ordine decrescente
    teams.sort((a, b) => b.valore - a.valore);

//    console.log("Percentuali ordinate:", teams);

    // Assegniamo un valore di `order` per controllare la posizione con CSS
    teams.forEach((team, index) => {
    let div = document.getElementById(team.id);
    div.style.order = index; // Assegna un valore crescente di `order`
    div.querySelector("p span").textContent = team.punteggio;
    div.querySelector("line").setAttribute("x2", team.valore + "%");
    });
    let primo = teams[0].id;
    let secondo = teams[1].id;
    let terzo = teams[2].id;
    let quarto = teams[3].id;

    let primo1 = teams[0].punteggio;
    let secondo1 = teams[1].punteggio;
    let terzo1 = teams[2].punteggio;
    let quarto1 = teams[3].punteggio;
    
    console.log(primo+'-'+primo1, secondo, terzo, quarto);

    document.getElementById("first").innerHTML = "1 - " + primo;
    document.getElementById("second").innerHTML = "2 - " + secondo;
    document.getElementById("third").innerHTML = "3 - " + terzo;
    document.getElementById("fourth").innerHTML = "4 - " + quarto;

    document.getElementsByClassName("primo1")[0].innerHTML = "Punteggio - " + primo1;
    document.getElementsByClassName("secondo1")[0].innerHTML = "Punteggio - " + secondo1;
    document.getElementsByClassName("terzo1")[0].innerHTML = "Punteggio - " + terzo1;
    document.getElementsByClassName("quarto1")[0].innerHTML = "Punteggio - " + quarto1;

})
.catch(error => console.error('Errore nel recupero dati:', error));
