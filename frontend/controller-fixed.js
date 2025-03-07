// No imports - using global variables only

// Expose functions to be called from Python
function hideLoader() {
  document.getElementById("Loader").hidden = true
  document.getElementById("HelloGreet").hidden = false
}

function hideStart() {
  document.getElementById("Start").hidden = true
  document.getElementById("Oval").hidden = false
  document.getElementById("SiriWave").hidden = true
}

function senderText(text) {
  document.querySelector(".siri-message").innerHTML = `<li>${text}</li>`
}

function ShowHood() {
  document.getElementById("Oval").hidden = false
  document.getElementById("SiriWave").hidden = true
}

function showFaceAuth() {
  document.getElementById("Loader").hidden = true
  document.getElementById("HelloGreet").hidden = true
  document.getElementById("FaceAuth").hidden = false
}

function showFaceAuthSuccess() {
  document.getElementById("FaceAuth").hidden = true
  document.getElementById("FaceAuthSuccess").hidden = false
}

function hideFaceAuth() {
  document.getElementById("FaceAuth").hidden = true
  document.getElementById("FaceAuthSuccess").hidden = true
  document.getElementById("HelloGreet").hidden = false
}

// Add the missing DisplayMessage function
function DisplayMessage(text) {
  document.getElementById("WishMessage").innerText = text
}

// Expose all functions to eel
// Declare eel variable if it's not already declared.  This is a common pattern in browser environments where eel might be defined by an external script.
let eel
try {
  eel = eel || window.eel // Check if eel is already defined globally
} catch (error) {
  console.error("eel variable not found.  Ensure your eel.js is included correctly.")
}

if (typeof eel !== "undefined") {
  eel.expose(hideLoader, "hideLoader")
  eel.expose(hideStart, "hideStart")
  eel.expose(senderText, "senderText")
  eel.expose(ShowHood, "ShowHood")
  eel.expose(showFaceAuth, "showFaceAuth")
  eel.expose(showFaceAuthSuccess, "showFaceAuthSuccess")
  eel.expose(hideFaceAuth, "hideFaceAuth")
  eel.expose(DisplayMessage, "DisplayMessage")
}

