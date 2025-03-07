// Main JavaScript file - NO IMPORTS

document.addEventListener("DOMContentLoaded", () => {
  console.log("DOM loaded, initializing main.js")

  // Initialize eel if available
  if (typeof window.eel !== "undefined" && window.eel.init) {
    window.eel.init()
    console.log("Eel initialized")
  } else {
    console.warn("Eel not available or init method missing")
  }

  // Set up event listeners
  setupEventListeners()

  // Initialize UI components if libraries are available
  initializeUI()
})

// Function to set up event listeners
function setupEventListeners() {
  // Mic button click handler
  var micBtn = document.getElementById("MicBtn")
  if (micBtn) {
    micBtn.addEventListener("click", () => {
      if (typeof window.eel !== "undefined") {
        window.eel.play_assistant_sound()
        document.getElementById("Oval").hidden = true
        document.getElementById("SiriWave").hidden = false
        window.eel.takeAllCommands()
      }
    })
    console.log("Mic button event listener added")
  }

  // Key press handler for keyboard shortcut
  document.addEventListener("keyup", (e) => {
    if (e.key === "j" && e.metaKey) {
      if (typeof window.eel !== "undefined") {
        window.eel.play_assistant_sound()
        document.getElementById("Oval").hidden = true
        document.getElementById("SiriWave").hidden = false
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
  }

  // Send button handler
  var sendBtn = document.getElementById("SendBtn")
  if (sendBtn) {
    sendBtn.addEventListener("click", () => {
      var message = document.getElementById("chatbox").value
      playAssistant(message)
    })
  }
}

// Function to initialize UI components
function initializeUI() {
  // Initialize textillate if jQuery and textillate are available
  if (typeof window.jQuery !== "undefined" && typeof window.jQuery.fn.textillate !== "undefined") {
    window.jQuery(".text").textillate({
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

    window.jQuery(".siri-message").textillate({
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
    var siriWave = new window.SiriWave({
      container: document.getElementById("siri-container"),
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
    console.warn("SiriWave not available")
  }
}

// Function to show/hide buttons based on input
function showHideButton(message) {
  if (message.length === 0) {
    document.getElementById("MicBtn").hidden = false
    document.getElementById("SendBtn").hidden = true
  } else {
    document.getElementById("MicBtn").hidden = true
    document.getElementById("SendBtn").hidden = false
  }
}

// Function to play assistant with message
function playAssistant(message) {
  if (message !== "") {
    document.getElementById("Oval").hidden = true
    document.getElementById("SiriWave").hidden = false
    if (typeof window.eel !== "undefined") {
      window.eel.takeAllCommands(message)
    }
    document.getElementById("chatbox").value = ""
    document.getElementById("MicBtn").hidden = false
    document.getElementById("SendBtn").hidden = true
  } else {
    console.log("Empty message, nothing sent.")
  }
}

