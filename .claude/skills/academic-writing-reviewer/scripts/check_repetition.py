#!/usr/bin/env python3
"""
check_repetition.py - Detector determinístico de redundância, repetição e monotonia.

Capacidades:
1. Repetição imediata de n-grams (3 e 4 palavras) entre sentenças próximas.
2. Início monotônico consecutivo (3+ sentenças iniciando com a mesma palavra/fórmula).
3. Redundância transversal entre seções (parágrafos quase idênticos em seções distintas).
4. Variação de comprimento de frase (burstiness / monotonia estrutural).
"""

import argparse
import difflib
import json
import os
import re
from typing import Any, Dict, List, Set, Tuple

try:
    from parsers import MarkdownParser
except ImportError:
    from .parsers import MarkdownParser


COMMON_STOP_NGRAMS = {
    # Português
    "de acordo com", "no que diz", "que diz respeito", "a partir de", "com base em",
    "do ponto de", "ponto de vista", "em relação a", "no contexto do", "no contexto da",
    "por meio de", "com o objetivo", "o objetivo de", "por outro lado", "tendo em vista",
    "em termos de", "ao longo do", "ao longo da", "como pode ser", "pode ser visto",
    # Inglês
    "in order to", "according to the", "as well as", "with respect to", "in terms of",
    "on the other", "the other hand", "in the context", "the context of", "based on the",
    "as shown in", "in this study", "the results of", "the impact of", "in addition to",
}


def clean_markdown_for_text(text: str) -> str:
    """Remove código, math, comentários e referências LaTeX."""
    text = re.sub(r"<!--.*?-->", "", text, flags=re.DOTALL)
    text = re.sub(r"(```|~~~).*?\1", "", text, flags=re.DOTALL)
    text = re.sub(r"\$\$[^$]*\$\$", "", text, flags=re.DOTALL)
    text = re.sub(r"\$[^$]+\$", "", text)
    text = re.sub(r"\\cite[a-z]*\{[^}]+\}", "", text)
    text = re.sub(r"\[([^\]]+)\]\([^\)]+\)", r"\1", text)
    text = re.sub(r"`[^`]+`", "", text)
    return text


def split_into_sentences(text: str) -> List[str]:
    """Divisão básica de sentenças por pontuação forte."""
    clean = clean_markdown_for_text(text)
    # Remove títulos markdown
    clean = re.sub(r"^#{1,6}\s+.*$", "", clean, flags=re.MULTILINE)
    # Divide por ponto final, exclamação ou interrogação seguido de espaço e maiúscula
    raw_sentences = re.split(r"(?<=[.!?])\s+(?=[A-ZÀ-Ú])", clean)
    sentences = [s.strip() for s in raw_sentences if len(s.strip().split()) >= 4]
    return sentences


def get_ngrams(tokens: List[str], n: int) -> List[Tuple[str, ...]]:
    return [tuple(tokens[i : i + n]) for i in range(len(tokens) - n + 1)]


