#!/usr/bin/env bash

set -u

cd "$(dirname "$0")"

echo "=================================================="
echo "DharmaAI — FULL TEST RUNNER"
echo "=================================================="

FAILURES=0

run_test() {
    local name="$1"
    local command="$2"

    echo
    echo "=================================================="
    echo "$name"
    echo "=================================================="

    echo "\$ $command"

    bash -c "$command"

    local status=$?

    if [ "$status" -eq 0 ]; then
        echo
        echo "RESULT: PASS"
    else
        echo
        echo "RESULT: FAIL (exit code $status)"
        FAILURES=$((FAILURES + 1))
    fi
}

run_test \
    "1. OLLAMA CLIENT" \
    "python3 tests/test_ollama_client.py"

run_test \
    "2. BRAIN ENGINE" \
    "python3 tests/test_engine.py"

run_test \
    "3. BRAIN ROUTER" \
    "python3 tests/test_router.py"

run_test \
    "4. MEMORY STORE + CONTEXT" \
    "python3 tests/test_memory.py"

run_test \
    "5. MEMORY-AWARE BRAIN" \
    "python3 tests/test_memory_engine.py"

run_test \
    "6. AGENTS" \
    "python3 -m pytest -q tests/test_agents.py"

echo
echo "=================================================="
echo "DharmaAI — TEST SUMMARY"
echo "=================================================="

echo "Test groups : 6"
echo "Failures    : $FAILURES"

if [ "$FAILURES" -eq 0 ]; then
    echo
    echo "=========================================="
    echo "DHARMAAI TEST SUITE: ALL PASS"
    echo "=========================================="
    exit 0
else
    echo
    echo "=========================================="
    echo "DHARMAAI TEST SUITE: FAIL"
    echo "=========================================="
    exit 1
fi
