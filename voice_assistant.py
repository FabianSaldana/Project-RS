import speech_recognition as sr
import pyttsx3
from transformers import pipeline
import warnings

# Import the class we created previously
from environment_sensor import EnvironmentSensor

# Suppress warnings from the transformers library for a cleaner terminal output
warnings.filterwarnings("ignore")

class VoiceAssistant:
    def __init__(self):
        # 1. Initialize our Sensors
        self.sensor = EnvironmentSensor(sensor_pin=4)
        
        # 2. Initialize Text-to-Speech (TTS)
        # pyttsx3 runs completely offline and locally, so there are no token caps!
        self.tts_engine = pyttsx3.init()
        self.tts_engine.setProperty('rate', 160) # Adjust speech speed
        
        # 3. Initialize Speech-to-Text (STT)
        self.recognizer = sr.Recognizer()
        
        # 4. Initialize the "Simple LLM" (Zero-Shot Classifier)
        # We use a lightweight HuggingFace Transformer for Natural Language Processing.
        # This runs 100% locally on your machine. No API keys, no internet required, NO TOKEN CAPS.
        # It's smart enough to understand "how hot is it", "what's the weather", "tell me the temp", etc.
        print("Loading local AI brain... (This takes a moment but ensures no token limits later)")
        self.classifier = pipeline(
            "zero-shot-classification", 
            model="cross-encoder/nli-distilroberta-base"
        )
        
        # These are the intents the AI will try to map your speech to
        self.intents = ["temperature", "humidity", "date", "greeting", "exit"]
        print("AI Brain loaded and ready!")

    def speak(self, text):
        """Convert text back to speech using the local TTS engine."""
        print(f"Robot: {text}")
        self.tts_engine.say(text)
        self.tts_engine.runAndWait()

    def listen(self):
        """Listen to the microphone and convert speech to text."""
        with sr.Microphone() as source:
            print("\nListening... (Speak now)")
            # Adjust for ambient noise so the mic doesn't trigger on static
            self.recognizer.adjust_for_ambient_noise(source, duration=1)
            try:
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=10)
                
                # Using Google's free default STT endpoint for easy setup. 
                # (If you want 100% offline STT later, you can swap this to 'recognize_sphinx' or Vosk)
                text = self.recognizer.recognize_google(audio)
                print(f"You : {text}")
                return text.lower()
            except sr.WaitTimeoutError:
                return None
            except sr.UnknownValueError:
                print("(Could not understand audio)")
                return None
            except sr.RequestError as e:
                print(f"(Network error for STT: {e})")
                return None

    def analyze_command(self, text):
        """Use the local NLP model to figure out what the user wants."""
        # The AI compares your spoken text to our list of intents and returns probabilities
        result = self.classifier(text, self.intents)
        
        best_intent = result['labels'][0]
        confidence = result['scores'][0]
        
        # If the AI is not confident, it will ask for clarification
        if confidence < 0.4:
            return "unknown"
            
        return best_intent

    def run(self):
        """Main loop keeping the robot awake and listening."""
        self.speak("I am online and ready to assist you.")
        
        while True:
            user_speech = self.listen()
            
            if user_speech:
                intent = self.analyze_command(user_speech)
                
                if intent == "temperature":
                    temp = self.sensor.get_temperature()
                    self.speak(f"The current temperature is {temp} degrees Celsius.")
                    
                elif intent == "humidity":
                    hum = self.sensor.get_humidity()
                    self.speak(f"The current humidity is {hum} percent.")
                    
                elif intent == "date":
                    date_str = self.sensor.get_date()
                    self.speak(f"Today is {date_str}.")
                    
                elif intent == "greeting":
                    self.speak("Hello there! You can ask me for the time, temperature, or humidity.")
                    
                elif intent == "exit":
                    self.speak("Shutting down the voice assistant. Goodbye!")
                    break
                else:
                    self.speak("I heard you, but I'm not sure if you want the temperature, humidity, or the date.")

if __name__ == "__main__":
    assistant = VoiceAssistant()
    assistant.run()
