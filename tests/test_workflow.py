"""
Basic smoke test for the main pipeline. Requires a valid OPENAI_API_KEY
and will make real (billed) API calls — mark as integration test.
"""

import pytest
from graph.workflow import run_pipeline


@pytest.mark.integration
def test_pipeline_produces_full_package():
    brief = {
        "brand": "TestBrand",
        "product": "Test Product",
        "audience": "Young professionals",
        "campaign": "Launch Week",
        "platforms": ["Instagram", "TikTok"],
        "tone": "playful",
        "num_assets": 3,
    }

    result = run_pipeline(brief)

    assert result["strategy"]
    assert len(result["content_ideas"]) == 3
    assert len(result["captions"]) == 3
    assert result["qc_report"]
    assert result["campaign_folder"]