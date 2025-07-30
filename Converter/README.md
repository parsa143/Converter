💱 Advanced Currency Converter
A professional currency exchange tool with a beautiful UI and advanced features

✨ Key Features
🔄 Real-time conversion of 30+ currencies

🌗 Dark/Light theme support with one-click switching

🔄 Reverse conversion with a single button

📅 Auto-updated rates from the European Central Bank (ECB) API

⚡ Offline mode with cached rates when no internet is available

📊 Precise calculations with 6 decimal places

📱 Responsive design that works on all screen sizes

🛠️ Technologies Used
Python 3.10+

Tkinter (for GUI)

Requests (for API calls)

ExchangeRatesAPI.io (for live rates)

🚀 How to Run
Clone the repository:

bash
git clone https://github.com/yourusername/currency-converter.git
Install dependencies:

bash
pip install requests
Run the application:

bash
python currency_converter.py
📈 Conversion Logic
The app uses EUR as the base currency for all conversions:

EUR → Other: Direct rate from API

Other → EUR: 1 / rate

Other → Other: (Target rate) / (Source rate)

🌐 Supported Currencies
Code	Currency
USD	US Dollar
EUR	Euro
GBP	British Pound
IRR	Iranian Rial
JPY	Japanese Yen
...	25+ more
📜 License
MIT License - Free for personal and commercial use

💡 Pro Tip: Press the ↔ Reverse button to quickly swap currencies!

⚠️ Note: Internet connection is required for live rates. The app will use cached rates when offline.

Made with ❤️ using Python 🐍