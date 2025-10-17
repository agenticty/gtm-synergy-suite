from crewai import Agent, Task, Crew, Process
from langchain_openai import ChatOpenAI
from typing import List, Dict, Optional
from pydantic import BaseModel
import json
import re
from dotenv import load_dotenv
load_dotenv()

class OutreachRequest(BaseModel):
    company_name: str
    industry: str
    company_size: str
    pain_points: List[str]
    decision_maker_name: Optional[str] = None
    decision_maker_title: Optional[str] = None
    recent_activity: Optional[str] = None
    channel: str = "email"  # email, linkedin, slack

class OutreachResult(BaseModel):
    subject: str
    body: str
    reasoning: str
    personalization_elements: List[str]
    call_to_action: str
    alternative_versions: Optional[List[Dict]] = None

class OutreachAIAgent:
    def __init__(self):
        self.llm = ChatOpenAI(
            model="gpt-4o",
            temperature=0.7
        )
    
    def generate_outreach(self, request: OutreachRequest) -> OutreachResult:
        """Generate personalized outreach - SIMPLIFIED VERSION"""
        
        # Build the prompt directly
        dm_info = ""
        if request.decision_maker_name and request.decision_maker_title:
            dm_info = f" to {request.decision_maker_name} ({request.decision_maker_title})"
        
        pain_points_str = ", ".join(request.pain_points)
        
        channel_guide = {
            "email": "Write a professional email with subject line. Keep body under 150 words.",
            "linkedin": "Write a LinkedIn connection message. No subject needed. Keep under 100 words. Casual tone.",
            "slack": "Write a casual Slack message. No subject needed. Under 75 words. Use 1-2 emojis max."
        }
        
        prompt = f"""You are writing a personalized {request.channel} outreach message{dm_info}.

PROSPECT INFO:
- Company: {request.company_name}
- Industry: {request.industry}
- Size: {request.company_size} employees
- Pain Points: {pain_points_str}
- Recent Activity: {request.recent_activity or "None"}

{channel_guide.get(request.channel, channel_guide['email'])}

REQUIREMENTS:
1. Hook them in the first sentence with a relevant insight about their industry or pain point
2. Keep it conversational and human (not salesy)
3. Reference their specific pain points
4. Clear call-to-action: book a 15-min discovery call
5. Include 2-3 personalization elements (company name, industry, specific pain point)

OUTPUT FORMAT (respond ONLY with valid JSON):
{{
  "subject": "subject line here" (if email, otherwise empty string),
  "body": "full message body here",
  "reasoning": "why you chose this approach",
  "personalization_elements": ["element1", "element2", "element3"],
  "call_to_action": "the specific CTA you used"
}}
"""
        
        # Get response from LLM
        from langchain.schema import HumanMessage
        response = self.llm.invoke([HumanMessage(content=prompt)])
        
        # Parse the response
        return self._parse_llm_response(response.content, request.channel)
    
    def _parse_llm_response(self, response_text: str, channel: str) -> OutreachResult:
        """Parse LLM response into OutreachResult"""
        try:
            # Try to extract JSON from response
            json_match = re.search(r'\{[\s\S]*\}', response_text)
            
            if json_match:
                data = json.loads(json_match.group())
                
                return OutreachResult(
                    subject=data.get("subject", ""),
                    body=data.get("body", ""),
                    reasoning=data.get("reasoning", ""),
                    personalization_elements=data.get("personalization_elements", []),
                    call_to_action=data.get("call_to_action", "")
                )
            else:
                # Fallback: use the raw text as body
                return OutreachResult(
                    subject="Quick question" if channel == "email" else "",
                    body=response_text,
                    reasoning="Direct LLM output",
                    personalization_elements=["Company mentioned"],
                    call_to_action="Book a call"
                )
                
        except Exception as e:
            print(f"Parse error: {e}")
            # Return minimal valid result
            return OutreachResult(
                subject="Quick question" if channel == "email" else "",
                body=response_text[:500] if response_text else "Error generating outreach",
                reasoning=f"Parsing failed: {str(e)}",
                personalization_elements=[],
                call_to_action="Let's connect"
            )