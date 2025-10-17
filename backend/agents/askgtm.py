from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain.docstore.document import Document
from typing import List, Dict, Optional
import os
from pathlib import Path
import json
from dotenv import load_dotenv
load_dotenv()

class AskGTMAgent:
    def __init__(self, persist_directory: str = "./chroma_db"):
        self.llm = ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0.2
        )
        self.embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
        self.persist_directory = persist_directory
        self.vectorstore = None
        self.conversation_chain = None
        self.chat_history = []
        
        # Initialize or load existing vectorstore
        self._initialize_vectorstore()
    
    def _initialize_vectorstore(self):
        """Initialize ChromaDB vectorstore"""
        if os.path.exists(self.persist_directory):
            # Load existing vectorstore
            self.vectorstore = Chroma(
                persist_directory=self.persist_directory,
                embedding_function=self.embeddings
            )
        else:
            # Create new vectorstore with sample docs
            self.vectorstore = Chroma(
                persist_directory=self.persist_directory,
                embedding_function=self.embeddings
            )
            self._add_sample_documents()
    
    def _add_sample_documents(self):
        """Add sample GTM knowledge documents"""
        sample_docs = [
            {
                "content": """
                Product Pricing Tiers:
                - Starter: $49/month - Up to 5 users, basic features
                - Professional: $149/month - Up to 20 users, advanced features, priority support
                - Enterprise: Custom pricing - Unlimited users, full features, dedicated CSM
                
                All plans include: 24/7 support, 99.9% uptime SLA, data encryption
                """,
                "metadata": {"source": "pricing", "category": "sales"}
            },
            {
                "content": """
                Ideal Customer Profile (ICP):
                - Company size: 50-500 employees
                - Industry: SaaS, Technology, Professional Services
                - Revenue: $5M-$50M ARR
                - Tech stack: Uses Salesforce, Slack, modern CRM
                - Pain points: Manual GTM processes, poor pipeline visibility
                - Decision makers: VP Sales, CRO, Head of Revenue Operations
                """,
                "metadata": {"source": "icp", "category": "sales"}
            },
            {
                "content": """
                Common Objections & Responses:
                
                1. "Too expensive"
                   Response: Focus on ROI - our customers see 80% reduction in manual work,
                   saving 10+ hours per week per rep. That's $50k+ in productivity annually.
                
                2. "We already have tools"
                   Response: Our platform integrates with existing tools and adds AI orchestration
                   layer that your current stack lacks. Most customers keep their CRM and add us.
                
                3. "Implementation seems complex"
                   Response: Average onboarding is 2 weeks. We provide dedicated implementation
                   support and most teams see value within first month.
                """,
                "metadata": {"source": "objections", "category": "sales"}
            },
            {
                "content": """
                Competitor Comparison:
                
                vs. Clari:
                - We're 40% cheaper
                - Better AI agent orchestration
                - Faster implementation (2 weeks vs 2 months)
                
                vs. Gong:
                - We focus on automation, they focus on conversation intelligence
                - Complementary products - many customers use both
                - Our AI agents actually take actions, not just insights
                """,
                "metadata": {"source": "competitive", "category": "sales"}
            },
            {
                "content": """
                Product Features:
                
                Core Features:
                - AI-powered pipeline forecasting with 90%+ accuracy
                - Automated lead scoring and qualification
                - Multi-channel engagement automation
                - RAG-powered knowledge base for instant answers
                - CRM integration (Salesforce, HubSpot)
                - Slack/Teams integration
                
                Differentiators:
                - Agentic AI (not just analytics)
                - Multi-agent orchestration
                - Real-time buying signal detection
                - Customizable agent workflows
                """,
                "metadata": {"source": "features", "category": "product"}
            },
            {
                "content": """
                Case Studies:
                
                TechStart Inc (Series B SaaS):
                - Challenge: Sales team spending 60% time on manual research
                - Solution: Implemented our AI agent platform
                - Results: 80% reduction in manual work, 35% increase in pipeline,
                  deal cycles reduced from 90 to 60 days
                
                Global Solutions (Professional Services):
                - Challenge: Inconsistent lead qualification, low conversion
                - Solution: AI-powered lead scoring and automation
                - Results: Lead-to-opportunity conversion improved from 12% to 31%,
                  sales team productivity up 45%
                """,
                "metadata": {"source": "case-studies", "category": "sales"}
            },
            {
                "content": """
                Implementation Process:
                
                Week 1: Discovery & Setup
                - Kickoff call with CSM
                - CRM integration setup
                - Data migration and sync
                - Agent configuration
                
                Week 2: Training & Launch
                - Team training (2 sessions)
                - Pilot with 5 users
                - Feedback and refinement
                - Full rollout
                
                Week 3-4: Optimization
                - Monitor usage and performance
                - Adjust agent workflows
                - Advanced feature training
                - Success metrics review
                """,
                "metadata": {"source": "implementation", "category": "customer-success"}
            },
            {
                "content": """
                Technical Requirements:
                
                Browser Support:
                - Chrome (recommended)
                - Firefox, Safari, Edge (latest versions)
                
                Integrations:
                - Salesforce (API v52+)
                - HubSpot (Marketing Hub Pro+)
                - Slack (workspace admin required)
                - Microsoft Teams
                
                Security:
                - SOC 2 Type II certified
                - GDPR compliant
                - Data encryption at rest and in transit
                - SSO support (SAML, OAuth)
                """,
                "metadata": {"source": "technical", "category": "product"}
            }
        ]
        
        documents = [
            Document(page_content=doc["content"], metadata=doc["metadata"])
            for doc in sample_docs
        ]
        
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len
        )
        
        splits = text_splitter.split_documents(documents)
        self.vectorstore.add_documents(splits)
        self.vectorstore.persist()
    
    def add_documents(self, texts: List[str], metadatas: Optional[List[dict]] = None):
        """Add new documents to knowledge base"""
        documents = [
            Document(page_content=text, metadata=meta or {})
            for text, meta in zip(texts, metadatas or [{}] * len(texts))
        ]
        
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )
        
        splits = text_splitter.split_documents(documents)
        self.vectorstore.add_documents(splits)
        self.vectorstore.persist()
    
    def setup_conversation_chain(self):
        """Setup conversational retrieval chain"""
        memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True,
            output_key="answer"
        )
        
        self.conversation_chain = ConversationalRetrievalChain.from_llm(
            llm=self.llm,
            retriever=self.vectorstore.as_retriever(
                search_type="similarity",
                search_kwargs={"k": 4}
            ),
            memory=memory,
            return_source_documents=True,
            verbose=False
        )
    
    def ask(self, question: str) -> Dict:
        """Ask a question and get answer with sources"""
        if not self.conversation_chain:
            self.setup_conversation_chain()
        
        result = self.conversation_chain.invoke({"question": question})
        
        # Format response
        response = {
            "answer": result["answer"],
            "sources": [
                {
                    "content": doc.page_content[:200] + "...",
                    "source": doc.metadata.get("source", "unknown"),
                    "category": doc.metadata.get("category", "general")
                }
                for doc in result["source_documents"]
            ]
        }
        
        return response
    
    def reset_conversation(self):
        """Reset conversation history"""
        self.chat_history = []
        self.conversation_chain = None
    
    def get_stats(self) -> Dict:
        """Get knowledge base statistics"""
        return {
            "total_documents": 8,
            "categories": ["sales", "product", "customer-success", "technical"]
        }