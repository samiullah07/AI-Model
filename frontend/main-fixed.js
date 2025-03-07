// Import necessary libraries (assuming they are available via a module system or globally defined)
// For example, if using a module bundler like Webpack or Parcel:
// import eel from './eel'; // Adjust path as needed
// import $ from 'jquery'; // Adjust path as needed
// import SiriWave from 'siriwave'; // Adjust path as needed

// Or if using global variables:
// Assuming eel, $, and SiriWave are defined globally.  If not, you'll need to include the relevant script tags in your HTML.

document.addEventListener("DOMContentLoaded", () => {
  // Initialize eel
  if (typeof eel !== "undefined" && eel.init) {
    eel.init()
  }

  // Initialize textillate if jQuery and textillate are available
  if (typeof $ !== "undefined" && $.fn.textillate) {
    $(".text").textillate({
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

    $(".siri-message").textillate({
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
  }

  // Initialize SiriWave if available
  if (typeof SiriWave !== "undefined") {
    var siriWave = new SiriWave({
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
  }

  // Set up event listeners
  var micBtn = document.getElementById("MicBtn")
  if (micBtn) {
    micBtn.addEventListener("click", () => {
      if (typeof eel !== "undefined") {
        eel.play_assistant_sound()
        document.getElementById("Oval").hidden = true
        document.getElementById("SiriWave").hidden = false
        eel.takeAllCommands()
      }
    })
  }

  // Key press handler
  function doc_keyUp(e) {
    if (e.key === "j" && e.metaKey) {
      if (typeof eel !== "undefined") {
        eel.play_assistant_sound()
        document.getElementById("Oval").hidden = true
        document.getElementById("SiriWave").hidden = false
        eel.takeAllCommands()
      }
    }
  }
  document.addEventListener("keyup", doc_keyUp, false)

  // Play assistant function
  function PlayAssistant(message) {
    if (message !== "") {
      document.getElementById("Oval").hidden = true
      document.getElementById("SiriWave").hidden = false
      if (typeof eel !== "undefined") {
        eel.takeAllCommands(message)
      }
      document.getElementById("chatbox").value = ""
      document.getElementById("MicBtn").hidden = false
      document.getElementById("SendBtn").hidden = true
    } else {
      console.log("Empty message, nothing sent.")
    }
  }

  // Show/hide button function
  function ShowHideButton(message) {
    if (message.length === 0) {
      document.getElementById("MicBtn").hidden = false
      document.getElementById("SendBtn").hidden = true
    } else {
      document.getElementById("MicBtn").hidden = true
      document.getElementById("SendBtn").hidden = false
    }
  }

  // Chatbox input handler
  var chatbox = document.getElementById("chatbox")
  if (chatbox) {
    chatbox.addEventListener("keyup", () => {
      var message = chatbox.value
      console.log("Current chatbox input: ", message)
      ShowHideButton(message)
    })

    chatbox.addEventListener("keypress", (e) => {
      if (e.key === "Enter" || e.keyCode === 13) {
        var message = chatbox.value
        PlayAssistant(message)
      }
    })
  }

  // Send button handler
  var sendBtn = document.getElementById("SendBtn")
  if (sendBtn) {
    sendBtn.addEventListener("click", () => {
      var message = document.getElementById("chatbox").value
      PlayAssistant(message)
    })
  }
})

