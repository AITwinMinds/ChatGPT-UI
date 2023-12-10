<h1 align="left">ChatGPT Interface</h1>

<img align="right" width="100" height="100" src="https://github.com/AITwinMinds/ChatGPT-UI/blob/main/icon.png" alt="ChatGPT Interface">

This repository contains a graphical user interface (GUI) for seamless interaction with OpenAI's GPT-3.5 Turbo model using the ChatGPT API. The interface, built using PyQt5, offers an intuitive and feature-rich environment for generating responses, rephrasing text, debugging code, summarizing content, translating languages, and more.

## Features

- **🌙 Dark Theme & ☀️ Light Theme**: Enjoy a sleek and eye-friendly dark theme for a comfortable and visually appealing interface, especially during nighttime usage. Additionally, a light theme is now available for a refreshing look.
  
- **🔝 Always On Top**: Quickly access ChatGPT UI with the enhanced *Always On Top* feature, allowing you to keep it above other applications.

- **🔄 HTTP Proxy Support**: Enable an HTTP proxy for communication with the ChatGPT API.

- **🖋️ Prompt Options**: Choose from a variety of prompt options, including:

   - **Paraphrasing**: `Standard`, `Fluency`, `Formal`, `Academic`, `Simple`, `Creative`, `Expand`, and `Shorten`

   - **Rewrite Level Selector**: Choose how many different rewrites you want to receive (max 20).

   - **Other Prompt Options**:
      - Debug code
      - Summarize
      - Custom prompt 
      - Check grammar
      - Translate
      - Reply to email
      - Explain

- **🌐 Language Translation**: Translate text from one language to another using the language dropdowns.

- **✍️ Grammar Checker**: Correct and provide in `Original Text`, `Differences Highlighted`, and `Corrected Text`.

- **📧 Enhance Email Prompt**: Add specific information to enhance the email prompt with a convenient checkbox option.

- **🎨 Code Highlighting**: Code blocks in the output are highlighted for better readability.

- **📋 Clipboard Integration**: Easily apply text from the clipboard as part of the prompt with a single checkbox.

- **🔒 Keep Previous Responses**: Retain previous responses while generating a new one by toggling the checkbox option.

- **🤝 User-Friendly Interface**: Enjoy a clean and intuitive interface for easy prompt input and response viewing.

## Usage

