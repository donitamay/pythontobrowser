# Python to Browser App 📊

A simple training tool to learn how to use Python to read Excel data, process it, and visualize it in a web browser using Streamlit and Plotly.

## 🎯 Learning Objectives

This project teaches:
- Reading Excel files with Pandas
- Processing data in a DataFrame
- Creating interactive visualizations with Plotly
- Building web apps with Streamlit
- Hot-reloading data when files change

## 📋 Prerequisites

- Python 3.8 or higher installed
- Basic understanding of Python

## 🚀 Getting Started

### 1. Install Dependencies

First, activate the virtual environment and install required packages:

```bash
# Activate virtual environment
# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Run the Application

```bash
streamlit run app.py
```

The app will automatically open in your default web browser at `http://localhost:8501`

### 3. Modify the Data

1. Open `data.xlsx` in Excel or any spreadsheet application
2. Modify the data (Product names or Sales values)
3. Add new rows or change existing ones
4. Save the file
5. Click the **"🔄 Reload Data"** button in the Streamlit app
6. Watch your chart update automatically!

## 📊 Sample Data Structure

The included `data.xlsx` file contains sample sales data:

| Product      | Sales |
|--------------|-------|
| Laptops      | 45000 |
| Smartphones  | 67000 |
| Tablets      | 32000 |
| Monitors     | 28000 |
| Keyboards    | 15000 |
| Mice         | 12000 |
| Headphones   | 23000 |
| Webcams      | 18000 |

## 🔧 Features

- **Automatic Excel Loading**: Reads data from `data.xlsx`
- **Data Preview**: See your data in a table format
- **Interactive Charts**: Bar chart with color themes
- **Column Selection**: Choose which columns to visualize
- **Summary Statistics**: Mean, median, max, and min values
- **Hot Reload**: Update data without restarting the app

## 📁 Project Structure

```
Python to Browser App/
├── app.py              # Main Streamlit application (single file)
├── data.xlsx           # Sample Excel data file
├── requirements.txt    # Python dependencies
├── .gitignore         # Git ignore rules
├── README.md          # This file
└── venv/              # Virtual environment (not tracked in git)
```

## 🎓 Training Exercises

Try these exercises to learn more:

1. **Change the data**: Modify values in `data.xlsx` and reload
2. **Add new categories**: Add more products to the Excel file
3. **Try different colors**: Select different color themes in the app
4. **Modify the title**: Change the chart title in the app
5. **Experiment with columns**: Create a new column in Excel and select it

## 🛠️ Troubleshooting

**App won't start?**
- Make sure the virtual environment is activated
- Verify all dependencies are installed: `pip install -r requirements.txt`

**Excel file not found?**
- Ensure `data.xlsx` is in the same folder as `app.py`

**Chart not updating?**
- Click the "🔄 Reload Data" button after modifying the Excel file
- Make sure you saved the Excel file after making changes

## 🔄 GitHub Setup

To sync this project with GitHub:

1. Initialize git repository:
```bash
git init
git add .
git commit -m "Initial commit: Python to Browser App training tool"
```

2. Create a new repository on GitHub

3. Link and push:
```bash
git remote add origin <your-repo-url>
git branch -M main
git push -u origin main
```

The `.gitignore` file is already configured to exclude:
- Virtual environment (`venv/`)
- Python cache files
- IDE settings
- OS-specific files

## 📚 Technologies Used

- **Streamlit**: Web framework for data apps
- **Pandas**: Data manipulation and analysis
- **Plotly**: Interactive visualization library
- **OpenPyXL**: Excel file reading/writing

## 📝 License

This is a training tool - feel free to modify and share with your team!

## 💡 Next Steps

Once comfortable with this app, try:
- Adding more chart types (line, pie, scatter)
- Processing multiple Excel sheets
- Adding data filtering options
- Creating custom calculations
- Exporting processed data

---

**Happy Learning! 🎉**
