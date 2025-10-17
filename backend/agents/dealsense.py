from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
from typing import List
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

class DealScore(BaseModel):
    """Model for a scored deal"""
    deal_id: str = Field(description="Unique deal identifier")
    company_name: str = Field(description="Company name")
    deal_value: float = Field(description="Deal value in dollars")
    close_probability: float = Field(description="Probability of closing (0-100)")
    risk_level: str = Field(description="Risk level: Low, Medium, High")
    reasoning: str = Field(description="AI reasoning for the score")
    next_actions: List[str] = Field(description="Recommended next actions")

class DealSenseAgent:
    def __init__(self):
        self.llm = ChatOpenAI(
            model="gpt-4o-mini",  # Use gpt-4o-mini for cost efficiency
            temperature=0.3
        )
        self.parser = PydanticOutputParser(pydantic_object=DealScore)
        
    def analyze_deal(self, deal_data: dict) -> DealScore:
        """Analyze a single deal and return scoring"""
        
        prompt = ChatPromptTemplate.from_template(
            """You are an AI sales analyst. Analyze this deal and provide scoring.

Deal Information:
- Company: {company_name}
- Deal Value: ${deal_value}
- Stage: {stage}
- Days in Pipeline: {days_in_pipeline}
- Last Contact: {last_contact_days} days ago
- Decision Maker Engaged: {decision_maker_engaged}
- Competitor: {has_competitor}
- Budget Confirmed: {budget_confirmed}

Analyze this deal and provide:
1. Close probability (0-100)
2. Risk level (Low/Medium/High)
3. Reasoning for your assessment
4. 3 specific next actions

Regarding your reasoning and "3 specific next actions" responses, respond in simple, to the point, laymans terms, and like you are a friend and fellow sales colleauge speaking to the user in a bar after work.

{format_instructions}
"""
        )
        
        chain = prompt | self.llm | self.parser
        
        result = chain.invoke({
            **deal_data,
            "format_instructions": self.parser.get_format_instructions()
        })
        
        return result
    
    def analyze_pipeline(self, deals_df: pd.DataFrame) -> List[DealScore]:
        """Analyze entire pipeline"""
        results = []
        
        for _, deal in deals_df.iterrows():
            deal_dict = deal.to_dict()
            score = self.analyze_deal(deal_dict)
            results.append(score)
        
        return results
    
    def get_risk_deals(self, scored_deals: List[DealScore]) -> List[DealScore]:
        """Filter deals with high risk"""
        return [d for d in scored_deals if d.risk_level == "High"]