// No imports - using global variables only
// Do NOT redeclare eel, $, or SiriWave here

// Declare jQuery variable
const jQuery = window.$

document.addEventListener("DOMContentLoaded", () => {
  console.log("DOM loaded, initializing main.js")

  // Initialize eel if available
  if (typeof window.eel !== "undefined" && window.eel.init) {
    window.eel.init()
    console.log("Eel initialized")
  } else {
    console.warn("Eel not available or init method missing")
  }

  // Initialize textillate if jQuery and textillate are available
  if (typeof jQuery !== "undefined" && jQuery.fn && jQuery.fn.textillate) {
    jQuery(".text").textillate({
      loop: true,
      speed: 1500,
      sync: true,
      in: {
        effect: "bounceIn",
      },
      out: {
        effect: "bounceOut",
      },
    })

    jQuery(".siri-message").textillate({
      loop: true,
      sync: true,
      in: {
        effect: "fadeInUp",
        sync: true,
      },
      out: {
        effect: "fadeOutUp",
        sync: true,
      },
    })
    console.log("Textillate initialized")
  } else {
    console.warn("jQuery or textillate not available")
  }

  // Initialize SiriWave if available
  if (typeof window.SiriWave !== "undefined") {
    const siriContainer = document.getElementById("siri-container")
    if (siriContainer) {
      var siriWave = new window.SiriWave({
        container: siriContainer,
        width: 940,
        style: "ios9",
        amplitude: "1",
        speed: "0.30",
        height: 200,
        autostart: true,
        waveColor: "#ff0000",
        waveOffset: 0,
        rippleEffect: true,
        rippleColor: "#ffffff",
      })
      console.log("SiriWave initialized")
    } else {
      console.warn("SiriWave container not found")
    }
  } else {
    console.warn("SiriWave not available")
  }

  // Set up event listeners
  setupEventListeners()
})

// Function to set up event listeners
function setupEventListeners() {
  // Mic button click handler
  var micBtn = document.getElementById("MicBtn")
  if (micBtn) {
    micBtn.addEventListener("click", () => {
      if (typeof window.eel !== "undefined") {
        window.eel.play_assistant_sound()
        const oval = document.getElementById("Oval")
        const siriWave = document.getElementById("SiriWave")
        if (oval) oval.hidden = true
        if (siriWave) siriWave.hidden = false
        window.eel.takeAllCommands()
      }
    })
    console.log("Mic button event listener added")
  } else {
    console.warn("Mic button not found")
  }

  // Key press handler for keyboard shortcut
  document.addEventListener("keyup", (e) => {
    if (e.key === "j" && e.metaKey) {
      if (typeof window.eel !== "undefined") {
        window.eel.play_assistant_sound()
        const oval = document.getElementById("Oval")
        const siriWave = document.getElementById("SiriWave")
        if (oval) oval.hidden = true
        if (siriWave) siriWave.hidden = false
        window.eel.takeAllCommands()
      }
    }
  })

  // Chatbox input handler
  var chatbox = document.getElementById("chatbox")
  if (chatbox) {
    chatbox.addEventListener("keyup", () => {
      var message = chatbox.value
      console.log("Current chatbox input: ", message)
      showHideButton(message)
    })

    chatbox.addEventListener("keypress", (e) => {
      if (e.key === "Enter" || e.keyCode === 13) {
        var message = chatbox.value
        playAssistant(message)
      }
    })
    console.log("Chatbox event listeners added")
  } else {
    console.warn("Chatbox not found")
  }

  // Send button handler
  var sendBtn = document.getElementById("SendBtn")
  if (sendBtn) {
    sendBtn.addEventListener("click", () => {
      var chatbox = document.getElementById("chatbox")
      if (chatbox) {
        var message = chatbox.value
        playAssistant(message)
      }
    })
    console.log("Send button event listener added")
  } else {
    console.warn("Send button not found")
  }
}

// Function to show/hide buttons based on input
function showHideButton(message) {
  const micBtn = document.getElementById("MicBtn")
  const sendBtn = document.getElementById("SendBtn")

  if (!micBtn || !sendBtn) return

  if (message.length === 0) {
    micBtn.hidden = false
    sendBtn.hidden = true
  } else {
    micBtn.hidden = true
    sendBtn.hidden = false
  }
}

// Function to play assistant with message
function playAssistant(message) {
  if (message !== "") {
    const oval = document.getElementById("Oval")
    const siriWave = document.getElementById("SiriWave")
    const chatbox = document.getElementById("chatbox")
    const micBtn = document.getElementById("MicBtn")
    const sendBtn = document.getElementById("SendBtn")

    if (oval) oval.hidden = true
    if (siriWave) siriWave.hidden = false

    if (typeof window.eel !== "undefined") {
      window.eel.takeAllCommands(message)
    }

    if (chatbox) chatbox.value = ""
    if (micBtn) micBtn.hidden = false
    if (sendBtn) sendBtn.hidden = true
  } else {
    console.log("Empty message, nothing sent.")
  }
}

