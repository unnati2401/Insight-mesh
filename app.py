from flask import Flask, render_template, request, jsonify
from monitoring.collector import VMCollector
from monitoring.analyzer import VMAnalyzer
from monitoring.recommender import VMRecommender
from services.ai_service import GeminiAIService
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Initialize AI service
ai_service = None
try:
    ai_service = GeminiAIService()
    print("✅ AI service initialized successfully")
except Exception as e:
    print(f"⚠️ AI service initialization failed: {e}")

@app.route("/", methods=["GET", "POST"])
def dashboard():
    csp = request.form.get("csp", "AWS")
    subscription = request.form.get("subscription", "")

    # Collect VM metrics
    metrics = VMCollector(csp, subscription).collect()
    
    # Analyze metrics
    analysis = VMAnalyzer(metrics).analyze()
    
    # Generate AI-enhanced recommendations
    recommender = VMRecommender(analysis, metrics, use_ai=bool(ai_service))
    recommendations = recommender.generate()
    
    # Get AI-powered insights
    insights = recommender.get_infrastructure_insights(csp)
    cost_report = recommender.generate_cost_report(csp)
    
    # Get AI predictions and optimization plan
    future_insights = None
    optimization_plan = None
    
    if ai_service:
        try:
            future_insights = ai_service.predict_future_trends(metrics, csp)
            optimization_plan = ai_service.generate_optimization_plan(metrics, csp)
        except Exception as e:
            print(f"Error getting AI predictions: {e}")

    return render_template("dashboard.html",
                           csp=csp,
                           subscription=subscription,
                           analysis=analysis,
                           recommendations=recommendations,
                           insights=insights,
                           cost_report=cost_report,
                           future_insights=future_insights,
                           optimization_plan=optimization_plan,
                           ai_enabled=bool(ai_service))

@app.route("/api/predictions/<cloud_provider>")
def get_predictions(cloud_provider):
    """API endpoint to get AI predictions"""
    if not ai_service:
        return jsonify({"error": "AI service not available"}), 503
    
    try:
        metrics = VMCollector(cloud_provider).collect()
        predictions = ai_service.predict_future_trends(metrics, cloud_provider)
        return jsonify(predictions)
        
    except Exception as e:
        return jsonify({"error": f"Failed to get predictions: {str(e)}"}), 500

@app.route("/api/optimization-plan/<cloud_provider>")
def get_optimization_plan(cloud_provider):
    """API endpoint to get optimization plan"""
    if not ai_service:
        return jsonify({"error": "AI service not available"}), 503
    
    try:
        metrics = VMCollector(cloud_provider).collect()
        plan = ai_service.generate_optimization_plan(metrics, cloud_provider)
        return jsonify(plan)
        
    except Exception as e:
        return jsonify({"error": f"Failed to generate optimization plan: {str(e)}"}), 500

@app.route("/api/insights/<cloud_provider>")
def get_insights(cloud_provider):
    """API endpoint to get infrastructure insights"""
    if not ai_service:
        return jsonify({"error": "AI service not available"}), 503
    
    try:
        # Get current metrics for the cloud provider
        metrics = VMCollector(cloud_provider).collect()
        insights = ai_service.get_infrastructure_insights(metrics, cloud_provider)
        return jsonify(insights)
        
    except Exception as e:
        return jsonify({"error": f"Failed to get insights: {str(e)}"}), 500

@app.route("/api/cost-report/<cloud_provider>")
def get_cost_report(cloud_provider):
    """API endpoint to get cost analysis report"""
    if not ai_service:
        return jsonify({"error": "AI service not available"}), 503
    
    try:
        # Get current metrics for the cloud provider
        metrics = VMCollector(cloud_provider).collect()
        cost_report = ai_service.generate_cost_report(metrics, cloud_provider)
        return jsonify(cost_report)
        
    except Exception as e:
        return jsonify({"error": f"Failed to generate cost report: {str(e)}"}), 500

@app.route("/api/refresh-data", methods=["POST"])
def refresh_data():
    """API endpoint to refresh VM data with AI insights"""
    try:
        data = request.json
        csp = data.get("csp", "AWS")
        subscription = data.get("subscription", "")
        
        # Collect fresh metrics
        metrics = VMCollector(csp, subscription).collect()
        analysis = VMAnalyzer(metrics).analyze()
        
        # Generate AI-enhanced recommendations
        recommender = VMRecommender(analysis, metrics, use_ai=bool(ai_service))
        recommendations = recommender.generate()
        insights = recommender.get_infrastructure_insights(csp)
        cost_report = recommender.generate_cost_report(csp)
        
        # Get AI predictions and optimization plan
        future_insights = None
        optimization_plan = None
        
        if ai_service:
            try:
                future_insights = ai_service.predict_future_trends(metrics, csp)
                optimization_plan = ai_service.generate_optimization_plan(metrics, csp)
            except Exception as e:
                print(f"Error getting AI predictions: {e}")
        
        return jsonify({
            "metrics": metrics,
            "analysis": analysis,
            "recommendations": recommendations,
            "insights": insights,
            "cost_report": cost_report,
            "future_insights": future_insights,
            "optimization_plan": optimization_plan,
            "ai_enabled": bool(ai_service)
        })
        
    except Exception as e:
        return jsonify({"error": f"Data refresh failed: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(debug=True)
