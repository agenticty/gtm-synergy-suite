from crewai import Agent, Task, Crew, Process
from langchain_openai import ChatOpenAI
from typing import List, Dict, Optional
from pydantic import BaseModel
import json

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
            model="gpt-4o-mini",
            temperature=0.7
        )
        
    def create_research_agent(self) -> Agent:
        """Agent that researches the prospect"""
        return Agent(
            role="Prospect Researcher",
            goal="Gather and analyze information about the prospect company to identify key pain points and opportunities",
            backstory="""You are an expert B2B researcher with deep knowledge of GTM operations.
            You excel at identifying company pain points, understanding their tech stack,
            and finding relevant case studies and social proof.""",
            llm=self.llm,
            verbose=False,
            allow_delegation=False
        )
    
    def create_copywriter_agent(self) -> Agent:
        """Agent that writes personalized outreach"""
        return Agent(
            role="Senior Outreach Copywriter",
            goal="Write compelling, personalized outreach messages that book discovery calls",
            backstory="""You are a world-class B2B copywriter specializing in cold outreach.
            Your messages are personal, concise, and value-focused. You know how to hook
            readers in the first line and make them want to respond. You avoid buzzwords
            and write like a human, not a sales robot.""",
            llm=self.llm,
            verbose=False,
            allow_delegation=False
        )
    
    def create_reviewer_agent(self) -> Agent:
        """Agent that reviews and scores outreach quality"""
        return Agent(
            role="Outreach Quality Reviewer",
            goal="Review outreach messages for quality, personalization, and effectiveness",
            backstory="""You are a seasoned sales leader who has reviewed thousands of
            outreach emails. You know what works and what doesn't. You provide honest
            feedback on personalization, clarity, and call-to-action strength.""",
            llm=self.llm,
            verbose=False,
            allow_delegation=False
        )
    
    def generate_outreach(self, request: OutreachRequest) -> OutreachResult:
        """Generate personalized outreach using multi-agent workflow"""
        
        # Create agents
        researcher = self.create_research_agent()
        copywriter = self.create_copywriter_agent()
        reviewer = self.create_reviewer_agent()
        
        # Define tasks
        research_task = Task(
            description=f"""Research {request.company_name} ({request.industry}, {request.company_size} employees).
            
            Focus on:
            1. Key pain points: {', '.join(request.pain_points)}
            2. Recent activity: {request.recent_activity or 'None provided'}
            3. Relevant case studies or social proof
            4. Personalization opportunities
            
            Output a structured analysis of what messaging would resonate most.""",
            agent=researcher,
            expected_output="Detailed research findings with personalization opportunities"
        )
        
        dm_context = ""
        if request.decision_maker_name and request.decision_maker_title:
            dm_context = f"to {request.decision_maker_name} ({request.decision_maker_title})"
        
        channel_instructions = self._get_channel_instructions(request.channel)
        
        copywriting_task = Task(
            description=f"""Using the research findings, write a personalized {request.channel} outreach {dm_context}.
            
            {channel_instructions}
            
            Key requirements:
            1. Hook them in the first sentence with relevant insight
            2. Reference their specific pain points
            3. Keep it concise (under 150 words for email)
            4. Clear call-to-action (book 15-min call)
            5. Natural, conversational tone (not salesy)
            6. Include 2-3 specific personalization elements
            
            Also provide:
            - Subject line (if email)
            - Your reasoning for the approach
            - List of personalization elements used
            - Clear call-to-action
            
            Output as JSON with keys: subject, body, reasoning, personalization_elements, call_to_action""",
            agent=copywriter,
            expected_output="Complete outreach message in JSON format",
            context=[research_task]
        )
        
        review_task = Task(
            description=f"""Review the outreach message for quality and effectiveness.
            
            Score on:
            1. Personalization (1-10): How tailored is it?
            2. Clarity (1-10): Is the value proposition clear?
            3. CTA Strength (1-10): How compelling is the call-to-action?
            4. Overall (1-10): Would you respond to this?
            
            Provide:
            - Scores for each criteria
            - Specific improvement suggestions
            - Alternative version if score < 8
            
            Output as JSON with keys: scores, feedback, alternative_version (if needed)""",
            agent=reviewer,
            expected_output="Quality review with scores and feedback in JSON format",
            context=[copywriting_task]
        )
        
        # Create crew and execute
        crew = Crew(
            agents=[researcher, copywriter, reviewer],
            tasks=[research_task, copywriting_task, review_task],
            process=Process.sequential,
            verbose=False
        )
        
        result = crew.kickoff()
        
        # Parse result
        return self._parse_crew_output(result, request.channel)
    
    def _get_channel_instructions(self, channel: str) -> str:
        """Get channel-specific instructions"""
        instructions = {
            "email": """
            EMAIL FORMAT:
            - Subject line: 6-8 words, curiosity-driven
            - Body: 3-4 short paragraphs
            - Include prospect's company name
            - End with single clear CTA
            """,
            "linkedin": """
            LINKEDIN MESSAGE FORMAT:
            - No subject line needed
            - Keep under 100 words (LinkedIn truncates)
            - More casual tone than email
            - Reference something from their LinkedIn profile
            - CTA: "Worth a quick chat?"
            """,
            "slack": """
            SLACK MESSAGE FORMAT:
            - Very casual, conversational tone
            - Under 75 words
            - Use emojis sparingly (1-2 max)
            - CTA: "Have 10 mins to chat?"
            """
        }
        return instructions.get(channel, instructions["email"])
    
    def _parse_crew_output(self, result, channel: str) -> OutreachResult:
        """Parse CrewAI output into structured result"""
        try:
            # Extract JSON from crew output
            output_str = str(result)
            
            # Try to find JSON in the output
            import re
            json_match = re.search(r'\{[\s\S]*\}', output_str)
            
            if json_match:
                data = json.loads(json_match.group())
            else:
                # Fallback parsing
                data = {
                    "subject": "Quick question about your GTM process",
                    "body": output_str[:500],
                    "reasoning": "Generated based on prospect research",
                    "personalization_elements": ["Company name", "Industry"],
                    "call_to_action": "Book 15-min call"
                }
            
            return OutreachResult(
                subject=data.get("subject", ""),
                body=data.get("body", ""),
                reasoning=data.get("reasoning", ""),
                personalization_elements=data.get("personalization_elements", []),
                call_to_action=data.get("call_to_action", "")
            )
            
        except Exception as e:
            # Fallback result
            return OutreachResult(
                subject=f"Quick question about {channel} outreach",
                body="Error generating outreach. Please try again.",
                reasoning=f"Error: {str(e)}",
                personalization_elements=[],
                call_to_action="Book a call"
            )
    
    def generate_multiple_versions(self, request: OutreachRequest, count: int = 3) -> List[OutreachResult]:
        """Generate multiple outreach versions for A/B testing"""
        versions = []
        
        for i in range(count):
            # Slightly modify temperature for variation
            original_temp = self.llm.temperature
            self.llm.temperature = 0.7 + (i * 0.1)
            
            version = self.generate_outreach(request)
            versions.append(version)
            
            self.llm.temperature = original_temp
        
        return versions