# 2.0 Recode
My code is trash, designed around completions, and very hard to update. This version seeks to 
rectify that so that I can easily add new GPT versions and features. It will disregard completions
and be based only on the chat endpoint, making it incompatible with GPT-3 completion models.

# Main Objectives:

- **Recode chatbot.py to only work with chat models**
- **Code with extensibility in mind**
- **Prune unneeded code**
- **Update modules used to take advantage of new features**

# Future Objectives:

- Use OpenAI TTS by default
- Use updated ElevenLabs python module 
- Revise token recycling model to work with chat mode, be less complete (i.e. no summary of summaries at first, only compression),
and usable with 128,000 token models. Have it be disabled by default in preference of chat pruning (deleting oldest message as needed).
- Add Assistants compatibility
- Add prewritten presets that are more comprehensive
- Use environment variables
- Have an installer that does not rely on a BAT file