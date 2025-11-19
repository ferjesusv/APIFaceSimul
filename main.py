from fastapi import FastAPI
from datetime import date
from random import random
import math

app = FastAPI()

students = {
    "student_01": {
        "campaigns": {
            "CAMP-A": {"ctr": 0.035, "cpm": 2.0, "conv": 0.06},
            "CAMP-B": {"ctr": 0.029, "cpm": 2.2, "conv": 0.04}
        }
    }
}

def generate_insights(campaign_params):
    base_impressions = 1500 + int(random() * 300)   # 1500–1800
    ctr = campaign_params["ctr"] * (0.8 + random()*0.4)
    clicks = int(base_impressions * ctr)

    spend = (base_impressions / 1000) * campaign_params["cpm"]
    conv_rate = campaign_params["conv"]
    conversions = int(clicks * conv_rate)

    return {
        "impressions": base_impressions,
        "clicks": clicks,
        "ctr": round(ctr, 4),
        "spend": round(spend, 2),
        "cpc": round(spend / clicks if clicks > 0 else 0, 3),
        "conversions": conversions,
        "cpa": round(spend / conversions if conversions > 0 else 0, 2)
    }

@app.get("/students/{student_id}/campaigns")
def list_campaigns(student_id: str):
    return students.get(student_id, {})

@app.get("/students/{student_id}/campaigns/{campaign_id}/insights")
def get_insights(student_id: str, campaign_id: str, date: str):
    campaign = students[student_id]["campaigns"][campaign_id]
    insights = generate_insights(campaign)
    return {"campaign_id": campaign_id, "date": date, **insights}
