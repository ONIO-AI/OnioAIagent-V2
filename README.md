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
- **Flexible Configuration**: Simple.py-based configuration allows for quick customization and updates.
- **Scalable Architecture**: The framework is designed to support a wide variety of agents, from basic ones to more complex, multi-functional agents.
- **Telegram Integration**: Create agents that can respond to messages on Telegram, send updates, and perform tasks within Telegram chats.
- **Discord Integration**: Build agents that interact with Discord users, send messages, and respond to commands in Discord servers.

---

## 🧑‍🤝‍🧑 **Telegram Agent**

The **Telegram Agent** functionality allows you to create an agent that interacts with users via Telegram. It can send and receive messages, respond to user commands, and integrate with Telegram bots for more interactive experiences.

### **Features**:
- Responds to messages sent to your Telegram bot.
- Can handle simple text messages and predefined commands (e.g., /hello, /joke).
- Supports interactive replies and tasks defined in your `config.py`.
- Customizable for specific Telegram groups or channels.

### **How It Works**:
1. **Create a Telegram Bot**: Set up a bot using the [BotFather](https://core.telegram.org/bots#botfather) on Telegram.
2. **Configure Telegram Integration**: Add your bot’s API token to the `telegram_config.py` file.
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
2. **Configure Discord Integration**: Add your bot’s token to the `discord_config.py` file.
3. **Invite Bot to Server**: Use the generated OAuth2 URL to invite your bot to a Discord server.
4. **Interact**: Your agent will begin responding to messages in Discord, whether it’s answering questions, handling commands, or providing information.

---

## ⚙️ **Architecture**

ONIO is structured to make building, customizing, and deploying AI agents easy:

1. **Agent Core**: The backbone of the framework, powered by OpenAI’s GPT models.
2. **Task Engine**: Manages the agent's responses and tasks, allowing it to handle predefined actions like sending greetings, jokes, etc.
3. **Social Media Integrations**: Provides easy-to-use configurations for integrating your agent with platforms like Telegram and Discord.
4. **Configuration Files**: `settings.py`, `telegram_config.py`, and `discord_config.py` control the agent’s behavior, personality, and platform-specific settings.
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

1. **Clone the Repository**

```bash
git clone https://github.com/onio-ai/onio.git
```

2. **Set Up Python Environment**

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows
.\venv\Scripts\activate
# On Unix or MacOS
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

3. **Configure Environment Variables**

```bash
# Copy example environment file
cp .env.example .env

# Edit .env file with your configurations
nano .env  # or use your preferred editor
```

4. **Initialize Project Structure**
```bash
# Create necessary directories
mkdir -p logs data models
mkdir -p config/platform_configs
```

5. **Start the Application**
```bash
# Development mode
python main.py

# Or with specific config
python main.py --config=config/config.py
```

### Production Deployment

1. **System Preparation**

```bash
# Update system packages
sudo apt-get update
sudo apt-get upgrade

# Install required system packages
sudo apt-get install python3.10 python3.10-venv python3-pip
sudo apt-get install redis-server postgresql
```

2. **Database Setup**
```bash
# Create PostgreSQL database
sudo -u postgres psql

postgres=# CREATE DATABASE onio_db;
postgres=# CREATE USER onio_user WITH PASSWORD 'your_password';
postgres=# GRANT ALL PRIVILEGES ON DATABASE onio_db TO onio_user;
postgres=# \q
```

3. **Application Setup**
```bash
# Create application directory
sudo mkdir /opt/onio
sudo chown $USER:$USER /opt/onio

# Clone repository
git clone https://github.com/your-repo/onio.git /opt/onio
cd /opt/onio

# Setup virtual environment
python3.10 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

4. **Production Configuration**
```bash
# Copy and edit production environment file
cp .env.example .env.production
nano .env.production

# Set production configurations
export ENVIRONMENT=production
export APP_ENV=production
```

5. **Setup Systemd Service**
```bash
# Create service file
sudo nano /etc/systemd/system/onio.service
```

Add the following content:
```ini
[Unit]
Description=ONIO AI Agent Service
After=network.target

[Service]
User=your_user
Group=your_group
WorkingDirectory=/opt/onio
Environment="PATH=/opt/onio/venv/bin"
EnvironmentFile=/opt/onio/.env.production
ExecStart=/opt/onio/venv/bin/python main.py
Restart=always

[Install]
WantedBy=multi-user.target
```

6. **Start the Service**
```bash
# Reload systemd
sudo systemctl daemon-reload

# Start service
sudo systemctl start onio

# Enable on boot
sudo systemctl enable onio

# Check status
sudo systemctl status onio
```

### Docker Deployment

1. **Prepare Docker Environment**
```bash
# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/download/v2.20.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

2. **Create Docker Configuration**

Create `Dockerfile`:
```dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "main.py"]
```

Create `docker-compose.yml`:
```yaml
version: '3.8'

services:
  onio:
    build: .
    env_file: .env.production
    volumes:
      - ./logs:/app/logs
      - ./data:/app/data
    depends_on:
      - redis
      - postgres

  redis:
    image: redis:alpine
    volumes:
      - redis_data:/data

  postgres:
    image: postgres:13
    environment:
      POSTGRES_DB: onio_db
      POSTGRES_USER: onio_user
      POSTGRES_PASSWORD: your_password
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  redis_data:
  postgres_data:
```

3. **Build and Run with Docker**
```bash
# Build images
docker-compose build

# Start services
docker-compose up -d

# Check logs
docker-compose logs -f onio
```

4. **Docker Production Considerations**
```bash
# Set up Docker Swarm (for orchestration)
docker swarm init

# Deploy stack
docker stack deploy -c docker-compose.yml onio

# Scale services
docker service scale onio_app=3
```

🎉 **Happy Coding!**

Official Twitter: https://x.com/onio_AItech
