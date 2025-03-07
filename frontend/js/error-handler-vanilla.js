// Error handler for Eel communication - no imports
// Declare eel variable.  This assumes eel.js is included in the HTML.  If not, adjust accordingly.
let eel
try {
  eel = window.eel
} catch (e) {
  console.error("Eel not found.  Ensure eel.js is included in your HTML.")
}

window.onerror = (message, source, lineno, colno, error) => {
  console.error("JavaScript error:", message, "at", source, ":", lineno, ":", colno)
  if (eel) {
    try {
      // Try both error handlers to ensure at least one works
      if (eel.handle_error) {
        eel.handle_error(message)
      }
      if (eel.patch_handle_error) {
        eel.patch_handle_error(message)
      }
    } catch (e) {
      console.error("Failed to report error to Python:", e)
    }
  }
  return true // Prevents the default error handling
}

// Add error handling for Eel functions
document.addEventListener("DOMContentLoaded", () => {
  // Assuming eel is imported elsewhere, e.g., <script src="/eel.js"></script> in the HTML
  if (eel && eel.expose) {
    var originalExpose = eel.expose
    eel.expose = (fn, name) => {
      var wrappedFn = function () {
        try {
          return fn.apply(this, arguments)
        } catch (e) {
          console.error("Error in exposed function " + (name || fn.name) + ":", e)
          // Try both error handlers
          if (eel.handle_error) {
            eel.handle_error("Error in " + (name || fn.name) + ": " + e.message)
          }
          if (eel.patch_handle_error) {
            eel.patch_handle_error("Error in " + (name || fn.name) + ": " + e.message)
          }
          throw e
        }
      }
      return originalExpose(wrappedFn, name)
    }
  }
})

