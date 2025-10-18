document.getElementById("analyzeBtn").addEventListener("click", async () => {
  const tweet = document.getElementById("tweetInput").value.trim();
  if (!tweet) return alert("Please enter a tweet!");

  const res = await fetch("main.py", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ tweet }),
  });

  const data = await res.json();
  const result = document.getElementById("result");
  const scoreBar = document.getElementById("scoreBar");
  const scoreValue = document.getElementById("scoreValue");
  const toneValue = document.getElementById("toneValue");
  const reasonsList = document.getElementById("reasonsList");
  const suggestionsList = document.getElementById("suggestionsList");

  result.classList.remove("hidden");

  const scorePercent = (data.score + 100) / 2; // convert -100–100 → 0–100
  scoreBar.style.width = `${scorePercent}%`;
  scoreBar.className = "h-4 transition-all duration-700 rounded-lg " + 
    (data.score > 60 ? "bg-green-400" : data.score > 30 ? "bg-yellow-400" : "bg-red-400");

  scoreValue.textContent = `Score: ${data.score}/100`;
  toneValue.textContent = `Sentiment: ${data.tone} (${data.sentiment})`;

  reasonsList.innerHTML = "";
  data.reasons.forEach(r => {
    const li = document.createElement("li");
    li.textContent = r;
    reasonsList.appendChild(li);
  });

  suggestionsList.innerHTML = "";
  data.suggestions.forEach(s => {
    const li = document.createElement("li");
    li.textContent = s;
    suggestionsList.appendChild(li);
  });
});


