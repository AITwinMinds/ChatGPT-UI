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

### API Key Mode

1. **Obtaining API Key**: Obtain your API key from OpenAI platform ([https://platform.openai.com/api-keys](https://platform.openai.com/api-keys)). <br>
(As a free user, you can enjoy the first three months of API key usage for free. After this period, consider buying credits or creating a new account to access an additional three months of free usage.)
For additional guidance, check out this YouTube tutorial: [How to Obtain an OpenAI API Key (ChatGPT-UI version 3 usage guide)](https://www.youtube.com/watch?v=t8DqWHmyT-A)

3. **Entering API Key**: After obtaining your API key, go to the settings menu and select API key. Enter the API key and then click "Save API Key" to apply the changes for the next run.

4. **Prompt Selection**: Choose the type of prompt you want to generate by selecting the appropriate radio button. For paraphrasing, use the new dropdown menu with eight different types, including simplify, informal, professional, formal, academic, simple, creative, expand, shorten, and use the *Rewrite Level Selector* to specify how many different rewrites you want to receive (max 20).

5. **Language Translation**: If translating, select the source and target languages from the dropdowns.

6. **Clipboard Option and Keep Previous Responses**: By checking the *Auto-clipboard input* in the setting, you can easily apply the text from your clipboard as part of the prompt. This provides a quick way to incorporate external content into your queries. Additionally, you can toggle the *Keep replies* checkbox in the setting to retain previous responses while generating a new one.

7. **Email Reply Customization**: When replying to emails, you can now add specific details to the prompt for a more personalized and context-aware response.

8. **Input Text**: Enter the prompt manually or input text for manual prompts.

9. **HTTP Proxy**: Enable the HTTP proxy option in the setting and configure the proxy server and port if necessary.

10. **Generate Response**: Click the *Generate* button to generate a response based on the selected options.

11. **Clear Response**: Click the *Clear response* button to remove the current response, providing a clean slate for new queries.

12. **Copy Response**: Click the *Copy response* button to copy the generated response to your clipboard for easy sharing or reference.

13. **Stop Process**: Click the *Stop* button to halt the response generation process.

### Chrome Mode
Chrome Mode provides an alternative method to use ChatGPT-UI without requiring an API key. To enable Chrome Mode, follow these steps:

1. **Download Chrome Driver:**
   - Determine your Chrome version by checking the "About" section in your Chrome browser (e.g., 120.0.6099).
   - Visit the official Chrome Driver download page: [Chrome Driver Downloads](https://chromedriver.chromium.org/downloads)
   - Depending on your operating system (Windows, Linux, or MacOS), copy the appropriate download link and paste it into your browser's search box or use a download manager for downloading.

2. **Installation:**
   - Extract the downloaded zip file and place the Chrome driver in the same directory as ChatGPT-UI on your system.

3. **Verification:**
   - Confirm the proper functioning of the driver by opening it. An opening terminal should appear.
   - Once verified, close the terminal.

4. **Important Notes:**
   - Close all instances of Chrome before switching to Chrome Mode.
   - Ensure you work with only a single instance while in Chrome Mode for optimal performance.

For additional assistance, refer to the [YouTube usage guide](#).

### File Uploading Feature

In this version, a new and exciting feature has been introduced - the ability to upload PDFs in the `Chrome Mode`, Word documents, or any other text files directly to ChatGPT! To utilize this feature, simply click on the upload button (Attach) to send the text to ChatGPT in Chrome mode. Subsequently, you can ask questions about the uploaded file.

#### Prerequisites

Before using the file uploading feature, ensure you have completed the following steps:

1. **Install the Chrome Extension:**
   - Download and install the `ChatGPT Sidebar & File Uploader` extension for your Chrome browser.
   - Extension Link: [ChatGPT Sidebar & File Uploader](https://chromewebstore.google.com/detail/chatgpt-sidebar-file-uplo/becfinhbfclcgokjlobojlnldbfillpf)

2. **Enjoy Uploading:**
   - Once the extension is successfully installed, you gain the ability to upload files such as PDFs during your interactions with ChatGPT.

For additional assistance, refer to the [YouTube usage guide](#).

## Download

- Executable files for different operating systems can be downloaded from the [Releases](https://github.com/AITwinMinds/ChatGPT-UI/releases) page.

  - 💻 **Windows**: [Direct download for Windows (version 4)](https://github.com/AITwinMinds/ChatGPT-UI/releases/download/v4.0/ChatGPT-UI-Windows.exe)
  - 🍏 **macOS**: [Direct download for macOS (version 3)](https://github.com/AITwinMinds/ChatGPT-UI/releases/download/v3.0/ChatGPT-UI-macOS.app.zip)
  - 🐧 **Linux**: [Direct download for Linux (version 3)](https://github.com/AITwinMinds/ChatGPT-UI/releases/download/v3.0/ChatGPT-UI-Linux)

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

![Windows_theme](https://github.com/AITwinMinds/ChatGPT-UI/assets/127874551/d1dd88e0-dfc3-47f9-8b96-3a75ff8f0db6)
   
## Video Guide on YouTube

Learn how to use the ChatGPT Interface effectively by watching our video guide on YouTube. The guide will cover topics such as prompt selection, language translation, clipboard integration, and more.

[Subscribe to our YouTube Channel](https://www.youtube.com/@AITwinMinds) for the latest updates and tutorials on ChatGPT Interface.

[![](https://github.com/AITwinMinds/ChatGPT-UI/assets/127874551/9af9d5e0-f79f-443d-a8a2-0697f51898ac)](#)

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
