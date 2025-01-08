# ONIO - AI Agent Framework V2

[![license](https://img.shields.io/packagist/l/doctrine/orm.svg)](https://github.com/QuickAI-Solutions/QuickAI-agent-trading?tab=MIT-1-ov-file)
[![dep1](https://img.shields.io/badge/implementation-tensorflow-orange.svg)](https://www.tensorflow.org/)
[![dep2](https://img.shields.io/badge/python-3.10-red.svg)](https://www.python.org/download/releases/2.7/)
[![dep3](https://img.shields.io/badge/status-in%20progress-green.svg)](https://github.com/QuickAI-Solutions/QuickAI-agent-trading)
[![dep4](https://img.shields.io/badge/docker%20image-available-ff69b4.svg)](https://hub.docker.com/layers/site24x7/docker-agent/release1990/images/sha256-66aa35f69df70b910a2813dc90f9cba2fbc4126e4eac68851f9c96c377901dbb)

**ONIO** is an open-source framework for building customizable AI agents. It allows developers to create agents with distinct personalities, execute specific tasks, and integrate external services. Built on top of OpenAI's GPT models, ONIO empowers you to create intelligent agents for various use cases such as chatbots, virtual assistants, task automation, and social media integrations like Telegram and Discord.

---

## 🧠 **Concept**

ONIO is designed to simplify the creation of AI agents that can interact with users and perform specific functions. It provides a flexible environment to define agent personalities, set tasks, and define responses based on input. Powered by GPT models, ONIO allows you to build agents that are interactive, intelligent, and can adapt to different scenarios.

### **Core Principles**:
- **Custom Personalities**: You can define your agent’s personality, voice, and behavior to make it unique.
- **Task-based Interactions**: Agents can perform specific tasks like greetings, jokes, calculations, and more.
- **OpenAI GPT Integration**: Built on top of OpenAI’s GPT models, making agents capable of understanding complex conversations and generating dynamic responses.
- **Social Media Integration**: Extend your agent's reach by integrating it with messaging platforms like **Telegram** and **Discord**.

---

## 🌟 **Features**

- **Customizable Agent Personalities**: Modify tone, behavior, and response style for personalized agents.
- **Task Management**: Define a list of tasks and have agents respond to specific user requests.
- **Multilingual Support**: Agents can interact with users in different languages.
- **API Integration**: Extend the functionality of your agents by connecting them to external services or APIs.
- **Flexible Configuration**: Simple JSON-based configuration allows for quick customization and updates.
- **Scalable Architecture**: The framework is designed to support a wide variety of agents, from basic ones to more complex, multi-functional agents.
- **Telegram Integration**: Create agents that can respond to messages on Telegram, send updates, and perform tasks within Telegram chats.
- **Discord Integration**: Build agents that interact with Discord users, send messages, and respond to commands in Discord servers.

---

## 🧑‍🤝‍🧑 **Telegram Agent**

The **Telegram Agent** functionality allows you to create an agent that interacts with users via Telegram. It can send and receive messages, respond to user commands, and integrate with Telegram bots for more interactive experiences.

### **Features**:
- Responds to messages sent to your Telegram bot.
- Can handle simple text messages and predefined commands (e.g., /hello, /joke).
- Supports interactive replies and tasks defined in your `config.json`.
- Customizable for specific Telegram groups or channels.

### **How It Works**:
1. **Create a Telegram Bot**: Set up a bot using the [BotFather](https://core.telegram.org/bots#botfather) on Telegram.
2. **Configure Telegram Integration**: Add your bot’s API token to the `telegram_config.json` file.
3. **Interact**: Once configured, your agent will start responding to messages in your Telegram bot, performing tasks like sending jokes, answering questions, and more.

---

## 💬 **Discord Agent**

ONIO also provides **Discord Agent** functionality, enabling agents to interact with users in Discord servers. This integration allows your agent to listen for commands, send messages to channels, and respond to user queries within Discord.

### **Features**:
- Responds to commands and messages from Discord users.
- Supports interactive features like posting jokes, providing information, and handling specific server-based tasks.
- Can be invited to any Discord server with the correct permissions.
- Works well with both public and private channels.

### **How It Works**:
1. **Create a Discord Bot**: Go to the [Discord Developer Portal](https://discord.com/developers/applications), create a new bot, and copy its token.
2. **Configure Discord Integration**: Add your bot’s token to the `discord_config.json` file.
3. **Invite Bot to Server**: Use the generated OAuth2 URL to invite your bot to a Discord server.
4. **Interact**: Your agent will begin responding to messages in Discord, whether it’s answering questions, handling commands, or providing information.

---

## ⚙️ **Architecture**

ONIO is structured to make building, customizing, and deploying AI agents easy:

1. **Agent Core**: The backbone of the framework, powered by OpenAI’s GPT models.
2. **Task Engine**: Manages the agent's responses and tasks, allowing it to handle predefined actions like sending greetings, jokes, etc.
3. **Social Media Integrations**: Provides easy-to-use configurations for integrating your agent with platforms like Telegram and Discord.
4. **Configuration Files**: `settings.json`, `telegram_config.json`, and `discord_config.json` control the agent’s behavior, personality, and platform-specific settings.
5. **Extensibility**: ONIO is designed to be easily extensible. You can add more tasks, integrate third-party APIs, and modify the agent's behavior as needed.

---

## 🌍 **Supported Use Cases**

ONIO can be used to build a wide range of AI-driven applications, including:

- **Chatbots**: Intelligent chatbots that can interact with users in natural language.
- **Virtual Assistants**: Personal assistants that can perform tasks, answer questions, and automate actions.
- **Customer Support**: AI agents that assist with customer service tasks, provide information, and resolve common queries.
- **Entertainment**: Fun and engaging agents that tell jokes, provide trivia, or just have a friendly conversation.
- **Productivity Tools**: Agents that help automate workflows, schedule tasks, or provide reminders.
- **Telegram & Discord Bots**: Create bots that can integrate with popular messaging platforms to interact with users in real-time.

---

## 🚀 **Technologies Used**

- **Python**: The framework is written in Python, making it easy to install, modify, and extend.
- **OpenAI GPT**: The underlying language model that powers ONIO's agents.
- **Telegram API**: For integrating the agent with Telegram bots.
- **Discord API**: For interacting with users in Discord servers.
- **Flask**: For running the agent as a web service, if required for more complex integrations.

---

## 🎨 **Customization**

ONIO is designed to be highly customizable, with options for:

- **Personality Customization**: Set how the agent responds, its tone, and style.
- **Task Definition**: Define specific tasks for the agent to execute, and customize how the agent handles user input.
- **Social Media Integration**: Easily connect your agent to Telegram, Discord, or other messaging platforms.
- **External API Integration**: Use external APIs to enhance agent capabilities (e.g., fetch weather data, interact with social media, etc.).
- **Multilingual Support**: Add multiple languages to your agent and let it communicate in the language of your choice.

---

## 🧑‍🤝‍🧑 **Contributing**

We welcome contributions to improve ONIO. Whether you want to fix a bug, add a new feature, or improve documentation, feel free to fork the repository and submit a pull request.

Here’s how you can contribute:
1. Fork the repository.
2. Create a new branch for your changes.
3. Implement your changes and add tests if necessary.
4. Submit a pull request with a detailed description of your changes.

---

## 🎉 **Get Involved!**

Whether you're a developer looking to create custom AI agents or just someone interested in AI technologies, ONIO provides the tools and flexibility to bring your vision to life. Start building today and create powerful, intelligent agents with ONIO!

---

🎉 **Happy Coding!**

Official Twitter: https://x.com/onio_AItech