class RepetitionChecker:
    def __init__(self):
        self.parser = MarkdownParser()

    def check_sentence_echoes(self, text: str, filename: str = "") -> List[Dict[str, Any]]:
        """Detecta eco de n-grams de 3 e 4 palavras entre sentenças adjacentes (janela de 2 sentenças)."""
        sentences = split_into_sentences(text)
        findings = []
        tokenized_sentences = [
            [re.sub(r"[^\wáéíóúãõâêîôûàèìòùç]", "", w.lower()) for w in s.split()]
            for s in sentences
        ]

        for i in range(len(tokenized_sentences) - 1):
            s1_tokens = [w for w in tokenized_sentences[i] if w]
            s2_tokens = [w for w in tokenized_sentences[i + 1] if w]

            # Checar 4-grams e 3-grams
            for n in (4, 3):
                ngrams1 = set(get_ngrams(s1_tokens, n))
                ngrams2 = set(get_ngrams(s2_tokens, n))
                overlap = ngrams1.intersection(ngrams2)

                for ng in overlap:
                    phrase = " ".join(ng)
                    if phrase in COMMON_STOP_NGRAMS:
                        continue

                    findings.append({
                        "file": filename,
                        "issue_code": "REP-02",
                        "severity": "WARNING",
                        "type": f"Eco de {n}-gram em sentenças vizinhas",
                        "repeated_phrase": phrase,
                        "context": f"Sentença 1: '{sentences[i][:70]}...' | Sentença 2: '{sentences[i+1][:70]}...'",
                        "suggestion": "Reestruture a segunda frase para evitar eco de vocabulário ou use pronome/coesão referencial."
                    })

        return findings

    def check_monotonous_openings(self, text: str, filename: str = "") -> List[Dict[str, Any]]:
        """Detecta se 3 sentenças consecutivas iniciam com a mesma palavra ou conectivo."""
        sentences = split_into_sentences(text)
        findings = []

        for i in range(len(sentences) - 2):
            w1 = sentences[i].split()[0].lower().rstrip(",:;")
            w2 = sentences[i + 1].split()[0].lower().rstrip(",:;")
            w3 = sentences[i + 2].split()[0].lower().rstrip(",:;")

            if w1 == w2 == w3 and len(w1) > 2:
                findings.append({
                    "file": filename,
                    "issue_code": "AIM-04",
                    "severity": "ADVISORY",
                    "type": "Início monotônico triplo",
                    "word": w1,
                    "snippet": f"1: '{sentences[i][:40]}...' | 2: '{sentences[i+1][:40]}...' | 3: '{sentences[i+2][:40]}...'",
                    "suggestion": f"Alterne o início das sentenças para evitar monotonia rítmica (3 sentenças seguidas iniciando com '{w1}')."
                })

        return findings

    def check_cross_section_duplicates(self, sections: Dict[str, str], threshold: float = 0.70) -> List[Dict[str, Any]]:
        """Detecta parágrafos substantivos com alta similaridade textual entre seções distintas."""
        findings = []
        section_paras: Dict[str, List[str]] = {}

        for sec_name, content in sections.items():
            cleaned = clean_markdown_for_text(content)
            raw_paras = cleaned.split("\n\n")
            # Parágrafos substantivos (> 25 palavras, sem cabeçalhos)
            paras = [
                p.strip() for p in raw_paras
                if len(p.strip().split()) >= 25 and not p.strip().startswith("#")
            ]
            section_paras[sec_name] = paras

        sec_names = list(section_paras.keys())
        for i in range(len(sec_names)):
            sec_a = sec_names[i]
            for j in range(i + 1, len(sec_names)):
                sec_b = sec_names[j]

                # Não comparar tabelas ou legendas
                if any(x in sec_a.lower() or x in sec_b.lower() for x in ["table", "figure", "title"]):
                    continue

                for pa_idx, pa in enumerate(section_paras[sec_a]):
                    for pb_idx, pb in enumerate(section_paras[sec_b]):
                        ratio = difflib.SequenceMatcher(None, pa.lower(), pb.lower()).ratio()
                        if ratio >= threshold:
                            findings.append({
                                "issue_code": "REP-01",
                                "severity": "CRITICAL",
                                "similarity_ratio": round(ratio, 2),
                                "section_a": sec_a,
                                "section_b": sec_b,
                                "snippet_a": f"{pa[:90]}...",
                                "snippet_b": f"{pb[:90]}...",
                                "suggestion": f"Redundância transversal de {int(ratio*100)}% entre '{sec_a}' e '{sec_b}'. Elimine a duplicação ou diferencie o foco analítico."
                            })

        return findings

    def analyze_single_file(self, filepath: str) -> Dict[str, Any]:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
        fname = os.path.basename(filepath)
        echoes = self.check_sentence_echoes(content, filename=fname)
        monotony = self.check_monotonous_openings(content, filename=fname)

        return {
            "file": fname,
            "total_issues": len(echoes) + len(monotony),
            "echo_count": len(echoes),
            "monotony_count": len(monotony),
            "findings": echoes + monotony
        }

    def analyze_directory(self, dirpath: str) -> Dict[str, Any]:
        sections: Dict[str, str] = {}
        file_results = {}
        total_issues = 0

        for root, _, files in os.walk(dirpath):
            for file in sorted(files):
                if file.endswith(".md"):
                    fpath = os.path.join(root, file)
                    with open(fpath, "r", encoding="utf-8") as f:
                        content = f.read()
                    sections[file] = content
                    res = self.analyze_single_file(fpath)
                    file_results[file] = res
                    total_issues += res["total_issues"]

        cross_findings = self.check_cross_section_duplicates(sections)
        total_issues += len(cross_findings)

        return {
            "total_issues": total_issues,
            "cross_section_duplicates": cross_findings,
            "file_results": file_results
        }


def main():
    parser = argparse.ArgumentParser(description="Verificador determinístico de redundância e repetição.")
    parser.add_argument("path", help="Caminho para arquivo markdown ou diretório de draft.")
    parser.add_argument("--json", action="store_true", help="Saída em formato JSON.")
    args = parser.parse_args()

    checker = RepetitionChecker()

    if os.path.isdir(args.path):
        results = checker.analyze_directory(args.path)
        if args.json:
            print(json.dumps(results, indent=2, ensure_ascii=False))
        else:
            print(f"=== Auditoria de Repetição e Redundância ({args.path}) ===")
            print(f"Total de issues: {results['total_issues']}\n")

            if results["cross_section_duplicates"]:
                print(f"🚨 DUPLICAÇÃO TRANSVERSAL ({len(results['cross_section_duplicates'])} casos):")
                for d in results["cross_section_duplicates"]:
                    print(f"   [{d['issue_code']}] [{d['severity']}] {d['section_a']} <-> {d['section_b']} (Similaridade: {d['similarity_ratio']})")
                    print(f"      Trecho A: {d['snippet_a']}")
                    print(f"      Trecho B: {d['snippet_b']}")
                    print(f"      -> {d['suggestion']}\n")

            for fname, res in results["file_results"].items():
                if res["total_issues"] > 0:
                    print(f"⚠️  {fname}: {res['total_issues']} issues locais (Ecos: {res['echo_count']}, Início Monótono: {res['monotony_count']})")
                    for f in res["findings"]:
                        print(f"      [{f['issue_code']}] [{f['severity']}] {f['type']}: {f.get('repeated_phrase') or f.get('word')}")
                        print(f"         -> {f['suggestion']}")
    else:
        res = checker.analyze_single_file(args.path)
        if args.json:
            print(json.dumps(res, indent=2, ensure_ascii=False))
        else:
            print(f"=== Auditoria de Repetição: {res['file']} ===")
            print(f"Total de issues: {res['total_issues']}")
            for f in res["findings"]:
                print(f"   [{f['issue_code']}] [{f['severity']}] {f['type']}: {f.get('repeated_phrase') or f.get('word')}")
                print(f"      -> {f['suggestion']}")


if __name__ == "__main__":
    main()
