const form = document.querySelector("form");
form.addEventListener("submit", (event) => {
  const submitButton = document.getElementById("submit_file")
  disableSubmitButton(submitButton)

  const errorSection = document.getElementById("errors")
  errorSection.innerHTML = ""

  const url = new URL(form.action);
  const formData = new FormData(form);

  const fetchOptions = {
    method: form.method,
    body: formData,
  };

  fetch(url, fetchOptions)
    .then((response) => {
      if(!response.ok){
        return Promise.reject(response)
      }
      return response.blob()
    })
    .then((blob) => {
      var url = window.URL.createObjectURL(blob);
      var a = document.createElement('a');
      a.href = url;
      a.download = "nomina.xlsx";
      document.body.appendChild(a);
      a.click();
      a.remove(); 
    })
    .catch((error) => {
      if(error.status != 400){
        errorSection.innerHTML = "Ocurrió un error en el sistema"
      }
      
      errorSection.innerHTML = "<h5>Ocurrieron los siguientes errores al procesar el archivo</h5><ul>"
      error.json().then((bodyError) => {
        bodyError.forEach(error => {
          errorSection.innerHTML += `<li>${error}</li>`
        });
      })
      errorSection.innerHTML += "</ul>"

    }).finally(() => {
      submitButton.removeAttribute("disabled")
      submitButton.innerHTML = "Procesar Archivo"
    });

  form.reset()
  event.preventDefault();
});

const disableSubmitButton = (button, input) => {
  button.setAttribute("disabled", "")
  button.innerHTML = `
    <span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
    Procesando...
  `
}
