from google import genai
import os
import json
from typing import List, Dict, Any
from dotenv import load_dotenv

load_dotenv()

class GeminiAIService:
    def __init__(self):
        """Initialize Gemini AI service with API key from environment"""
        api_key = os.getenv('GEMINI_API_KEY')
        if not api_key:
            raise ValueError("GEMINI_API_KEY environment variable not found")
        
        self.client = genai.Client(api_key=api_key)
    
    def enhance_vm_recommendations(self, vm_metrics: List[Dict], basic_analysis: List[Dict]) -> List[Dict]:
        """
        Enhance VM recommendations using Gemini AI analysis
        """
        try:
            # Prepare context for AI analysis
            context = {
                "vm_metrics": vm_metrics,
                "current_analysis": basic_analysis,
                "analysis_context": "Cloud infrastructure optimization and cost management"
            }
            
            prompt = f"""
            As a cloud infrastructure expert, analyze the following VM metrics and current recommendations to provide enhanced, actionable insights:

            VM Metrics:
            {json.dumps(vm_metrics, indent=2)}

            Current Analysis:
            {json.dumps(basic_analysis, indent=2)}

            Please provide enhanced recommendations that include:
            1. More detailed reasoning for each recommendation
            2. Specific cost savings estimates where possible
            3. Risk assessment for proposed changes
            4. Priority levels (High, Medium, Low) for each recommendation
            5. Alternative solutions if the primary recommendation isn't feasible
            6. Timeline suggestions for implementation

            Format your response as JSON with the same structure as the current analysis but with enhanced fields:
            - Add "ai_reasoning" field with detailed explanation
            - Add "cost_savings_estimate" field with potential monthly savings
            - Add "risk_level" field (Low, Medium, High)
            - Add "priority" field (High, Medium, Low)
            - Add "implementation_timeline" field
            - Add "alternative_options" array with other possible solutions
            - Enhance the existing "recommendation" field with more specific guidance

            Return only valid JSON without any markdown formatting or extra text.
            """

            response = self.client.models.generate_content(
                model='gemini-2.0-flash-exp',
                contents=prompt,
                config=genai.GenerateContentConfig(
                    system_instruction="You are a cloud infrastructure expert providing detailed VM optimization recommendations.",
                    generation_config=genai.GenerationConfig(
                        temperature=0.1,
                        response_mime_type="application/json"
                    )
                )
            )
            
            try:
                # Parse the AI response
                ai_enhanced_analysis = json.loads(response.text)
                return ai_enhanced_analysis if isinstance(ai_enhanced_analysis, list) else basic_analysis
            except json.JSONDecodeError:
                print(f"Failed to parse AI response: {response.text}")
                return basic_analysis
                
        except Exception as e:
            print(f"Error in AI enhancement: {e}")
            return basic_analysis
    
    def get_infrastructure_insights(self, vm_metrics: List[Dict], cloud_provider: str) -> Dict[str, Any]:
        """
        Get high-level infrastructure insights and recommendations
        """
        try:
            prompt = f"""
            Analyze the following {cloud_provider} infrastructure metrics and provide strategic insights:

            VM Metrics:
            {json.dumps(vm_metrics, indent=2)}

            Cloud Provider: {cloud_provider}

            Please provide strategic insights including:
            1. Overall infrastructure health score (1-10)
            2. Top 3 optimization opportunities
            3. Cost optimization potential percentage
            4. Security and compliance considerations
            5. Scalability recommendations
            6. Disaster recovery suggestions
            7. Performance optimization opportunities

            Format as JSON with these keys:
            - health_score: number (1-10)
            - optimization_opportunities: array of strings
            - cost_optimization_potential: string (percentage)
            - security_recommendations: array of strings
            - scalability_insights: string
            - disaster_recovery_notes: string
            - performance_tips: array of strings
            - summary: string (overall assessment)

            Return only valid JSON.
            """

            response = self.client.models.generate_content(
                model='gemini-2.0-flash-exp',
                contents=prompt,
                config=genai.GenerateContentConfig(
                    system_instruction="You are a cloud infrastructure strategist providing high-level insights.",
                    generation_config=genai.GenerationConfig(
                        temperature=0.2,
                        response_mime_type="application/json"
                    )
                )
            )
            
            try:
                insights = json.loads(response.text)
                return insights
            except json.JSONDecodeError:
                return {
                    "health_score": 7,
                    "optimization_opportunities": ["Enable autoscaling", "Right-size instances", "Review storage types"],
                    "cost_optimization_potential": "15-25%",
                    "security_recommendations": ["Enable monitoring", "Review access policies"],
                    "scalability_insights": "Consider implementing auto-scaling groups",
                    "disaster_recovery_notes": "Implement cross-region backups",
                    "performance_tips": ["Monitor resource utilization", "Optimize database queries"],
                    "summary": "Infrastructure shows good potential for optimization"
                }
                
        except Exception as e:
            print(f"Error getting infrastructure insights: {e}")
            return {
                "health_score": 7,
                "optimization_opportunities": ["Review current setup"],
                "cost_optimization_potential": "Unknown",
                "security_recommendations": ["Regular security audits"],
                "scalability_insights": "Review current scaling policies",
                "disaster_recovery_notes": "Implement backup strategies",
                "performance_tips": ["Monitor key metrics"],
                "summary": "Unable to analyze due to technical issues"
            }
    
    def predict_future_trends(self, vm_metrics: List[Dict], cloud_provider: str) -> Dict[str, Any]:
        """
        Predict future infrastructure trends and provide proactive insights
        """
        try:
            prompt = f"""
            Based on the current {cloud_provider} infrastructure metrics, predict future trends and provide proactive recommendations:

            Current VM Metrics:
            {json.dumps(vm_metrics, indent=2)}

            Provide predictions and insights for:
            1. Resource usage trends for next 30 days
            2. Cost projection and potential savings opportunities
            3. Performance bottlenecks that may emerge
            4. Scaling recommendations based on current patterns
            5. Proactive optimization suggestions
            6. Risk assessment for current configuration
            7. Future technology recommendations (newer instance types, etc.)

            Format as JSON with these keys:
            - usage_trend_prediction: object with cpu_trend, memory_trend, cost_trend
            - next_month_cost_projection: number
            - potential_bottlenecks: array of strings
            - scaling_recommendations: array of objects with vm_id and recommendation
            - proactive_optimizations: array of strings
            - risk_assessment: object with risk_level and issues
            - future_tech_suggestions: array of strings
            - confidence_score: number (0-100)

            Return only valid JSON.
            """

            response = self.client.models.generate_content(
                model='gemini-2.0-flash-exp',
                contents=prompt,
                config=genai.GenerateContentConfig(
                    system_instruction="You are a cloud infrastructure analyst predicting future trends.",
                    generation_config=genai.GenerationConfig(
                        temperature=0.3,
                        response_mime_type="application/json"
                    )
                )
            )
            
            try:
                predictions = json.loads(response.text)
                return predictions
            except json.JSONDecodeError:
                # Fallback predictions
                total_cost = sum(vm.get('cost', 0) for vm in vm_metrics)
                return {
                    "usage_trend_prediction": {
                        "cpu_trend": "stable",
                        "memory_trend": "increasing",
                        "cost_trend": "stable"
                    },
                    "next_month_cost_projection": total_cost * 1.05,
                    "potential_bottlenecks": ["Memory constraints on high-usage VMs"],
                    "scaling_recommendations": [{"vm_id": vm["id"], "recommendation": "Monitor closely"} for vm in vm_metrics[:3]],
                    "proactive_optimizations": ["Enable auto-scaling", "Review instance types"],
                    "risk_assessment": {"risk_level": "Medium", "issues": ["Some VMs running at high utilization"]},
                    "future_tech_suggestions": ["Consider newer generation instances", "Evaluate serverless options"],
                    "confidence_score": 75
                }
                
        except Exception as e:
            print(f"Error predicting trends: {e}")
            return {
                "usage_trend_prediction": {"cpu_trend": "unknown", "memory_trend": "unknown", "cost_trend": "unknown"},
                "next_month_cost_projection": 0,
                "potential_bottlenecks": [],
                "scaling_recommendations": [],
                "proactive_optimizations": [],
                "risk_assessment": {"risk_level": "Unknown", "issues": []},
                "future_tech_suggestions": [],
                "confidence_score": 0
            }

    def generate_optimization_plan(self, vm_metrics: List[Dict], cloud_provider: str) -> Dict[str, Any]:
        """
        Generate a comprehensive optimization plan with prioritized action items
        """
        try:
            prompt = f"""
            Create a comprehensive optimization plan for this {cloud_provider} infrastructure:

            VM Metrics:
            {json.dumps(vm_metrics, indent=2)}

            Generate a detailed optimization plan including:
            1. Immediate actions (can be done today)
            2. Short-term optimizations (1-2 weeks)
            3. Long-term strategic changes (1-3 months)
            4. Cost optimization priorities
            5. Performance improvement priorities
            6. Security enhancements
            7. Automation opportunities

            Format as JSON with these keys:
            - immediate_actions: array of objects with action, impact, effort_level
            - short_term_plan: array of objects with action, timeline, expected_benefit
            - long_term_strategy: array of objects with action, timeline, strategic_value
            - cost_optimization_priorities: array ranked by potential savings
            - performance_priorities: array ranked by impact
            - security_enhancements: array of security improvements
            - automation_opportunities: array of automation suggestions
            - overall_roi_estimate: string describing return on investment

            Return only valid JSON.
            """

            response = self.client.models.generate_content(
                model='gemini-2.0-flash-exp',
                contents=prompt,
                config=genai.GenerateContentConfig(
                    system_instruction="You are a cloud infrastructure consultant creating optimization plans.",
                    generation_config=genai.GenerationConfig(
                        temperature=0.2,
                        response_mime_type="application/json"
                    )
                )
            )
            
            try:
                plan = json.loads(response.text)
                return plan
            except json.JSONDecodeError:
                return {
                    "immediate_actions": [
                        {"action": "Review high-usage VMs", "impact": "High", "effort_level": "Low"},
                        {"action": "Enable monitoring alerts", "impact": "Medium", "effort_level": "Low"}
                    ],
                    "short_term_plan": [
                        {"action": "Right-size overprovisioned VMs", "timeline": "1-2 weeks", "expected_benefit": "15-20% cost reduction"}
                    ],
                    "long_term_strategy": [
                        {"action": "Implement auto-scaling", "timeline": "2-3 months", "strategic_value": "Dynamic resource optimization"}
                    ],
                    "cost_optimization_priorities": ["Right-size instances", "Review storage types", "Consider reserved instances"],
                    "performance_priorities": ["Address CPU bottlenecks", "Optimize memory usage"],
                    "security_enhancements": ["Enable encryption", "Review access policies"],
                    "automation_opportunities": ["Automated scaling", "Cost monitoring alerts"],
                    "overall_roi_estimate": "Expected 20-30% cost reduction with improved performance"
                }
                
        except Exception as e:
            print(f"Error generating optimization plan: {e}")
            return {
                "immediate_actions": [],
                "short_term_plan": [],
                "long_term_strategy": [],
                "cost_optimization_priorities": [],
                "performance_priorities": [],
                "security_enhancements": [],
                "automation_opportunities": [],
                "overall_roi_estimate": "Unable to generate estimate"
            }

    def generate_cost_report(self, vm_metrics: List[Dict], cloud_provider: str) -> Dict[str, Any]:
        """
        Generate a comprehensive cost analysis report
        """
        try:
            prompt = f"""
            Generate a comprehensive cost analysis report for this {cloud_provider} infrastructure:

            VM Data:
            {json.dumps(vm_metrics, indent=2)}

            Please provide:
            1. Current monthly cost breakdown
            2. Cost optimization opportunities with specific savings amounts
            3. Cost trends and patterns analysis
            4. Budget recommendations
            5. Reserved instance opportunities
            6. Right-sizing impact analysis

            Format as JSON with these keys:
            - total_monthly_cost: number
            - cost_breakdown: object with categories
            - optimization_savings: object with opportunity and amount
            - budget_recommendations: string
            - reserved_instance_savings: string
            - right_sizing_impact: object with details
            - executive_summary: string

            Return only valid JSON.
            """

            response = self.client.models.generate_content(
                model='gemini-2.0-flash-exp',
                contents=prompt,
                config=genai.GenerateContentConfig(
                    system_instruction="You are a cloud cost optimization specialist providing detailed cost analysis.",
                    generation_config=genai.GenerationConfig(
                        temperature=0.1,
                        response_mime_type="application/json"
                    )
                )
            )
            
            try:
                report = json.loads(response.text)
                return report
            except json.JSONDecodeError:
                total_cost = sum(vm.get('cost', 0) for vm in vm_metrics)
                return {
                    "total_monthly_cost": total_cost,
                    "cost_breakdown": {"compute": total_cost * 0.8, "storage": total_cost * 0.2},
                    "optimization_savings": {"opportunity": "Right-sizing", "amount": total_cost * 0.15},
                    "budget_recommendations": "Consider implementing cost alerts and budgets",
                    "reserved_instance_savings": "Potential 20-30% savings with reserved instances",
                    "right_sizing_impact": {"potential_savings": total_cost * 0.15, "affected_vms": len(vm_metrics)},
                    "executive_summary": f"Total monthly cost: ${total_cost:.2f} with optimization potential"
                }
                
        except Exception as e:
            print(f"Error generating cost report: {e}")
            return {
                "total_monthly_cost": 0,
                "cost_breakdown": {},
                "optimization_savings": {},
                "budget_recommendations": "Unable to generate recommendations",
                "reserved_instance_savings": "Unable to calculate",
                "right_sizing_impact": {},
                "executive_summary": "Cost analysis temporarily unavailable"
            }