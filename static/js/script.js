document.addEventListener("DOMContentLoaded", function () {
  const form = document.getElementById("convertForm");
  const outputSelect = document.getElementById("outputFormatSelect");
  const converterButtons = document.querySelectorAll(".converter-buttons button");

  const converterOptions = {
      document: ["pdf", "docx", "txt", "pptx"],
      image: ["jpg", "png", "webp"],
      video: ["mp4", "avi", "mov"],
      audio: ["mp3", "wav", "ogg"]
  };

  // Function to switch converter and update UI
  function switchConverter(type) {
      // Remove 'active' class from all buttons
      converterButtons.forEach(btn => btn.classList.remove("active"));
      
      // Add 'active' class to the clicked button
      document.querySelector(`[data-converter="${type}"]`).classList.add("active");

      // Update form action and output options
      form.action = `/convert/${type}`;
      outputSelect.innerHTML = "";
      
      converterOptions[type].forEach(format => {
          const option = document.createElement("option");
          option.value = format;
          option.textContent = format.toUpperCase();
          outputSelect.appendChild(option);
      });
  }

  // Set default converter on page load
  switchConverter('document');

  // Attach event listeners to buttons
  converterButtons.forEach(button => {
    button.addEventListener("click", (e) => {
      const type = button.getAttribute("data-converter");
      switchConverter(type);
    });
  });

  // Handle form submission and show loading indicator
  form.addEventListener("submit", function () {
      document.getElementById("loading").classList.remove("hidden");
  });

  // Handle source selection changes
  document.getElementById("source").addEventListener("change", function () {
    const source = this.value;
    const fileInput = document.getElementById("fileInput");

    if (source === "url") {
      const newInput = document.createElement("input");
      newInput.type = "text";
      newInput.name = "file_url";
      newInput.id = "fileInput";
      newInput.placeholder = "Paste file URL here";
      fileInput.replaceWith(newInput);
    } else {
      const newInput = document.createElement("input");
      newInput.type = "file";
      newInput.name = "file";
      newInput.id = "fileInput";
      newInput.required = true;
      fileInput.replaceWith(newInput);
    }
  });
});