// No imports - using global variables only

// Expose functions to be called from Python
function hideLoader() {
  const loader = document.getElementById("Loader")
  const helloGreet = document.getElementById("HelloGreet")

  if (loader) loader.hidden = true
  if (helloGreet) helloGreet.hidden = false
}

function hideStart() {
  const start = document.getElementById("Start")
  const oval = document.getElementById("Oval")
  const siriWave = document.getElementById("SiriWave")

  if (start) start.hidden = true
  if (oval) oval.hidden = false
  if (siriWave) siriWave.hidden = true
}

function senderText(text) {
  const siriMessage = document.querySelector(".siri-message")
  if (siriMessage) siriMessage.innerHTML = `<li>${text}</li>`
}

function ShowHood() {
  const oval = document.getElementById("Oval")
  const siriWave = document.getElementById("SiriWave")

  if (oval) oval.hidden = false
  if (siriWave) siriWave.hidden = true
}

function showFaceAuth() {
  const loader = document.getElementById("Loader")
  const helloGreet = document.getElementById("HelloGreet")
  const faceAuth = document.getElementById("FaceAuth")

  if (loader) loader.hidden = true
  if (helloGreet) helloGreet.hidden = true
  if (faceAuth) faceAuth.hidden = false
}

function showFaceAuthSuccess() {
  const faceAuth = document.getElementById("FaceAuth")
  const faceAuthSuccess = document.getElementById("FaceAuthSuccess")

  if (faceAuth) faceAuth.hidden = true
  if (faceAuthSuccess) faceAuthSuccess.hidden = false
}

function hideFaceAuth() {
  const faceAuth = document.getElementById("FaceAuth")
  const faceAuthSuccess = document.getElementById("FaceAuthSuccess")
  const helloGreet = document.getElementById("HelloGreet")

  if (faceAuth) faceAuth.hidden = true
  if (faceAuthSuccess) faceAuthSuccess.hidden = true
  if (helloGreet) helloGreet.hidden = false
}

// Add the missing DisplayMessage function
function DisplayMessage(text) {
  const wishMessage = document.getElementById("WishMessage")
  if (wishMessage) wishMessage.innerText = text
}

// Expose all functions to eel when the document is loaded
document.addEventListener("DOMContentLoaded", () => {
  // Do NOT redeclare eel here
  if (typeof window.eel !== "undefined") {
    window.eel.expose(hideLoader, "hideLoader")
    window.eel.expose(hideStart, "hideStart")
    window.eel.expose(senderText, "senderText")
    window.eel.expose(ShowHood, "ShowHood")
    window.eel.expose(showFaceAuth, "showFaceAuth")
    window.eel.expose(showFaceAuthSuccess, "showFaceAuthSuccess")
    window.eel.expose(hideFaceAuth, "hideFaceAuth")
    window.eel.expose(DisplayMessage, "DisplayMessage")

    console.log("Controller functions exposed to eel")
  } else {
    console.warn("Eel object not available for function exposure")
  }
})

