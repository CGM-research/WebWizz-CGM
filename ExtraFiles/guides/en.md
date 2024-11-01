# User manual for WebWizz

## Introduction
WebWizz is a web service designed for creating and editing web pages using artificial intelligence. The service provides tools for generating, constructing, and editing HTML code, as well as managing files and configuring settings. WebWizz is open-source on GitHub (License: GNU-GPL 3.0).

# Getting Started

## Main Features

### Navigation Through Pages
In the sidebar, you can select one of the following pages:
- **About us ℹ️**: Information about the project.
- **Account 👤**: Managing your account and files.
- **Settings ⚙️**: Configuring parameters and tokens.
- **Generate ✨**: Generating web pages using AI.
- **Build 🛠️**: Constructing web pages.
- **Edit 👨‍💻**: Editing HTML code.

### Account Page 👤
On this page, you can:
- **Create a new account** or **log in to an existing one**.
- **Upload files** or **add them manually**.
- **View and manage files** saved in your account.

### Settings Page ⚙️
Here you can:
- **Configure your tokens** for HuggingFace and Pixabay. (For better performance)

### Generate Page ✨
This page allows you to:
- **Enter a topic and description** for generating a web page.
- **Generate HTML code** using AI algorithms.
- **Preview and download** the generated code and the page itself.
- **Save the code** to your account.

### Build Page 🛠️
On this page, you can:
- **Add, edit, and delete elements** on the web page.
    - Add text with various customization options. (Color, background, border, etc.)
    - Add images with various customization options. (Size, border, etc.)
    - Create groups of elements.
    - Edit or delete existing elements.
- **Save and download** the finished HTML code.

### Edit Page 👨‍💻
Here you can:
- **Upload an existing HTML file** or **create a blank file**.
- **Edit the code** using the built-in editor. (The editor can be customized by the user using the built-in menu. It also autocompletes the user's code and formats brackets.)
- **Use the AI assistant** for generating and editing the user's code, with the ability to see all changes made.
- **Preview the page** by clicking the run code button.
- **Save and download** the source code of the page.

# Installation and Running (Local build) 

1. **Cloning the Repository**:
   ```bash
   git clone https://github.com/Wafflelover404/WebWizz.git
   cd WebWizz
   ```

2. **Installing Dependencies**:
   ```bash
   pip3 install -r requirements.txt
   ```

3. **Running the Application**:
   ```bash
   python3 -m streamlit run streamlit_app.py
   ```

### Configuring Tokens
For full functionality, WebWizz requires tokens from HuggingFace and Pixabay.

1. **HuggingFace Token**:
   - Go to the [HuggingFace token settings page](https://huggingface.co/settings/tokens).
   - Register and obtain your API key.

2. **Pixabay Token**:
   - Go to the [Pixabay API documentation page](https://pixabay.com/api/docs/).
   - Register and obtain your API key.
