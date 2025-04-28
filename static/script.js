const videoFeed = document.getElementById("video-feed");
const canvas = document.getElementById("canvas");
const captureButton = document.getElementById("capture");
const uploadForm = document.getElementById("upload-form");
const loader = document.getElementById("loader");
const fileInput = document.getElementById("file");
const capturePreview = document.getElementById("capture-preview");
const capturedImage = document.getElementById("captured-image");

// 📸 Capturar foto desde el video feed
captureButton.addEventListener("click", () => {
  const nameInput = document.getElementById("name");

  if (!nameInput.value.trim()) {
    alert("Por favor ingresa un nombre antes de capturar.");
    return;
  }

  const context = canvas.getContext("2d");
  canvas.width = videoFeed.width;
  canvas.height = videoFeed.height;
  context.drawImage(videoFeed, 0, 0, canvas.width, canvas.height);

  canvas.toBlob((blob) => {
    const file = new File([blob], "captura.png", { type: "image/png" });

    const dataTransfer = new DataTransfer();
    dataTransfer.items.add(file);

    fileInput.files = dataTransfer.files; // Cargar captura en el input "file"

    // Mostrar miniatura de la captura
    const url = URL.createObjectURL(blob);
    capturedImage.src = url;
    capturePreview.style.display = "block";

    alert(
      '✅ Foto capturada correctamente. Ahora presiona "Registrar Nueva Cara".'
    );
  }, "image/png");
});

// 🛡️ Validar formulario antes de enviar
uploadForm.addEventListener("submit", (e) => {
  if (fileInput.files.length === 0 || !fileInput.files[0]) {
    e.preventDefault(); // Cancelar envío
    alert(
      "⚠️ Debes capturar una foto o seleccionar una imagen antes de registrar."
    );
    loader.style.display = "none";
    return;
  }

  loader.style.display = "block"; // Mostrar loader al enviar
});
