import cv2
import numpy as np
import pyautogui
from scipy.ndimage import gaussian_filter
from datetime import datetime
import time
import os
from pynput import keyboard
import threading
import sys

# Global flag for stopping the recording
recording = True

def on_press(key):
    global recording
    try:
        if key == keyboard.Key.esc:
            print("\nStopping eye tracking recording...")
            recording = False
            return False  # Stop listener
    except AttributeError:
        pass

def minimize_window(window_name):
    try:
        # Get window handle and minimize it
        cv2.namedWindow(window_name)
        cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_NORMAL)
        cv2.setWindowProperty(window_name, cv2.WND_PROP_VISIBLE, 0)
    except:
        pass

# Create output directory for heatmaps
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
output_dir = f'heatmap_session_{timestamp}'
os.makedirs(output_dir, exist_ok=True)

print("Eye tracking recording started!")
print("The recording is now running in the background.")
print("Press 'esc' at any time to stop recording.")
print(f"Output will be saved to: {output_dir}")

# Start keyboard listener in a separate thread
listener = keyboard.Listener(on_press=on_press)
listener.start()

# Initialize eye detector and webcam
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')
cap = cv2.VideoCapture(0)
screen_width, screen_height = pyautogui.size()

# Parameters for heatmap
heatmap = np.zeros((screen_height, screen_width), dtype=np.float32)
cumulative_heatmap = np.zeros((screen_height, screen_width), dtype=np.float32)
decay_rate = 0.9  # Decay factor for heatmap
blur_radius = 50  # Gaussian blur radius
frame_count = 0
save_interval = 30  # Save every 30 frames

