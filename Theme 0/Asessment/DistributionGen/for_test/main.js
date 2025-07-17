let distributionData = [];

function generateDistribution() {
  let seed = document.getElementById("seed").value;
  let numStudents = parseInt(document.getElementById("num_students").value);
  let numTickets = parseInt(document.getElementById("num_tickets").value);

  if (
    !seed ||
    isNaN(numStudents) ||
    isNaN(numTickets) ||
    numStudents >= numTickets
  ) {
    alert(
      "Помилка! Введіть коректні дані: seed, кількість слухачів (менше, ніж білетів), кількість білетів."
    );
    return;
  }

  Math.seedrandom(seed); // Встановлення генератора випадкових чисел із seed

  let tickets = Array.from({ length: numTickets }, (_, i) => i + 1);
  let selectedTickets = shuffleArray(tickets).slice(0, numStudents);

  let tableBody = document.querySelector("#distributionTable tbody");
  tableBody.innerHTML = ""; // Очищення таблиці перед генерацією

  distributionData = []; // Очищення попередніх даних

  for (let i = 0; i < numStudents; i++) {
    let row = tableBody.insertRow();
    row.insertCell(0).textContent = `Слухач ${i + 1}`;
    row.insertCell(1).textContent = selectedTickets[i];

    distributionData.push({
      student: `Слухач ${i + 1}`,
      ticket: selectedTickets[i],
    });
  }
}

// Функція перемішування масиву (Fisher-Yates Shuffle)
function shuffleArray(array) {
  for (let i = array.length - 1; i > 0; i--) {
    let j = Math.floor(Math.random() * (i + 1));
    [array[i], array[j]] = [array[j], array[i]];
  }
  return array;
}

// Функція для збереження у JSON
function saveToJSON() {
  if (distributionData.length === 0) {
    alert("Спочатку згенеруйте розподіл!");
    return;
  }

  let jsonData = JSON.stringify({ distribution: distributionData }, null, 4);
  let blob = new Blob([jsonData], { type: "application/json" });
  let link = document.createElement("a");
  link.href = URL.createObjectURL(blob);
  link.download = "distribution.json";
  link.click();
}
