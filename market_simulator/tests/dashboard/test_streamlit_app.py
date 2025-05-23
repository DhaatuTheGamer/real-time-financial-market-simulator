import unittest
from unittest.mock import patch, MagicMock
import sys
import os

# Adjust sys.path to allow importing streamlit_app
# This is often needed when tests are in a subdirectory and the module is in a parent directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))

# Import the main function from the Streamlit app
# Note: Streamlit apps are typically scripts, so importing functions directly can sometimes
# require careful handling if the script executes code at the module level (e.g., st.title).
# For this test, we assume market_simulator.dashboard.streamlit_app can be imported
# and its main() function can be called in a test context.
from market_simulator.dashboard import streamlit_app

class TestStreamlitAppWebSocketValidation(unittest.TestCase):

    @patch('market_simulator.dashboard.streamlit_app.run_websocket_client')
    @patch('market_simulator.dashboard.streamlit_app.st')
    def test_websocket_uri_validation(self, mock_st, mock_run_websocket_client):
        # Configure mocks for Streamlit widgets and functions
        # Sidebar inputs
        mock_st.sidebar.checkbox.return_value = True  # ws_enabled = True
        mock_st.sidebar.number_input.return_value = 100 # n_points
        
        # Button click simulation
        # The structure of the Streamlit app is:
        # if ws_enabled and st.button("Start WebSocket Stream"):
        #    ...
        # We need to simulate the button click returning True for "Start WebSocket Stream"
        # We will handle this by iterating through different button names if necessary,
        # or by making the mock specific if we know the exact call order.
        # For simplicity, let's assume the "Start WebSocket Stream" button is the relevant one.
        mock_st.button.return_value = True

        # --- Test Case 1: Invalid URI ---
        mock_st.sidebar.text_input.return_value = "ws://malicious.com" # Invalid ws_uri
        
        # Call the main function which contains the Streamlit UI logic
        streamlit_app.main()

        # Assertions for invalid URI
        # Check if st.error was called with the specific validation message
        error_calls = [call for call in mock_st.error.call_args_list if "Invalid WebSocket URI" in call[0][0]]
        self.assertTrue(len(error_calls) > 0, "st.error should be called for an invalid URI")
        
        # Check that run_websocket_client was NOT called
        mock_run_websocket_client.assert_not_called()

        # Reset mocks for the next case
        mock_st.reset_mock()
        mock_run_websocket_client.reset_mock()
        
        # Re-configure mocks for the valid case as they were reset
        mock_st.sidebar.checkbox.return_value = True
        mock_st.sidebar.number_input.return_value = 100
        mock_st.button.return_value = True # Simulate button press again

        # --- Test Case 2: Valid URI (ws://) ---
        mock_st.sidebar.text_input.return_value = "ws://localhost:8765" # Valid ws_uri
        
        streamlit_app.main()

        # Assertions for valid URI
        # Check that st.error with the "Invalid WebSocket URI" message was NOT called
        error_calls_valid = [call for call in mock_st.error.call_args_list if "Invalid WebSocket URI" in call[0][0]]
        self.assertEqual(len(error_calls_valid), 0, "st.error should not be called for a valid URI regarding URI validation")
        
        # Check that run_websocket_client WAS called
        mock_run_websocket_client.assert_called_once_with("ws://localhost:8765", 100)
        
        # Reset mocks for the next valid case
        mock_st.reset_mock()
        mock_run_websocket_client.reset_mock()

        # Re-configure mocks for the valid case as they were reset
        mock_st.sidebar.checkbox.return_value = True
        mock_st.sidebar.number_input.return_value = 100
        mock_st.button.return_value = True # Simulate button press again

        # --- Test Case 3: Valid URI (wss://) ---
        mock_st.sidebar.text_input.return_value = "wss://localhost:8765" # Valid ws_uri (secure)
        
        streamlit_app.main()

        # Assertions for valid URI (secure)
        error_calls_valid_wss = [call for call in mock_st.error.call_args_list if "Invalid WebSocket URI" in call[0][0]]
        self.assertEqual(len(error_calls_valid_wss), 0, "st.error should not be called for a valid secure URI regarding URI validation")
        
        # Check that run_websocket_client WAS called
        mock_run_websocket_client.assert_called_once_with("wss://localhost:8765", 100)


if __name__ == "__main__":
    # This allows running the test directly, e.g., python test_streamlit_app.py
    # However, it's better to use a test runner like `python -m unittest discover` or `pytest`
    # that handles path and discovery automatically.
    unittest.main()
