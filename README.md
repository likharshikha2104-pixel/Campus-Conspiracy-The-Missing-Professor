Campus Conspiracy: An AI-Driven Detective Mystery Game
Abstract—This paper presents "Campus Conspiracy: The Missing Professor," an interactive, AI-driven detective thriller implemented using Python and Streamlit. The application leverages Google's Generative AI (Gemini) to simulate dynamic, real-time suspect interrogations. Players navigate through multiple campus locations, collect digital and physical evidence, and confront suspects whose stress levels dynamically adapt based on presented evidence. The game culminates in the deductive identification of the culprit, Vikram Rao, based on carefully pieced-together clues such as lab access logs and security footage. This project demonstrates the potential of integrating Large Language Models (LLMs) into interactive narrative gaming for educational and entertainment purposes.
Keywords—Streamlit, Generative AI, Large Language Models, Interactive Fiction, Gamification.

I. INTRODUCTION
The integration of Large Language Models (LLMs) into video games and interactive storytelling has opened new avenues for dynamic narrative generation. "Campus Conspiracy: The Missing Professor" is a web-based interactive mystery game where players assume the role of a lead detective investigating the disappearance of Professor Sharma, who vanished after discovering an illegal AI research project. The game relies on a combination of predefined logic and generative AI to create a responsive and immersive player experience.

II. SYSTEM ARCHITECTURE
The application is built primarily using Python, utilizing the **Streamlit** framework for rapid frontend development and state management. The backend integrates with **Google Generative AI (Gemini API)** to facilitate natural language interactions with non-playable characters (NPCs).
A. Modular Design
The project is structured modularly for maintainability:
- `app.py`: The main application entry point, handling UI rendering, state management, and API calls.
- `suspects.py`: Contains dictionaries mapping suspect names to their background profiles.
- `clues.py`: Maps campus locations to specific discoverable items.
- `evidence_details.py`: Provides detailed descriptions of the significance of each clue.
B. User Interface and State Management
The UI utilizes custom CSS to create a "detective noir" aesthetic, hiding default Streamlit headers and applying dark themes, sleek sidebars, and custom card layouts. `st.session_state` is heavily utilized to persist the player's progress, tracking collected evidence, detective score, interrogation chat histories, and the individual stress levels of suspects.

III. GAMEPLAY MECHANICS
The gameplay is divided into several key phases accessible via a tabbed interface.
A. Crime Scene Investigation
Players can explore three primary locations: The Professor's Office, the Library, and the Computer Lab. Each location contains specific clues (e.g., a "Torn Note" or "Deleted Email"). Interacting with clues adds them to the player's inventory and increases their "Detective Reputation Score." A specialized puzzle mechanic is implemented for a locked USB drive, requiring the player to deduce a 4-digit cipher based on contextual hints.
B. Suspect Interrogation and Stress Mechanics
The game features six distinct suspects, each with unique backgrounds and specific "weaknesses" tied to collected evidence. When interrogating a suspect, the player can choose to ask standard questions or confront them with specific evidence. 
A core mechanic is the **Stress Bar**. Confronting a suspect with their specific weakness (e.g., confronting Vikram Rao with the "Lab Access Log") significantly spikes their stress level (+35%), while other evidence causes minor spikes (+10%). 
C. Final Verdict
The game concludes when the player issues an official arrest warrant. The game logic validates the selection against the predefined culprit (Vikram Rao), rewarding the player for correct deduction or penalizing them if the true culprit escapes.

IV. GENERATIVE AI INTEGRATION
The core innovation of this project is the use of the Gemini 2.5 Flash model to drive suspect dialogue. During interrogation, a dynamic prompt is constructed including:
1. The suspect's character background.
2. Their current calculated stress level.
3. The player's question and any confronted evidence.
The LLM is instructed to stay in character, adjust its tone based on stress (e.g., acting defensive if stress is >50%), and react nervously if confronted with relevant evidence, without outright confessing. This allows for open-ended, non-linear dialogue that responds organically to the player's investigative choices. Fallback static responses are provided in case of API failure.

V. CONCLUSION
"Campus Conspiracy" successfully demonstrates a lightweight, scalable approach to building AI-driven interactive fiction. By combining deterministic state management for game progression with non-deterministic LLM generation for character interaction, the project achieves a high degree of replayability and immersion. Future work could involve expanding the generative aspects to dynamically generate clues and entirely new mystery scenarios.

VI. REFERENCES
[1] Google Generative AI Documentation, "Gemini API," Google, 2024.
[2] Streamlit Documentation, "State management," Streamlit Inc., 2024.
