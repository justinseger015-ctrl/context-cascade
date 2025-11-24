# Metrics API Router
# Performance metrics, cost tracking, and analytics aggregation

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, and_
from typing import List, Optional
from datetime import datetime, timedelta
from pydantic import BaseModel, Field

from ..database import get_db
from ..models.metric import Metric

router = APIRouter()

# Pydantic schemas
class MetricCreate(BaseModel):
    """Schema for recording a new metric"""
    agent_id: str = Field(..., description="Agent ID")
    metric_type: str = Field(..., description="Metric type (execution, cost, quality, task_completion)")
    execution_time_ms: Optional[float] = Field(None, description="Execution time in milliseconds")
    success: Optional[bool] = Field(None, description="Success flag (true/false)")
    tokens_used: Optional[int] = Field(None, description="Tokens used")
    api_calls: Optional[int] = Field(None, description="Number of API calls")
    cost_usd: Optional[float] = Field(None, description="Cost in USD")
    quality_score: Optional[float] = Field(None, ge=0.0, le=1.0, description="Quality score (0-1)")
    code_violations: Optional[int] = Field(None, description="Number of code violations")
    tasks_completed: Optional[int] = Field(None, description="Tasks completed count")
    tasks_failed: Optional[int] = Field(None, description="Tasks failed count")
    context: Optional[dict] = Field(None, description="Additional context (JSON)")

class MetricResponse(BaseModel):
    """Schema for metric API responses"""
    metric_id: str
    agent_id: str
    metric_type: str
    execution_time_ms: Optional[float]
    success: Optional[bool]
    tokens_used: Optional[int]
    api_calls: Optional[int]
    cost_usd: Optional[float]
    quality_score: Optional[float]
    code_violations: Optional[int]
    tasks_completed: Optional[int]
    tasks_failed: Optional[int]
    context: Optional[dict]
    recorded_at: str

    class Config:
        from_attributes = True

# Endpoints
@router.post("/", response_model=MetricResponse, status_code=201)
def record_metric(metric: MetricCreate, db: Session = Depends(get_db)):
    """
    Record a new metric for an agent.

    **Use case**: Called by Phase 2 hooks to log performance, cost, and quality metrics
    """
    # Validate agent exists
    from ..models.agent import Agent
    agent = db.query(Agent).filter(Agent.agent_id == metric.agent_id).first()
    if not agent:
        raise HTTPException(status_code=404, detail=f"Agent with ID '{metric.agent_id}' not found")

    # Create metric record
    new_metric = Metric(
        agent_id=metric.agent_id,
        metric_type=metric.metric_type,
        execution_time_ms=metric.execution_time_ms,
        success=1 if metric.success else 0 if metric.success is not None else None,
        tokens_used=metric.tokens_used,
        api_calls=metric.api_calls,
        cost_usd=metric.cost_usd,
        quality_score=metric.quality_score,
        code_violations=metric.code_violations,
        tasks_completed=metric.tasks_completed,
        tasks_failed=metric.tasks_failed,
        context=metric.context
    )

    db.add(new_metric)
    db.commit()
    db.refresh(new_metric)

    return new_metric.to_dict()

@router.get("/", response_model=List[MetricResponse])
def list_metrics(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Max records to return"),
    agent_id: Optional[str] = Query(None, description="Filter by agent ID"),
    metric_type: Optional[str] = Query(None, description="Filter by metric type"),
    start_date: Optional[datetime] = Query(None, description="Filter by start date"),
    end_date: Optional[datetime] = Query(None, description="Filter by end date"),
    db: Session = Depends(get_db)
):
    """
    List metrics with optional filters and pagination.

    **Filters**:
    - agent_id: Filter by specific agent
    - metric_type: Filter by metric type (execution, cost, quality, task_completion)
    - start_date/end_date: Filter by time range

    **Pagination**: Use `skip` and `limit` parameters
    """
    query = db.query(Metric)

    # Apply filters
    if agent_id:
        query = query.filter(Metric.agent_id == agent_id)
    if metric_type:
        query = query.filter(Metric.metric_type == metric_type)
    if start_date:
        query = query.filter(Metric.recorded_at >= start_date)
    if end_date:
        query = query.filter(Metric.recorded_at <= end_date)

    # Order by most recent first
    query = query.order_by(Metric.recorded_at.desc())

    # Pagination
    metrics = query.offset(skip).limit(limit).all()

    return [metric.to_dict() for metric in metrics]

