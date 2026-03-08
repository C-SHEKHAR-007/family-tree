#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
main.py - Family Tree API Application Entry Point.

Author: Family Tree API Team
Created: 2026-02-23

This module bootstraps the FastAPI application and registers all routers.

OWASP Secure Coding Practices:
    - CORS configuration (to be tightened for production)
    - Input validation via Pydantic schemas
    - Authentication via JWT tokens
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import (
    auth,
    user_routes,
    person_routes,
    relationship_routes,
    tree_routes,
    address_routes,
    occupation_routes,
)

app = FastAPI(
    title="Family Tree API",
    description="A scalable API for managing family trees with authentication and RBAC",
    version="1.0.0",
)

# CORS Middleware - Tighten for production
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # TODO: Restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(auth.router)
app.include_router(user_routes.router)
app.include_router(person_routes.router)
app.include_router(relationship_routes.router)
app.include_router(tree_routes.router)
app.include_router(address_routes.router)
app.include_router(occupation_routes.router)


@app.get("/", tags=["Health"])
def root():
    """Health check endpoint."""
    return {"message": "Family Tree Backend is running!", "status": "healthy"}