import eel
import traceback

# Store the original _process_message function
original_process_message = eel._process_message

# Define our patched version that handles missing 'value' key
def patched_process_message(message, websocket):
    try:
        # Check if this is an error response without a 'value' key
        if 'return' in message and 'status' in message and message.get('status') == 'error':
            # Handle error responses properly
            call_id = message.get('return')
            if call_id in eel._call_return_values:
                # Set a default error value
                eel._call_return_values[call_id] = None
                print(f"Handled error response for call ID {call_id}")
            return
        
        # Otherwise, use the original function
        return original_process_message(message, websocket)
    except Exception as e:
        print(f"Error in patched _process_message: {e}")
        traceback.print_exc()

# Apply the patch
eel._process_message = patched_process_message

# Add a global error handler
@eel.expose
def handle_error(error_message):
    print(f"JavaScript error reported: {error_message}")
