// Fix for Eel communication errors
// No imports - eel is already available globally

// Declare eel variable if it's not already declared.  This is a safeguard.  Ideally, eel should be available globally.
window.eel = window.eel || {}

document.addEventListener("DOMContentLoaded", () => {
  // Patch Eel's _call method to handle error responses properly
  if (window.eel) {
    const originalCall = eel._call

    eel._call = function (name, ...args) {
      try {
        return originalCall.apply(this, [name, ...args])
      } catch (error) {
        console.error(`Error in eel._call for ${name}:`, error)
        return Promise.reject(error)
      }
    }

    // Add global error handler for Eel
    window.addEventListener("error", (event) => {
      console.error("Global error caught:", event.error)
      if (eel.handle_error) {
        try {
          eel.handle_error(event.error.toString())
        } catch (e) {
          console.error("Failed to report error to Python:", e)
        }
      }
      return true // Prevents the default error handling
    })
  }
})

