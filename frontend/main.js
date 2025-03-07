// Import necessary libraries
import $ from "jquery"
import eel from "eel"
import SiriWave from "siriwave"

$(document).ready(() => {
  eel.init()()
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

  $("#MicBtn").click(() => {
    eel.play_assistant_sound()
    $("#Oval").attr("hidden", true)
    $("#SiriWave").attr("hidden", false)

    eel.takeAllCommands()()
  })

  function doc_keyUp(e) {
    // this would test for whichever key is 40 (down arrow) and the ctrl key at the same time

    if (e.key === "j" && e.metaKey) {
      eel.play_assistant_sound()
      $("#Oval").attr("hidden", true)
      $("#SiriWave").attr("hidden", false)
      eel.takeAllCommands()()
    }
  }
  document.addEventListener("keyup", doc_keyUp, false)

  function PlayAssistant(message) {
    if (message != "") {
      $("#Oval").attr("hidden", true)
      $("#SiriWave").attr("hidden", false)
      eel.takeAllCommands(message)
      $("#chatbox").val("")
      $("#MicBtn").attr("hidden", false)
      $("#SendBtn").attr("hidden", true)
    } else {
      console.log("Empty message, nothing sent.") // Log if the message is empty
    }
  }

  function ShowHideButton(message) {
    if (message.length == 0) {
      $("#MicBtn").attr("hidden", false)
      $("#SendBtn").attr("hidden", true)
    } else {
      $("#MicBtn").attr("hidden", true)
      $("#SendBtn").attr("hidden", false)
    }
  }

  $("#chatbox").keyup(() => {
    const message = $("#chatbox").val()
    console.log("Current chatbox input: ", message) // Log input value for debugging
    ShowHideButton(message)
  })

  $("#SendBtn").click(() => {
    const message = $("#chatbox").val()
    PlayAssistant(message)
  })

  $("#chatbox").keypress((e) => {
    const key = e.which // Declare key here
    if (key == 13) {
      const message = $("#chatbox").val()
      PlayAssistant(message)
    }
  })
})

