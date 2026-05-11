import cv2
import os
import datetime

class RobotVision:
    """
    A class to handle the robot's camera.
    Provides functions to take snapshots and detect if a person is looking at the robot.
    """
    def __init__(self, camera_index=0, save_directory="robot_images"):
        """
        Initialize the camera module.
        :param camera_index: Usually 0 for the default built-in camera or USB webcam.
        :param save_directory: The folder where the robot will save its photos.
        """
        self.camera_index = camera_index
        self.save_directory = save_directory
        
        # Create a directory to store images if it doesn't exist
        if not os.path.exists(self.save_directory):
            os.makedirs(self.save_directory)
            
        # Load OpenCV's pre-trained face detection model (Haar Cascade)
        # This is lightweight, runs completely offline, and has zero token caps!
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    def take_snapshot(self):
        """
        Briefly turns on the camera, takes a photo, saves it, and turns the camera off.
        Returns the path to the saved file.
        """
        cap = cv2.VideoCapture(self.camera_index)
        
        if not cap.isOpened():
            print("RobotVision Error: Could not access the camera.")
            return None
            
        # Read a frame from the camera
        ret, frame = cap.read()
        cap.release() # Immediately release the camera so other apps can use it
        
        if not ret:
            print("RobotVision Error: Could not read frame from camera.")
            return None
            
        # Generate a filename using the current date and time
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"snapshot_{timestamp}.jpg"
        filepath = os.path.join(self.save_directory, filename)
        
        # Save the image to the drive
        cv2.imwrite(filepath, frame)
        print(f"RobotVision: Snapshot saved to {filepath}")
        
        return filepath

    def scan_for_people(self):
        """
        Scans the camera feed to see if any humans are present.
        Returns a tuple: (Boolean indicating if person found, Integer count of people)
        """
        cap = cv2.VideoCapture(self.camera_index)
        ret, frame = cap.read()
        cap.release()
        
        if not ret:
            return False, 0
            
        # Convert image to Grayscale (Face detection works better and faster in black & white)
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Detect faces
        faces = self.face_cascade.detectMultiScale(
            gray_frame, 
            scaleFactor=1.1, 
            minNeighbors=5, 
            minSize=(30, 30)
        )
        
        person_count = len(faces)
        person_found = person_count > 0
        
        return person_found, person_count


# ==========================================
# Example usage / Testing the script directly
# ==========================================
if __name__ == "__main__":
    vision = RobotVision()
    
    print("Testing Robot Camera...")
    
    # 1. Test taking a photo
    saved_path = vision.take_snapshot()
    
    # 2. Test person detection
    found, count = vision.scan_for_people()
    if found:
        print(f"Success! I can see {count} person/people in the room right now.")
    else:
        print("I don't see anyone in front of the camera right now.")
