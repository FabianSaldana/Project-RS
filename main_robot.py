from environment_sensor import EnvironmentSensor
from voice_assistant import VoiceAssistant
from robot_vision import RobotVision
import time

class MainRobot(VoiceAssistant):
    """
    The master script that controls the robot.
    It inherits from VoiceAssistant (so it gets TTS, STT, and AI intent matching for free),
    and aggregates the EnvironmentSensor and RobotVision modules.
    """
    def __init__(self):
        print("Initializing Main Robot Systems...")
        # Initialize the Parent class (VoiceAssistant) which sets up sensors, TTS, STT, and the AI Brain
        super().__init__()
        
        # Initialize the Vision module
        print("Initializing Vision Module...")
        self.vision = RobotVision()
        
        # Expand the AI's understanding natively by adding new camera intents
        self.intents.extend(["take photo", "scan room"])
        
        # Variable to keep track of if we've already greeted someone recently
        self.has_greeted_person = False

    def run(self):
        """The main execution loop for the robot."""
        self.speak("All systems initialized. Sensors, vision, and voice modules are online.")
        
        while True:
            # 1. Proactive Vision Check
            # If we haven't greeted a person recently, quickly scan the room before listening
            if not self.has_greeted_person:
                person_found, count = self.vision.scan_for_people()
                if person_found:
                    self.speak(f"Oh, hello there! I see you.")
                    self.has_greeted_person = True
            
            # 2. Listen for voice commands
            # This will pause and listen to the mic for a few seconds.
            user_speech = self.listen()
            
            if user_speech:
                # Let the AI brain figure out the intent of what the person said
                intent = self.analyze_command(user_speech)
                print(f"--> AI determined intent: {intent}")
                
                if intent == "temperature":
                    temp = self.sensor.get_temperature()
                    self.speak(f"The temperature is {temp} degrees Celsius.")
                    
                elif intent == "humidity":
                    hum = self.sensor.get_humidity()
                    self.speak(f"The humidity is {hum} percent.")
                    
                elif intent == "date":
                    date_str = self.sensor.get_date()
                    self.speak(f"Today is {date_str}.")
                    
                elif intent == "take photo":
                    self.speak("Taking a picture now. Smile!")
                    filepath = self.vision.take_snapshot()
                    if filepath:
                        self.speak("Snapshot saved successfully to my local drive.")
                    else:
                        self.speak("Sorry, I had an issue accessing my camera.")
                        
                elif intent == "scan room":
                    self.speak("Scanning the area...")
                    person_found, count = self.vision.scan_for_people()
                    if person_found:
                        self.speak(f"I can see {count} person right now.")
                    else:
                        self.speak("I don't see anyone at the moment.")
                        
                elif intent == "greeting":
                    self.speak("Hello! How can I assist you today?")
                    self.has_greeted_person = True 
                    
                elif intent == "exit":
                    self.speak("Powering down my systems. Goodbye!")
                    break
                else:
                    self.speak("I heard you, but I didn't quite understand the command.")
            else:
                # If listen() timed out (no one spoke and it returned None), we can optionally
                # reset the greeting flag so the robot can greet people again if they leave and return.
                # Here we just reset it assuming if it's quiet, maybe they left.
                person_found, _ = self.vision.scan_for_people()
                if not person_found:
                    self.has_greeted_person = False

if __name__ == "__main__":
    robot = MainRobot()
    robot.run()
