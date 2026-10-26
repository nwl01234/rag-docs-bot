import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from core import eval as rev


def test_hit_rate_on_golden():
    from core.rag import build_index, load_docs
    idx = build_index(load_docs("data/docs"))
    r = rev.hit_rate_at_k(idx, 3)
    assert r["golden_size"] == len(rev.GOLDEN)
    assert r["hit_rate"] > 0.5


def test_ab_offline():
    from core.rag import build_index, load_docs
    idx = build_index(load_docs("data/docs"))
    r = rev.ab_offline(idx)
    assert set(r) >= {"variant_a_synonyms", "variant_b_plain"}
    assert 0 <= r["variant_a_synonyms"] <= 1


def test_eval_report(tmp_path):
    r = rev.eval_report("data/docs")
    assert r["hit_rate_at_3"]["hit_rate"] == r["hit_rate_at_3"]["hit_rate"]
    assert Path("data/evals_report.json").exists()
