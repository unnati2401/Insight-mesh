from services.ai_service import GeminiAIService

class VMRecommender:
    def __init__(self, analysis, vm_metrics=None, use_ai=True):
        self.analysis = analysis
        self.vm_metrics = vm_metrics or []
        self.use_ai = use_ai
        self.ai_service = None
        
        if self.use_ai:
            try:
                self.ai_service = GeminiAIService()
            except Exception as e:
                print(f"AI service initialization failed: {e}")
                self.use_ai = False

    def generate(self):
        """Generate recommendations with optional AI enhancement"""
        if self.use_ai and self.ai_service and self.vm_metrics:
            try:
                # Get AI-enhanced recommendations
                enhanced_analysis = self.ai_service.enhance_vm_recommendations(
                    self.vm_metrics, self.analysis
                )
                return enhanced_analysis
            except Exception as e:
                print(f"AI enhancement failed, falling back to basic analysis: {e}")
        
        # Return basic analysis if AI is not available or failed
        return self.analysis
    
    def get_infrastructure_insights(self, cloud_provider="Unknown"):
        """Get high-level infrastructure insights using AI"""
        if self.use_ai and self.ai_service and self.vm_metrics:
            try:
                return self.ai_service.get_infrastructure_insights(self.vm_metrics, cloud_provider)
            except Exception as e:
                print(f"Failed to get infrastructure insights: {e}")
        
        # Return basic insights if AI is not available
        return {
            "health_score": 7,
            "optimization_opportunities": ["Review resource utilization", "Consider cost optimization"],
            "cost_optimization_potential": "10-20%",
            "summary": "Basic analysis available - enable AI for detailed insights"
        }
    
    def get_future_predictions(self, cloud_provider="Unknown"):
        """Get future trend predictions using AI"""
        if self.use_ai and self.ai_service and self.vm_metrics:
            try:
                return self.ai_service.predict_future_trends(self.vm_metrics, cloud_provider)
            except Exception as e:
                print(f"Failed to get future predictions: {e}")
        
        # Return basic predictions if AI is not available
        total_cost = sum(vm.get('cost', 0) for vm in self.vm_metrics)
        return {
            "usage_trend_prediction": {"cpu_trend": "stable", "memory_trend": "stable", "cost_trend": "stable"},
            "next_month_cost_projection": total_cost,
            "potential_bottlenecks": ["Monitor high-usage VMs"],
            "confidence_score": 50
        }
    
    def get_optimization_plan(self, cloud_provider="Unknown"):
        """Get comprehensive optimization plan using AI"""
        if self.use_ai and self.ai_service and self.vm_metrics:
            try:
                return self.ai_service.generate_optimization_plan(self.vm_metrics, cloud_provider)
            except Exception as e:
                print(f"Failed to get optimization plan: {e}")
        
        # Return basic plan if AI is not available
        return {
            "immediate_actions": [{"action": "Review resource utilization", "impact": "Medium", "effort_level": "Low"}],
            "short_term_plan": [{"action": "Optimize instance sizes", "timeline": "2 weeks", "expected_benefit": "Cost reduction"}],
            "overall_roi_estimate": "Basic optimization recommendations available"
        }
    
    def generate_cost_report(self, cloud_provider="Unknown"):
        """Generate cost analysis report"""
        if not self.vm_metrics:
            return {
                "total_monthly_cost": 0,
                "optimization_savings": None,
                "cost_breakdown": {},
                "top_cost_drivers": []
            }
        
        # Calculate costs from VM metrics
        total_monthly_cost = sum(vm.get('cost', 0) for vm in self.vm_metrics)
        
        # Calculate potential optimization savings
        high_cost_vms = [vm for vm in self.vm_metrics if vm.get('cost', 0) > 100]
        underutilized_vms = [vm for vm in self.vm_metrics if 
                           vm.get('cpu', 0) < 30 and vm.get('memory', 0) < 30]
        
        potential_savings = 0
        for vm in underutilized_vms:
            # Estimate 20-40% savings on underutilized VMs
            potential_savings += vm.get('cost', 0) * 0.3
        
        # Group costs by VM type or status
        cost_breakdown = {}
        for vm in self.vm_metrics:
            vm_type = vm.get('vm_type', 'Unknown')
            if vm_type not in cost_breakdown:
                cost_breakdown[vm_type] = 0
            cost_breakdown[vm_type] += vm.get('cost', 0)
        
        # Find top cost drivers
        top_cost_drivers = sorted(
            [{"vm_id": vm.get('vm_id', 'Unknown'), "cost": vm.get('cost', 0)} 
             for vm in self.vm_metrics], 
            key=lambda x: x['cost'], reverse=True
        )[:5]
        
        optimization_savings = None
        if potential_savings > 0:
            optimization_savings = {
                "amount": potential_savings,
                "percentage": (potential_savings / total_monthly_cost * 100) if total_monthly_cost > 0 else 0,
                "vms_affected": len(underutilized_vms)
            }
        
        return {
            "total_monthly_cost": total_monthly_cost,
            "optimization_savings": optimization_savings,
            "cost_breakdown": cost_breakdown,
            "top_cost_drivers": top_cost_drivers
        }
