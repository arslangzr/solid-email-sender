<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>README - SOLID Email Sender</title>
    <style>
        body { font-family: Arial, sans-serif; line-height: 1.6; padding: 20px; }
        pre { background: #f4f4f4; padding: 10px; border-radius: 5px; overflow-x: auto; }
        code { font-family: monospace; }
        h1, h2, h3 { color: #333; }
    </style>
</head>
<body>
    <h1>📧 SOLID Email Sender</h1>
    <p>A Python project demonstrating the SOLID principles through an email sending service.</p>
    
    <h2>🛠 Features</h2>
    <ul>
        <li>Follows SOLID principles (Single Responsibility, Open/Closed, Liskov, Interface Segregation, Dependency Inversion).</li>
        <li>Supports multiple email sending services (SMTP, MailHog, Mailtrap SMTP & API).</li>
        <li>Uses environment variables for sensitive configurations.</li>
    </ul>

    <h2>📦 Installation</h2>
    <pre><code>git clone https://github.com/yourusername/solid-email-sender.git
cd solid-email-sender
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
pip install -r requirements.txt</code></pre>

    <h2>⚙️ Configuration</h2>
    <p>Create a <code>.env</code> file in the root directory and add the following:</p>
    <pre><code>SMTP_HOST=smtp.example.com
SMTP_PORT=587
SMTP_USERNAME=your_username
SMTP_PASSWORD=your_password
MAILTRAP_API_TOKEN=your_mailtrap_api_token</code></pre>

    <h2>🚀 Usage</h2>
    <pre><code>python main.py</code></pre>
    
    <h2>📜 SOLID Principles in Action</h2>
    <ul>
        <li><strong>Single Responsibility Principle (SRP)</strong>: <code>EmailMessage</code> handles message creation, <code>SMTPService</code> handles sending.</li>
        <li><strong>Open/Closed Principle (OCP)</strong>: New email services can be added without modifying existing code.</li>
        <li><strong>Liskov Substitution Principle (LSP)</strong>: <code>SMTPService</code> and <code>MailtrapAPIService</code> can replace <code>EmailSender</code> without altering behavior.</li>
        <li><strong>Interface Segregation Principle (ISP)</strong>: The <code>EmailSender</code> interface ensures only relevant methods are implemented.</li>
        <li><strong>Dependency Inversion Principle (DIP)</strong>: High-level modules depend on abstractions (<code>EmailSender</code>).</li>
    </ul>

    <h2>📝 License</h2>
    <p>MIT License</p>
</body>
</html>
