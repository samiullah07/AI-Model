// Simple error handler for Eel communication - NO IMPORTS

// Global error handler
window.onerror = (message, source, lineno, colno, error) => {
  console.error("JavaScript error:", message, "at", source, ":", lineno, ":", colno)

  // Try to report error to Python if eel is available
  if (typeof window.eel !== "undefined") {
    try {
      // Try both error handlers to ensure at least one works
      if (window.eel.handle_error) {
        window.eel.handle_error(message)
      }
      if (window.eel.patch_handle_error) {
        window.eel.patch_handle_error(message)
      }
    } catch (e) {
      console.error("Failed to report error to Python:", e)
    }
  }

  return true // Prevents the default error handling
}

// Add error handling for Eel functions when DOM is loaded
document.addEventListener("DOMContentLoaded", () => {
  console.log("DOM loaded, initializing error handler")

  // Check if eel is available
  if (typeof window.eel !== "undefined" && window.eel.expose) {
    // Store the original expose function
    var originalExpose = window.eel.expose

    // Override the expose function to add error handling
    window.eel.expose = (fn, name) => {
      // Create a wrapped function that catches errors
      var wrappedFn = function () {
        try {
          return fn.apply(this, arguments)
        } catch (e) {
          console.error("Error in exposed function " + (name || fn.name) + ":", e)

          // Try to report error to Python
          if (window.eel.handle_error) {
            window.eel.handle_error("Error in " + (name || fn.name) + ": " + e.message)
          }
          if (window.eel.patch_handle_error) {
            window.eel.patch_handle_error("Error in " + (name || fn.name) + ": " + e.message)
          }

          throw e
        }
      }

      // Call the original expose function with the wrapped function
      return originalExpose(wrappedFn, name)
    }

    console.log("Eel expose function patched for error handling")
  } else {
    console.warn("Eel not available or expose method missing")
  }
})

