// ডিফল্ট কনভার্টার: Document
let currentConverter = "document";

// কনভার্টার সুইচার
function switchConverter(type) {
  currentConverter = type;
  const form = document.getElementById("convertForm");
  form.action = `/convert/${type}`;

  // বাটন হাইলাইট
  document.querySelectorAll(".converter-buttons button").forEach(btn => {
    btn.classList.remove("active");
  });
  document.querySelector(`.converter-buttons button[onclick*="${type}"]`).classList.add("active");
}

// লোডিং শো এবং ফর্ম সাবমিট
document.getElementById("convertForm").addEventListener("submit", function (e) {
  document.getElementById("loading").classList.remove("hidden");
});

// সোর্স নির্বাচন অনুযায়ী ইনপুট চেঞ্জ
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