1. **Obtaining API Key**: Obtain your API key from OpenAI platform ([https://platform.openai.com/api-keys](https://platform.openai.com/api-keys)). <br>
(As a free user, you can enjoy the first three months of API key usage for free. After this period, consider buying credits or creating a new account to access an additional three months of free usage.)

2. **Entering API Key**: Once you have your API key, enter it into the designated field in the interface. You can toggle the fix/unfix status by clicking "Fix/Unfix API Key."

<div align="center">
  <img src="https://github.com/AITwinMinds/ChatGPT-UI/assets/127874551/87d1c639-da90-48ab-9426-182eba660940" />
</div>
<br>

3. **Prompt Selection**: Choose the type of prompt you want to generate by selecting the appropriate radio button. For rephrasing, use the new dropdown menu that offers five different types, including Simplify, Informal, Professional, Formal, and Generalize.

<div align="center">
  <img src="https://github.com/AITwinMinds/ChatGPT-UI/assets/127874551/eb844792-55d7-4e1e-be56-4db845da692c" />
</div>
<br>

4. **Language Translation**: If translating, select the source and target languages from the dropdowns.

<div align="center">
  <img src="https://github.com/AITwinMinds/ChatGPT-UI/assets/127874551/97f0e93d-0116-4277-b569-581fcec59075" />
</div>
<br>

5. **Clipboard Option**: By checking the "Use last clipboard text" checkbox, you can easily apply the text from your clipboard as part of the prompt. This provides a quick way to incorporate external content into your queries.

<div align="center">
  <img src="https://github.com/AITwinMinds/ChatGPT-UI/assets/127874551/c09f2324-beff-41e2-86db-0822218b103e" />
</div>
<br>

6. **Email Reply Customization**: When replying to emails, you can now add specific details to the prompt for a more personalized and context-aware response.

<div align="center">
  <img src="https://github.com/AITwinMinds/ChatGPT-UI/assets/127874551/d1af7244-a32a-4ec8-92fb-8b528464e3da" />
</div>
<br>

7. **Input Text**: Enter the prompt manually or input text for manual prompts.

<div align="center">
  <img src="https://github.com/AITwinMinds/ChatGPT-UI/assets/127874551/6e30f217-0b7e-420b-a5f3-9be214ccf5a3" />
</div>
<br>

8. **HTTP Proxy**: Enable the HTTP proxy option and configure the proxy server and port if necessary.

<div align="center">
  <img src="https://github.com/AITwinMinds/ChatGPT-UI/assets/127874551/d64a099b-0dc7-4422-8ed1-c91eaed7f0ab" />
</div>
<br>

9. **Generate Response**: Click the "Generate" button to generate a response based on the selected options.

10. **Stop Process**: Click the "Stop" button to halt the response generation process.


## Download

- Executable files for different operating systems can be downloaded from the [Releases](https://github.com/AITwinMinds/ChatGPT-UI/releases) page.

  - 💻 **Windows**: [Direct download for Windows](https://github.com/AITwinMinds/ChatGPT-UI/releases/download/v3.0/ChatGPT-UI-Windows.exe)
  - 🍏 **macOS**: [Direct download for macOS](https://github.com/AITwinMinds/ChatGPT-UI/releases/download/v3.0/ChatGPT-UI-macOS.app.zip)
  - 🐧 **Linux**: [Direct download for Linux](https://github.com/AITwinMinds/ChatGPT-UI/releases/download/v3.0/ChatGPT-UI-Linux)

## Running on macOS
1. **Download the .app.zip file.**
2. **Open Terminal and navigate to the directory where you downloaded the file and unzip the file:**
 ```bash
 cd /path/to/downloaded/file
 unzip ChatGPT-UI-macOS.app.zip
 ```
3. **Fix Damaged App Error:**
- If you encounter the "ChatGPT-UI-macOS.app is damaged and can't be opened" error, run the following commands in Terminal:
```bash
cd /path/to/extracted/folder
xattr -rc ChatGPT-UI-macOS.app && codesign --force --deep --sign - ChatGPT-UI-macOS.app
```
4. **Run the App:**
   - After completing the above steps, try running the application again.


## Running on Linux
Linux users can run the application using the following command:

```bash
./ChatGPT-UI-Linux
```

If you encounter a "Permission denied" error, follow these steps:

1. Navigate to the directory containing the ChatGPT-UI-Linux executable:

    ```bash
    cd /path/to/directory/containing/
    ```

2. Grant execute permissions to the ChatGPT-UI-Linux file:

    ```bash
    chmod +x ChatGPT-UI-Linux
    ```

3. Try running the application again:

    ```bash
    ./ChatGPT-UI-Linux
    ```
## Theme

1. Windows:
![image](https://github.com/AITwinMinds/ChatGPT-UI/assets/100919352/a114f5e2-4647-4ff1-8cac-7db0b05586ae)

2. MacOS:
   
## Video Guide on YouTube

Learn how to use the ChatGPT Interface effectively by watching our upcoming video guide on YouTube. The guide will cover topics such as prompt selection, language translation, clipboard integration, and more.

[Subscribe to our YouTube Channel](https://www.youtube.com/@AITwinMinds) for the latest updates and tutorials on ChatGPT Interface. Stay tuned for the upcoming video guide!

## Contributions

Contributions are welcome! Feel free to open issues or submit pull requests to improve the functionality or fix any issues.

## License

This project is licensed under the [GNU General Public License v3.0](LICENSE).

## Support Us

This app is completely free! If you find it helpful, consider supporting us in the following ways:

- ⭐ Star this repository on [GitHub](https://github.com/AITwinMinds/ChatGPT-UI).
  
- 🐦 Follow us on X (Twitter): [@AITwinMinds](https://twitter.com/AITwinMinds)

- 📣 Join our Telegram Channel: [AITwinMinds](https://t.me/AITwinMinds) for discussions and announcements.

- 🎥 Subscribe to our YouTube Channel: [AITwinMinds](https://www.youtube.com/@AITwinMinds) for video tutorials and updates.

- 📸 Follow us on Instagram: [@AITwinMinds](https://www.instagram.com/AITwinMinds)


Don't forget to provide feedback by commenting on the repository and help us make it better. Share it with your friends and let them benefit from this tool!

## Contact

For any inquiries, please contact us at [AITwinMinds@gmail.com](mailto:AITwinMinds@gmail.com).
