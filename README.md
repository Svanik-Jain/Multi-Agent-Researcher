# Multi-Agent AI Researcher 🤖

An AI-powered research system that uses multiple specialized agents to research topics, analyze information, fact-check claims, extract key metrics, generate visualizations, and produce structured research reports.

Built with **Python, Google Gemini, Tavily Search, and Streamlit**.

## 🚀 Features

- **Web Research:** Searches the web and gathers relevant information using Tavily.
- **Analysis Agent:** Identifies patterns, trends, insights, opportunities, and risks from collected research.
- **Fact-Checker Agent:** Extracts important claims and independently verifies them against external sources.
- **Visual Insights:** Extracts numerical data and generates charts to make research findings easier to understand.
- **Writer Agent:** Combines research, analysis, and fact-checking into a structured final report.
- **Interactive Dashboard:** Provides a Streamlit interface to view research outputs and visual insights.

## 🏗️ Architecture

The project follows a multi-agent pipeline where each agent performs a specialized task.

```text
                 User Query
                     |
                     v
              Researcher Agent
                     |
                     v
                Analyst Agent
                     |
                     v
             Fact-Checker Agent
                     |
                     v
            Visual Insights Engine
                     |
                     v
                Writer Agent
                     |
                     v
                Final Report
                     |
                     v
               Streamlit UI
```

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| Python | Core development |
| Google Gemini | AI reasoning and content generation |
| Tavily Search | Web research and information retrieval |
| Streamlit | Interactive user interface |
| BeautifulSoup | Webpage content extraction |
| Requests | HTTP requests |
| Python-dotenv | Environment variable management |
| SVG | Chart rendering |

## 📁 Project Structure

```text
Multi-Agent-Researcher/
│
├── agents/
│   ├── researcher.py
│   ├── analyst.py
│   ├── fact_checker.py
│   └── writer.py
│
├── visualizations/
│   ├── data_extractor.py
│   └── charts.py
│
├── main.py
├── app.py
├── config.py
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

## ⚙️ Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/Multi-Agent-Researcher.git
```

```bash
cd Multi-Agent-Researcher
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

Activate it:

**Windows PowerShell**
```powershell
.\venv\Scripts\Activate.ps1
```

**Git Bash**
```bash
source venv/Scripts/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure API keys

Create a `.env` file in the root directory:

```env
GEMINI_API_KEY=your_gemini_api_key
GEMINI_MODEL=the_model_you_are_going_use
TAVILY_API_KEY=your_tavily_api_key
```

Get your API keys:

- [Google AI Studio](https://aistudio.google.com/) — Gemini API
- [Tavily](https://tavily.com/) — Web search API

**Important:** Never commit your `.env` file or expose your API keys publicly.

## ▶️ Running the Project

### Run the research pipeline

```bash
python main.py
```

This executes the multi-agent research workflow and generates the research outputs.

### Launch the Streamlit application

```bash
streamlit run app.py
```

Open the local URL displayed in your terminal to access the dashboard.

### Test visualizations separately

To test charts using an existing `visual_data.json` without running the research pipeline:

```bash
streamlit run test.py
```

## 📄 Generated Outputs

The system generates the following files:

| File | Description |
|---|---|
| `research.md` | Collected research and source references |
| `analysis.md` | Insights, trends, opportunities, and risks |
| `fact_check_output.md` | Verification results for extracted claims |
| `visual_data.json` | Structured numerical and strategic data |
| `final_report.md` | Consolidated research report |

## 🔄 How It Works

1. **Research:** The Researcher Agent searches the web and collects relevant information.
2. **Analysis:** The Analyst Agent processes the collected information to identify meaningful insights.
3. **Fact-Checking:** The Fact-Checker Agent independently verifies important claims.
4. **Visualization:** The Visual Insights Engine extracts metrics and generates charts.
5. **Report Generation:** The Writer Agent combines the outputs into a structured research report.

## 🔮 Future Improvements

- Agent-to-agent communication and coordination.
- Improved source credibility scoring.
- Research quality evaluation.
- More visualization types and interactive charts.
- Export reports to PDF.
- Support for additional LLM providers.
- Research history and report management.

## 👨‍💻 Author

**Svanik**

Built as a hands-on project to explore multi-agent AI systems, automated research, fact-checking, and AI-powered data visualization.

---

⭐ If you find this project interesting, consider giving the repository a star!