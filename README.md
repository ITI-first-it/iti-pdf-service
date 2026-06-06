# ITI PDF Generator Service

A Flask API that generates branded ITI Assessment Report PDFs automatically.

## Endpoints

### POST /generate
Generates a PDF report and returns it as base64.

**Request body (JSON):**
```json
{
  "full_name": "Debby Odion",
  "organisation": "I AM WHO I SAY I AM",
  "role_level": "Individual Contributor",
  "submission_date": "June 5, 2026",
  "iti_score": "52",
  "iti_band": "Stabilizing",
  "avs": "75",
  "avs_band": "On Promotion Track",
  "rss": "85",
  "rrs": "15",
  "rrs_band": "Stable",
  "igd": "12",
  "igd_band": "Expansion Phase",
  "sa_avg": "50",
  "vv_avg": "55",
  "co_avg": "35",
  "fa_avg": "37",
  "ab_avg": "75",
  "dp_avg": "40",
  "al_avg": "75",
  "ri_avg": "85",
  "ai_narrative": "Your full AI narrative text here..."
}
```

**Response:**
```json
{
  "success": true,
  "pdf_base64": "base64 encoded PDF...",
  "filename": "ITI_Report_Debby_Odion.pdf"
}
```

### GET /health
Health check endpoint.

## Deployment on Render

1. Push this folder to GitHub
2. Connect GitHub repo to Render
3. Set build command: `pip install -r requirements.txt`
4. Set start command: `gunicorn app:app`
5. Deploy
