// Global controller functions - NO IMPORTS

// Function to hide loader and show greeting
function hideLoader() {
  document.getElementById("Loader").hidden = true
  document.getElementById("HelloGreet").hidden = false
}

// Function to hide start screen and show main interface
function hideStart() {
  document.getElementById("Start").hidden = true
  document.getElementById("Oval").hidden = false
  document.getElementById("SiriWave").hidden = true
}

// Function to update sender text
function senderText(text) {
  document.querySelector(".siri-message").innerHTML = `<li>${text}</li>`
}

// Function to show the main interface
function ShowHood() {
  document.getElementById("Oval").hidden = false
  document.getElementById("SiriWave").hidden = true
}

// Function to show face authentication UI
function showFaceAuth() {
  document.getElementById("Loader").hidden = true
  document.getElementById("HelloGreet").hidden = true
  document.getElementById("FaceAuth").hidden = false
}

// Function to show face authentication success UI
function showFaceAuthSuccess() {
  document.getElementById("FaceAuth").hidden = true
  document.getElementById("FaceAuthSuccess").hidden = false
}

// Function to hide face authentication UI
function hideFaceAuth() {
  document.getElementById("FaceAuth").hidden = true
  document.getElementById("FaceAuthSuccess").hidden = true
  document.getElementById("HelloGreet").hidden = false
}

// Function to display message
function DisplayMessage(text) {
  document.getElementById("WishMessage").innerText = text
}

// Wait for eel to be available, then expose functions
document.addEventListener("DOMContentLoaded", () => {
  // Check if eel is available
  if (typeof window.eel !== "undefined") {
    // Expose functions to Python
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
    console.error("Eel not available. Functions not exposed.")
  }
})

