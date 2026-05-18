#!/bin/bash
echo "============================================"
echo "BOOKFLOW AI COMMERCE - E2E TEST SUITE"
echo "============================================"

echo ""
echo "1. Verificando health de todos los servicios..."
python health_check.py

echo ""
echo "2. Ejecutando pruebas E2E..."
pytest tests/ -v --tb=short

echo ""
echo "============================================"
echo "E2E TESTS COMPLETADOS"
echo "============================================"
