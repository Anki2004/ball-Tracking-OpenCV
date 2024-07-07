# import cv2
# import numpy as np
# from collections import defaultdict

# # Define color ranges (in HSV)
# COLOR_RANGES = {
#     'red': ([0, 100, 100], [10, 255, 255]),
#     'blue': ([110, 100, 100], [130, 255, 255]),
#     'green': ([50, 100, 100], [70, 255, 255]),
#     'yellow': ([20, 100, 100], [30, 255, 255])
# }

# def detect_balls(frame):
#     hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
#     balls = {}

#     for color, (lower, upper) in COLOR_RANGES.items():
#         mask = cv2.inRange(hsv, np.array(lower), np.array(upper))
#         mask = cv2.erode(mask, None, iterations=2)
#         mask = cv2.dilate(mask, None, iterations=2)
        
#         contours, _ = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
#         for contour in contours:
#             if cv2.contourArea(contour) > 100:  # Minimum area threshold
#                 M = cv2.moments(contour)
#                 center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
#                 balls[center] = color

#     return balls
    

# def update_trackers(trackers, balls, frame_count):
#     for center, color in balls.items():
#         if color not in trackers or all(abs(existing_center[0] - center[0]) > 20 or abs(existing_center[1] - center[1]) > 20 for existing_center in trackers[color]):
#             trackers[color][center] = {'first_seen': frame_count, 'last_seen': frame_count, 'current_quadrant': get_quadrant(center)}
#         else:
#             closest_center = min(trackers[color], key=lambda x: ((x[0] - center[0])**2 + (x[1] - center[1])**2)**0.5)
#             trackers[color][closest_center]['last_seen'] = frame_count
#             trackers[color][closest_center]['current_quadrant'] = get_quadrant(center)
#             if closest_center != center:
#                 trackers[color][center] = trackers[color].pop(closest_center)

# def get_quadrant(center):
#     x, y = center
#     if x < 320 and y < 240:
#         return 1
#     elif x >= 320 and y < 240:
#         return 2
#     elif x < 320 and y >= 240:
#         return 3
#     else:
#         return 4

# def check_events(trackers, frame_count):
#     events = []
#     colors_to_remove = []
    
#     for color in list(trackers.keys()):
#         centers_to_remove = []
#         for center in list(trackers[color].keys()):
#             data = trackers[color][center]
#             if frame_count - data['last_seen'] > 5:  # Ball disappeared
#                 events.append({
#                     'time': data['last_seen'],
#                     'quadrant': data['current_quadrant'],
#                     'color': color,
#                     'type': 'Exit'
#                 })
#                 centers_to_remove.append(center)
#             elif data['first_seen'] == frame_count:  # New ball appeared
#                 events.append({
#                     'time': frame_count,
#                     'quadrant': data['current_quadrant'],
#                     'color': color,
#                     'type': 'Entry'
#                 })
#             elif data['current_quadrant'] != get_quadrant(center):  # Ball changed quadrant
#                 events.append({
#                     'time': frame_count,
#                     'quadrant': data['current_quadrant'],
#                     'color': color,
#                     'type': 'Exit'
#                 })
#                 data['current_quadrant'] = get_quadrant(center)
#                 events.append({
#                     'time': frame_count,
#                     'quadrant': data['current_quadrant'],
#                     'color': color,
#                     'type': 'Entry'
#                 })
        
#         # Remove centers after iteration
#         for center in centers_to_remove:
#             del trackers[color][center]
        
#         # If no balls of this color left, mark color for removal
#         if not trackers[color]:
#             colors_to_remove.append(color)
    
#     # Remove colors after iteration
#     for color in colors_to_remove:
#         del trackers[color]
    
#     return events

import cv2
import numpy as np
from collections import defaultdict
from sklearn.cluster import KMeans

def detect_balls(frame, n_colors=4):
    # Convert the frame to RGB (from BGR)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    # Reshape the image to be a list of pixels
    pixels = rgb_frame.reshape((-1, 3))
    
    # Perform k-means clustering
    kmeans = KMeans(n_clusters=n_colors, random_state=42)
    kmeans.fit(pixels)
    
    # Get the colors
    colors = kmeans.cluster_centers_.astype(int)
    
    balls = {}
    
    for color in colors:
        # Create a mask for this color
        lower = np.array([max(0, c - 30) for c in color])
        upper = np.array([min(255, c + 30) for c in color])
        
        mask = cv2.inRange(rgb_frame, lower, upper)
        
        # Erode and dilate to remove noise
        mask = cv2.erode(mask, None, iterations=2)
        mask = cv2.dilate(mask, None, iterations=2)
        
        # Find contours in the mask
        contours, _ = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        for contour in contours:
            if cv2.contourArea(contour) > 100:  # Minimum area threshold
                M = cv2.moments(contour)
                center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
                color_name = f'Color_{",".join(map(str, color))}'
                balls[center] = color_name

    return balls

def update_trackers(trackers, balls, frame_count):
    for center, color in balls.items():
        if color not in trackers or all(abs(existing_center[0] - center[0]) > 20 or abs(existing_center[1] - center[1]) > 20 for existing_center in trackers[color]):
            trackers[color][center] = {'first_seen': frame_count, 'last_seen': frame_count, 'current_quadrant': get_quadrant(center)}
        else:
            closest_center = min(trackers[color], key=lambda x: ((x[0] - center[0])**2 + (x[1] - center[1])**2)**0.5)
            trackers[color][closest_center]['last_seen'] = frame_count
            trackers[color][closest_center]['current_quadrant'] = get_quadrant(center)
            if closest_center != center:
                trackers[color][center] = trackers[color].pop(closest_center)

def check_events(trackers, frame_count):
    events = []
    colors_to_remove = []
    
    for color in list(trackers.keys()):
        centers_to_remove = []
        for center in list(trackers[color].keys()):
            data = trackers[color][center]
            if frame_count - data['last_seen'] > 5:  # Ball disappeared
                events.append({
                    'time': data['last_seen'],
                    'quadrant': data['current_quadrant'],
                    'color': color,
                    'type': 'Exit'
                })
                centers_to_remove.append(center)
            elif data['first_seen'] == frame_count:  # New ball appeared
                events.append({
                    'time': frame_count,
                    'quadrant': data['current_quadrant'],
                    'color': color,
                    'type': 'Entry'
                })
            elif data['current_quadrant'] != get_quadrant(center):  # Ball changed quadrant
                events.append({
                    'time': frame_count,
                    'quadrant': data['current_quadrant'],
                    'color': color,
                    'type': 'Exit'
                })
                data['current_quadrant'] = get_quadrant(center)
                events.append({
                    'time': frame_count,
                    'quadrant': data['current_quadrant'],
                    'color': color,
                    'type': 'Entry'
                })
        
        # Remove centers after iteration
        for center in centers_to_remove:
            del trackers[color][center]
        
        # If no balls of this color left, mark color for removal
        if not trackers[color]:
            colors_to_remove.append(color)
    
    # Remove colors after iteration
    for color in colors_to_remove:
        del trackers[color]
    
    return events

def get_quadrant(center):
    x, y = center
    if x < 320 and y < 240:
        return 1
    elif x >= 320 and y < 240:
        return 2
    elif x < 320 and y >= 240:
        return 3
    else:
        return 4