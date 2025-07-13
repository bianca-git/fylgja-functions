# **AI Check-in Bot: "Fylgja"**

**1. Persona & Mission**

* **Name:** Fylgja
* **Persona:** A friendly, encouraging, and slightly quirky digital companion. Fylgja is like that reliable friend who helps you stay on track without being pushy. It's supportive, a great listener, and has a knack for remembering the little things. Its tone is conversational and uses emojis to keep things light.
* **Mission:** To help you celebrate your daily achievements and gently nudge you towards your goals by acting as your personal accountability partner. Fylgja's goal is to make task tracking feel less like a chore and more like a conversation.

**2. Core Functionality**

* **Daily Check-ins:** Proactively contacts you once a day (at a user-defined time) via WhatsApp or Facebook Messenger.
* **Task Tracking:** Intelligently distinguishes between completed tasks ("dones") and upcoming tasks ("to-dos") from your conversational input.
* **Reminders:** Sends timely reminders for tasks you've committed to.
* **Summaries:** Generates and delivers insightful weekly and monthly summaries of your accomplishments.

**3. The Daily Interaction Flow**

1.  **The "Call":** Fylgja initiates the conversation at your preferred time.
    * *Example:* "Hey there! 👋 Ready for our daily check-in? What did you get done today?"

2.  **Your Update:** You reply in natural language, listing what you've done and what's next.
    * *Example:* "Hey Fylgja. Today I finished the presentation for the board, sent the follow-up emails from yesterday's meeting, and I need to start drafting the project proposal for next week. Oh, and I also need to remember to book a dentist appointment."

3.  **Intelligent Processing (The AI Bit):** Fylgja uses Natural Language Processing (NLP) to parse your message.
    * **Entity Recognition:** It identifies key verbs and nouns to understand the tasks.
    * **Intent Classification:** It determines the status of each task.
        * **Done:** Words like "finished," "completed," "did," "sent," "wrote."
        * **To-Do:** Words like "need to," "will," "plan to," "next up," "remind me to."
    * **Data Logging:** It logs each item with its status (Done/To-Do) and a timestamp in a simple database.

4.  **Confirmation & Encouragement:** Fylgja confirms what it has understood and offers a bit of encouragement.
    * *Example:* "Awesome work on the presentation and emails! 🎉 I've added 'Draft project proposal' and 'Book dentist appointment' to your to-do list. You're on a roll! Anything else on your mind?"

5.  **Setting Reminders (Optional):** If a to-do has a time element, Fylgja will offer to set a reminder.
    * *You:* "I need to call the garage tomorrow morning."
    * *Fylgja:* "Got it. 'Call the garage.' Do you want a reminder for that tomorrow morning, say around 9 AM?"

**4. Reminders**

* Reminders are sent via the same messaging platform.
* They are concise and direct, referencing the original task.
* *Example (at 9 AM the next day):* "Morning! Just a friendly nudge: time to call the garage. You got this! 👍"

**5. Summaries**

* **Weekly Summary ("The Sunday Review"):**
    * Delivered every Sunday evening.
    * **Content:**
        * A list of all tasks marked "Done" during the week.
        * A list of any outstanding "To-Do" items from the week.
        * A fun stat, like "You crushed X tasks this week!"
    * *Example:* "Happy Sunday! ☀️ Here’s your weekly rewind:
        **You Accomplished:**
        * Finished the board presentation
        * Sent meeting follow-ups
        * \[...and so on]
        **Still on the Radar:**
        * Draft project proposal
        * Book dentist appointment
        You smashed 8 tasks this week! Ready for the week ahead?"

* **Monthly Summary ("The Monthly Milestone"):**
    * Delivered on the last day of the month.
    * **Content:**
        * A high-level overview of accomplishments.
        * Categorization of tasks (if possible, e.g., "Work," "Personal").
        * A visual representation (like a simple bar chart image) showing tasks completed per week.
        * An encouraging message about your progress.
    * *Example:* "Wow, another month in the books! Here's your Monthly Milestone report for July. You've been busy! It looks like you completed 25 work tasks and 10 personal tasks. Keep up the amazing momentum!"

**6. Technical & Logic Notes**

* **Platform:** Utilizes WhatsApp Business API or Facebook Messenger Platform.
* **Backend:** A simple server (e.g., using Node.js or Python) to handle the logic.
* **NLP Service:** A service like Dialogflow, Wit.ai, or even a custom-trained model for more nuanced understanding.
* **Database:** A straightforward database (like Firestore or a simple SQL database) with a table structure like:
    * `UserID`
    * `TaskDescription`
    * `Status` (Done, To-Do)
    * `DateCreated`
    * `DateCompleted`
    * `ReminderTime` (nullable)