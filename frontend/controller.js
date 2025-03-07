// Import eel.js - this line needs to be added to declare eel
import * as eel from "./eel.js"

// Expose functions to be called from Python
function hideLoader() {
  document.getElementById("Loader").hidden = true
  document.getElementById("HelloGreet").hidden = false
}
eel.expose(hideLoader)

function hideStart() {
  document.getElementById("Start").hidden = true
  document.getElementById("Oval").hidden = false
  document.getElementById("SiriWave").hidden = true
}
eel.expose(hideStart)

function senderText(text) {
  document.querySelector(".siri-message").innerHTML = `<li>${text}</li>`
}
eel.expose(senderText)

function ShowHood() {
  document.getElementById("Oval").hidden = false
  document.getElementById("SiriWave").hidden = true
}
eel.expose(ShowHood)

function showFaceAuth() {
  document.getElementById("Loader").hidden = true
  document.getElementById("HelloGreet").hidden = true
  document.getElementById("FaceAuth").hidden = false
}
eel.expose(showFaceAuth)

function showFaceAuthSuccess() {
  document.getElementById("FaceAuth").hidden = true
  document.getElementById("FaceAuthSuccess").hidden = false
}
eel.expose(showFaceAuthSuccess)

function hideFaceAuth() {
  document.getElementById("FaceAuth").hidden = true
  document.getElementById("FaceAuthSuccess").hidden = true
  document.getElementById("HelloGreet").hidden = false
}
eel.expose(hideFaceAuth)

// Add the missing DisplayMessage function
function DisplayMessage(text) {
  document.getElementById("WishMessage").innerText = text
}
eel.expose(DisplayMessage)

