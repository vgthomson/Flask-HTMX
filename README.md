# HTMX Task Manager

A lightweight task management application built using HTMX, Flask, and SQLite that demonstrates the power of hypermedia-driven architecture.

## ✨ Features

- Create, read, update, and delete tasks with real-time UI updates
- Mark tasks as complete with visual state changes
- Filter tasks by status (All, Active, Completed)
- Responsive design that works across devices
- No complex JavaScript or build tools required
- Blazing fast performance with minimal client-side footprint

## 🚀 Live Demo

Check out the live demo: [HTMX Task Manager Demo](https://your-demo-url.com)

## 🛠️ Tech Stack

- **Frontend**: HTMX, HTML, CSS
- **Backend**: Flask (Python)
- **Database**: SQLite
- **Deployment**: (Your deployment platform)

## 🧩 How It Works

This application showcases HTMX's ability to create dynamic, interactive web applications with minimal JavaScript. Key implementation details:

- Server-rendered HTML templates with Flask
- AJAX requests via HTMX attributes
- Real-time DOM updates through HTML fragments
- CSS transitions for smooth UI feedback
- Progressive enhancement approach

## 🔧 Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/htmx-task-manager.git
   cd htmx-task-manager
   ```

2. Create and activate a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Initialize the database:
   ```
   python init_db.py
   ```

5. Start the development server:
   ```
   python app.py
   ```

6. Open your browser and navigate to `http://localhost:5000`

## 📝 Project Structure

```
htmx-task-manager/
├── app.py              # Flask application entry point
├── init_db.py          # Database initialization script
├── models.py           # SQLite database models
├── static/             # Static assets
│   ├── css/            # Stylesheets
│   └── img/            # Images
├── templates/          # HTML templates
│   ├── base.html       # Base template with HTMX inclusion
│   ├── index.html      # Main application page
│   └── partials/       # HTML fragments for HTMX swapping
│       ├── task.html   # Single task component
│       └── task_list.html # List of tasks component
└── requirements.txt    # Python dependencies
```

## 🔄 Key HTMX Patterns Used

- `hx-post` for creating new tasks
- `hx-put` for updating existing tasks
- `hx-delete` for removing tasks
- `hx-trigger` for various user interactions
- `hx-target` for specifying DOM update locations
- `hx-swap` for controlling how content is inserted

## 🤔 Why HTMX?

HTMX offers several advantages for this type of application:

- **Simplicity**: Clean, declarative HTML attributes instead of complex JavaScript
- **Performance**: Small payload sizes and targeted DOM updates
- **Developer Experience**: Easier to maintain and understand
- **SEO-friendly**: Server-rendered content with progressive enhancement
- **Accessibility**: Built on native HTML patterns

## 📚 HTMX Resources

- [Official HTMX Documentation](https://htmx.org/docs/)
- [HTMX Examples](https://htmx.org/examples/)
- [HTMX Discord Community](https://htmx.org/discord)

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgements

- [HTMX](https://htmx.org/) - For making hypermedia-driven applications accessible
- [Flask](https://flask.palletsprojects.com/) - For the lightweight Python web framework
- [SQLite](https://www.sqlite.org/) - For the embedded database

## 👤 Author

Your Name - [@your_twitter](https://twitter.com/your_twitter) - your.email@example.com

Project Link: [https://github.com/yourusername/htmx-task-manager](https://github.com/yourusername/htmx-task-manager)
