<h1 align="left">ChatGPT Interface</h1>

<img align="right" width="100" height="100" src="https://github.com/I-A-Team/ChatGPT-UI/blob/main/icon.png" alt="ChatGPT Interface">

<!-- Rest of your README content goes here -->


This repository contains a graphical user interface (GUI) for seamless interaction with OpenAI's GPT-3.5 Turbo model using the ChatGPT API. The interface, built using PyQt5, offers an intuitive and feature-rich environment for generating responses, rephrasing text, debugging code, summarizing content, translating languages, and more.

## Features

- **User-Friendly Interface**: Enjoy a clean and intuitive interface for easy prompt input and response viewing.

- **Prompt Options**: Select from various prompt options such as rephrase, debug code, summarize, translate, reply to email, explain, and manual prompts.

- **Language Translation**: Translate text from one language to another using the language dropdowns.

- **Code Highlighting**: Code blocks in the output are highlighted for better readability.

- **Clipboard Integration**: Easily apply text from the clipboard as a prompt with a single checkbox.

- **HTTP Proxy Support**: Enable an HTTP proxy for communication with the ChatGPT API.

## Usage

1. **API Key Setup**: Obtain an API key from OpenAI and enter it in the provided field. Click "Fix/Unfix API Key" to toggle the fix/unfix status.

2. **Prompt Selection**: Choose the type of prompt you want to generate by selecting the appropriate radio button.

3. **Language Translation**: If translating, select the source and target languages from the dropdowns.

4. **Clipboard Option**: Use the last clipboard text as a prompt with a single checkbox.

5. **Input Text**: Enter the prompt manually or input text for manual prompts or code debugging.

6. **HTTP Proxy**: Enable the HTTP proxy option and configure the proxy server and port if necessary.

7. **Generate Response**: Click the "Generate" button to generate a response based on the selected options.

8. **Stop Process**: Click the "Stop" button to halt the response generation process.

## Clipboard Integration

- **Clipboard Option**: By checking the "Use last clipboard text" checkbox, you can easily apply the text from your clipboard as part of the prompt. This provides a quick way to incorporate external content into your queries.

## Dependencies

- PyQt5
- httpx
- openai
- bs4 (Beautiful Soup)
- pygments

## Download

- Executable file for Windows can be downloaded from the [Releases](https://github.com/I-A-Team/ChatGPT-UI/releases) page.

## Configuration

- **API Key**: Enter your OpenAI API key in the provided field. Toggle the fix/unfix status as needed.

- **Proxy Settings**: Configure HTTP proxy settings if required.

- **Language Preferences**: Set default source and target languages for translation.

## Video Guide on YouTube

Learn how to use the ChatGPT Interface effectively by watching our video guide on YouTube. The guide covers topics such as prompt selection, language translation, clipboard integration, and more. 

[![ChatGPT Interface YouTube Guide](path/to/your/youtube-thumbnail.png)](https://www.youtube.com/watch?v=yourvideoid)

## Contributions

Contributions are welcome! Feel free to open issues or submit pull requests to improve the functionality or fix any issues.

## License

This project is licensed under the [GNU General Public License v3.0](LICENSE).

## Contact

For any inquiries, please contact us at [AITwinMinds@gmail.com](mailto:AITwinMinds@gmail.com).
