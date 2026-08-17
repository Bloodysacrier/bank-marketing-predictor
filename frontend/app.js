const form = document.getElementById("prediction-form");
const resultBox = document.getElementById("result");
const errorBox = document.getElementById("error");

form.addEventListener("submit", async function (event) {
    event.preventDefault();

    const clientData = {
        age: Number(document.getElementById("age").value),
        job: document.getElementById("job").value,
        marital: document.getElementById("marital").value,
        education: document.getElementById("education").value,
        balance: Number(document.getElementById("balance").value),
        housing: document.getElementById("housing").value,
        loan: document.getElementById("loan").value,
        campaign: Number(document.getElementById("campaign").value)
    };

    try {
        const response = await fetch("/predict", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(clientData)
        });

        if (!response.ok) {
            throw new Error("Datos inválidos");
        }

        const data = await response.json();
        document.getElementById("probability").textContent =
            (data.probability * 100).toFixed(1) + "%";
        document.getElementById("prediction").textContent = data.prediction;
        document.getElementById("classification").textContent = data.classification;

        resultBox.style.display = "block";
        errorBox.style.display = "none";
    } catch (error) {
        resultBox.style.display = "none";
        errorBox.style.display = "block";
    }
});

