function processText() {
  const text = document.getElementById("input").value;
  const processed = text.toUpperCase(); // Your processing here
  const wordCount = text.trim().split(/\s+/).filter(w => w).length;

  document.getElementById("output").innerText = processed;
  document.getElementById("wordCount").innerText = wordCount;
}
