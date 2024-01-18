# Our First Intelligent Chatting UI

This project is a simple Python application that interacts with the OpenAI API to generate responses to user input. It features a user interface for inputting questions, displaying responses, and saving conversations.

## [--@STCGoal](STC.md)

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

You will need Python 3.7 or later to run this application. You can download it from the official Python website.

### Installing

1. Clone the repository to your local machine.
2. Navigate to the project directory.
3. Install the required packages using pip:

```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the project directory and add your OpenAI API key:

```bash
OPENAI_API_KEY__our_prototypes_240117=your_api_key_here
```

### Running the Application

To run the application, navigate to the `src` directory and run the `main.py` file:

```bash
python main.py
```

## Usage

The application presents a user interface with a field for entering a question, a submit button for sending the question to the OpenAI API, and a textbox for displaying the response. You can modify the response, copy it to the clipboard, or save it to a file.

## Contributing

Please read `CONTRIBUTING.md` for details on our code of conduct, and the process for submitting pull requests to us.

## License

This project is licensed under the MIT License - see the `LICENSE.md` file for details.