@router.get("/aggregate")
def aggregate_metrics(
    agent_id: Optional[str] = Query(None, description="Filter by agent ID"),
    metric_type: Optional[str] = Query(None, description="Filter by metric type"),
    days: int = Query(7, ge=1, le=90, description="Number of days to aggregate (default 7)"),
    db: Session = Depends(get_db)
):
    """
    Get aggregated metrics for analytics.

    **Returns**:
    - Total count
    - Average execution time
    - Success rate
    - Total cost (USD)
    - Total tokens used
    - Average quality score
    """
    start_date = datetime.utcnow() - timedelta(days=days)
    query = db.query(Metric).filter(Metric.recorded_at >= start_date)

    # Apply filters
    if agent_id:
        query = query.filter(Metric.agent_id == agent_id)
    if metric_type:
        query = query.filter(Metric.metric_type == metric_type)

    metrics = query.all()

    if not metrics:
        return {
            "count": 0,
            "avg_execution_time_ms": 0,
            "success_rate": 0,
            "total_cost_usd": 0,
            "total_tokens_used": 0,
            "avg_quality_score": 0
        }

    # Calculate aggregates
    total_count = len(metrics)
    execution_times = [m.execution_time_ms for m in metrics if m.execution_time_ms is not None]
    successes = [m.success for m in metrics if m.success is not None]
    costs = [m.cost_usd for m in metrics if m.cost_usd is not None]
    tokens = [m.tokens_used for m in metrics if m.tokens_used is not None]
    quality_scores = [m.quality_score for m in metrics if m.quality_score is not None]

    return {
        "count": total_count,
        "avg_execution_time_ms": sum(execution_times) / len(execution_times) if execution_times else 0,
        "success_rate": sum(successes) / len(successes) if successes else 0,
        "total_cost_usd": sum(costs),
        "total_tokens_used": sum(tokens),
        "avg_quality_score": sum(quality_scores) / len(quality_scores) if quality_scores else 0,
        "time_range_days": days
    }

@router.get("/agent/{agent_id}/summary")
def get_agent_metrics_summary(agent_id: str, db: Session = Depends(get_db)):
    """
    Get comprehensive metrics summary for a specific agent.

    **Returns**: Performance, cost, quality metrics aggregated across all time
    """
    # Validate agent exists
    from ..models.agent import Agent
    agent = db.query(Agent).filter(Agent.agent_id == agent_id).first()
    if not agent:
        raise HTTPException(status_code=404, detail=f"Agent with ID '{agent_id}' not found")

    metrics = db.query(Metric).filter(Metric.agent_id == agent_id).all()

    if not metrics:
        return {
            "agent_id": agent_id,
            "total_metrics": 0,
            "performance": {},
            "cost": {},
            "quality": {}
        }

    # Aggregate by type
    execution_times = [m.execution_time_ms for m in metrics if m.execution_time_ms is not None]
    successes = [m.success for m in metrics if m.success is not None]
    costs = [m.cost_usd for m in metrics if m.cost_usd is not None]
    tokens = [m.tokens_used for m in metrics if m.tokens_used is not None]
    quality_scores = [m.quality_score for m in metrics if m.quality_score is not None]
    tasks_completed = [m.tasks_completed for m in metrics if m.tasks_completed is not None]
    tasks_failed = [m.tasks_failed for m in metrics if m.tasks_failed is not None]

    return {
        "agent_id": agent_id,
        "total_metrics": len(metrics),
        "performance": {
            "avg_execution_time_ms": sum(execution_times) / len(execution_times) if execution_times else 0,
            "success_rate": sum(successes) / len(successes) if successes else 0,
            "total_tasks_completed": sum(tasks_completed),
            "total_tasks_failed": sum(tasks_failed)
        },
        "cost": {
            "total_cost_usd": sum(costs),
            "total_tokens_used": sum(tokens)
        },
        "quality": {
            "avg_quality_score": sum(quality_scores) / len(quality_scores) if quality_scores else 0
        }
    }


@router.get("/quality/", response_model=dict)
def get_quality_metrics(
    agent_id: Optional[str] = Query(None),
    days: int = Query(7, ge=1, le=90),
    db: Session = Depends(get_db)
):
    """Get code quality metrics over time period"""
    from datetime import timedelta
    cutoff_date = datetime.utcnow() - timedelta(days=days)
    query = db.query(Metric).filter(Metric.recorded_at >= cutoff_date)
    if agent_id:
        query = query.filter(Metric.agent_id == agent_id)
    metrics = query.filter(Metric.metric_type == "quality").all()
    total = len(metrics)
    avg_quality = sum(m.quality_score or 0 for m in metrics) / total if total > 0 else 0
    total_violations = sum(m.code_violations or 0 for m in metrics)
    return {"overall_quality_score": round(avg_quality, 2), "total_code_violations": total_violations, "metrics_analyzed": total, "period_days": days}


@router.get("/resources/usage/", response_model=dict)
def get_resource_usage(
    agent_id: Optional[str] = Query(None),
    days: int = Query(7, ge=1, le=90),
    db: Session = Depends(get_db)
):
    """Get resource usage metrics (tokens, cost, API calls)"""
    from datetime import timedelta
    cutoff_date = datetime.utcnow() - timedelta(days=days)
    query = db.query(Metric).filter(Metric.recorded_at >= cutoff_date)
    if agent_id:
        query = query.filter(Metric.agent_id == agent_id)
    metrics = query.all()
    total_tokens = sum(m.tokens_used or 0 for m in metrics)
    total_cost = sum(m.cost_usd or 0 for m in metrics)
    total_api_calls = sum(m.api_calls or 0 for m in metrics)
    return {"total_tokens_used": total_tokens, "total_cost_usd": round(total_cost, 2), "total_api_calls": total_api_calls, "period_days": days}