# Calibration parameters
calibration_points = [(0, 0), (screen_width-1, 0), 
                     (screen_width-1, screen_height-1), 
                     (0, screen_height-1),
                     (screen_width//2, screen_height//2)]
calibration_data = []
is_calibrated = False

# Smoothing parameters
smooth_factor = 0.3  # Lower = smoother
prev_screen_x, prev_screen_y = screen_width//2, screen_height//2

def calibrate():
    global calibration_data, is_calibrated
    
    print("Starting calibration...")
    calibration_data = []
    
    # Create a window that uses screen dimensions and make it fullscreen
    cv2.namedWindow('Calibration', cv2.WINDOW_NORMAL)
    cv2.setWindowProperty('Calibration', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    cv2.resizeWindow('Calibration', screen_width, screen_height)
    
    for point in calibration_points:
        # Create a blank image with screen dimensions
        calib_image = np.zeros((screen_height, screen_width, 3), dtype=np.uint8)
        
        # Draw calibration point (bigger and with additional visual guides)
        cv2.circle(calib_image, point, 20, (0, 255, 0), -1)  # Main point
        cv2.circle(calib_image, point, 30, (0, 255, 0), 2)   # Outer ring
        
        # Add text instruction
        font = cv2.FONT_HERSHEY_SIMPLEX
        text = "Look at the green dot"
        text_size = cv2.getTextSize(text, font, 1, 2)[0]
        text_x = (screen_width - text_size[0]) // 2
        text_y = screen_height - 50
        cv2.putText(calib_image, text, (text_x, text_y), font, 1, (255, 255, 255), 2)
        
        cv2.imshow('Calibration', calib_image)
        
        # Wait for 2 seconds while user looks at the point
        start_time = time.time()
        point_data = []
        
        while time.time() - start_time < 2:
            ret, frame = cap.read()
            if not ret:
                continue
                
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            eyes = eye_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
            
            if len(eyes) > 0:
                ex, ey, ew, eh = eyes[0]
                eye_center_x = ex + ew // 2
                eye_center_y = ey + eh // 2
                point_data.append((eye_center_x, eye_center_y))
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
        if point_data:
            # Average the eye positions for this calibration point
            avg_x = sum(x for x, _ in point_data) / len(point_data)
            avg_y = sum(y for _, y in point_data) / len(point_data)
            calibration_data.append((avg_x, avg_y, point[0], point[1]))
    
    # Automatically destroy the window once calibration is done
    cv2.destroyWindow('Calibration')
    cv2.waitKey(1)  # Give time for the window to be destroyed
    time.sleep(0.1)  # Small delay to ensure window closes
    
    is_calibrated = True
    print("Calibration complete!")


def map_eye_to_screen(eye_x, eye_y):
    if not is_calibrated or len(calibration_data) < 5:
        return None, None
        
    # Find the closest calibration points and interpolate
    distances = []
    for ex, ey, _, _ in calibration_data:
        dist = np.sqrt((eye_x - ex)**2 + (eye_y - ey)**2)
        distances.append(dist)
    
    # Get the two closest points
    closest_indices = np.argsort(distances)[:2]
    weights = [1/max(d, 0.1) for d in [distances[i] for i in closest_indices]]
    weight_sum = sum(weights)
    weights = [w/weight_sum for w in weights]
    
    screen_x = sum(weights[i] * calibration_data[closest_indices[i]][2] for i in range(2))
    screen_y = sum(weights[i] * calibration_data[closest_indices[i]][3] for i in range(2))
    
    return int(screen_x), int(screen_y)

# Start with calibration
calibrate()

while recording:
    ret, frame = cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    eyes = eye_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    if len(eyes) > 0:
        ex, ey, ew, eh = eyes[0]  # Use the first detected eye
        eye_center_x = ex + ew // 2
        eye_center_y = ey + eh // 2

        # Map eye coordinates to screen coordinates using calibration data
        screen_x, screen_y = map_eye_to_screen(eye_center_x, eye_center_y)
        
        if screen_x is not None and screen_y is not None:
            # Apply smoothing
            screen_x = int(prev_screen_x + smooth_factor * (screen_x - prev_screen_x))
            screen_y = int(prev_screen_y + smooth_factor * (screen_y - prev_screen_y))
            
            # Update previous positions
            prev_screen_x, prev_screen_y = screen_x, screen_y
            
            # Ensure coordinates are within screen bounds
            screen_x = max(0, min(screen_x, screen_width-1))
            screen_y = max(0, min(screen_y, screen_height-1))
            
            # Update heatmaps
            heatmap[screen_y, screen_x] += 1
            cumulative_heatmap[screen_y, screen_x] += 1

    # Decay heatmap to avoid permanent marks
    heatmap *= decay_rate

    # Apply Gaussian blur to simulate heatmap spread
    heatmap_blurred = gaussian_filter(heatmap, sigma=blur_radius)
    cumulative_blurred = gaussian_filter(cumulative_heatmap, sigma=blur_radius)
    
    # Normalize both heatmaps
    heatmap_normalized = cv2.normalize(heatmap_blurred, None, 0, 255, cv2.NORM_MINMAX)
    cumulative_normalized = cv2.normalize(cumulative_blurred, None, 0, 255, cv2.NORM_MINMAX)
    
    # Create color maps
    heatmap_colored = cv2.applyColorMap(heatmap_normalized.astype(np.uint8), cv2.COLORMAP_JET)
    cumulative_colored = cv2.applyColorMap(cumulative_normalized.astype(np.uint8), cv2.COLORMAP_JET)

    # Capture the screen
    screen = np.array(pyautogui.screenshot())
    screen = cv2.cvtColor(screen, cv2.COLOR_RGB2BGR)

    # Ensure heatmap_colored has the same dimensions as screen
    heatmap_colored = cv2.resize(heatmap_colored, (screen.shape[1], screen.shape[0]))
    cumulative_colored = cv2.resize(cumulative_colored, (screen.shape[1], screen.shape[0]))

    # Create overlays
    current_overlay = cv2.addWeighted(screen, 0.6, heatmap_colored, 0.4, 0)
    cumulative_overlay = cv2.addWeighted(screen, 0.6, cumulative_colored, 0.4, 0)

    # Save frames periodically without showing them
    if frame_count % save_interval == 0:
        frame_filename = os.path.join(output_dir, f'heatmap_frame_{frame_count:06d}.png')
        cumulative_filename = os.path.join(output_dir, f'cumulative_frame_{frame_count:06d}.png')
        cv2.imwrite(frame_filename, current_overlay)
        cv2.imwrite(cumulative_filename, cumulative_overlay)

    frame_count += 1

# Save final heatmaps
final_current = os.path.join(output_dir, 'final_current_heatmap.png')
final_cumulative = os.path.join(output_dir, 'final_cumulative_heatmap.png')
cv2.imwrite(final_current, current_overlay)
cv2.imwrite(final_cumulative, cumulative_overlay)

# Clean up
cap.release()
listener.join()  # Clean up keyboard listener

print("\nRecording stopped!")
print(f"All heatmaps have been saved to: {output_dir}")
print("Files saved:")
print("- Periodic snapshots of current heatmap")
print("- Periodic snapshots of cumulative heatmap")
print("- Final current heatmap")
print("- Final cumulative heatmap")