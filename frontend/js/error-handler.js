// Error handler for Eel communication
// Assuming eel is imported elsewhere, e.g., <script src="/eel.js"></script> in the HTML
// Do NOT declare eel variable here

window.onerror = (message, source, lineno, colno, error) => {
  console.error("JavaScript error:", message, "at", source, ":", lineno, ":", colno)

  // Make sure eel exists before trying to use it
  if (typeof window.eel !== "undefined") {
    try {
      // Try both error handlers to ensure at least one works
      if (typeof window.eel.handle_error === "function") {
        window.eel.handle_error(message)
      }
      if (typeof window.eel.patch_handle_error === "function") {
        window.eel.patch_handle_error(message)
      }
    } catch (e) {
      console.error("Failed to report error to Python:", e)
    }
  } else {
    console.error("Eel object not available for error reporting")
  }

  return true // Prevents the default error handling
}

// Add error handling for Eel functions
document.addEventListener("DOMContentLoaded", () => {
  // Assuming eel is imported elsewhere, e.g., <script src="/eel.js"></script> in the HTML
  if (typeof window.eel !== "undefined" && typeof window.eel.expose === "function") {
    var originalExpose = window.eel.expose
    window.eel.expose = (fn, name) => {
      var wrappedFn = function () {
        try {
          return fn.apply(this, arguments)
        } catch (e) {
          console.error("Error in exposed function " + (name || fn.name) + ":", e)
          // Try both error handlers
          if (typeof window.eel.handle_error === "function") {
            window.eel.handle_error("Error in " + (name || fn.name) + ": " + e.message)
          }
          if (typeof window.eel.patch_handle_error === "function") {
            window.eel.patch_handle_error("Error in " + (name || fn.name) + ": " + e.message)
          }
          throw e
        }
      }
      return originalExpose(wrappedFn, name)
    }
  } else {
    console.warn("Eel object not available for function exposure")
  }
})

