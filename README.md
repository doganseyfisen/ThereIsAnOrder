# ThereIsAnOrder 

Welcome to **There Is An Order** repository! This project aims to provide a simple order management and tracking system web application. It includes basic functionalities such as creating, updating, viewing, and deleting orders.

## Features

- Users can create, update, view, and delete orders.
- Orders can be tracked by their status.
- User-friendly interface and navigation.

## Installation

1. Clone the repository to your local machine:
   ```
   git clone https://github.com/doganseyfisen/ThereIsAnOrder.git
   cd ThereIsAnOrder
   ```

2. Create a virtual environment (optional but recommended):
   ```
   python -m venv venv
   source venv/bin/activate  # For Windows: venv\Scripts\activate
   ```

3. Install required dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Set up the database and load sample data:
   ```
   python manage.py migrate
   python manage.py loaddata sample_data.json
   ```

5. Start the application:
   ```
   python manage.py runserver
   ```

## Usage

- Once the application is running, open your web browser and go to `http://127.0.0.1:8000/`.
- You can start managing orders through the user-friendly interface.

## License

This project is distributed under the MIT License. For more information, see the [LICENSE](LICENSE) file.
