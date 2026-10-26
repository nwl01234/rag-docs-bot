import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from core.rag import answer, build_index, load_docs


def test_index_built(tmp_path):
    docs = load_docs("data/docs")
    assert len(docs) >= 4
    idx = build_index(docs)
    assert idx["N"] == len(docs)


def test_answer_with_sources():
    idx = build_index(load_docs("data/docs"))
    r = answer("сколько дней отпуск", idx)
    assert "28" in r["answer"]
    assert r["sources"] and r["sources"][0]["doc"] == "hr_policy"


def test_no_match_is_honest():
    idx = build_index(load_docs("data/docs"))
    r = answer("как приготовить борщ", idx)
    assert "нет ответа" in r["answer"]
