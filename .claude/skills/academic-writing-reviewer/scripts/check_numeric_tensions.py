#!/usr/bin/env python3
"""
check_numeric_tensions.py - Detector determinístico de tensões e contradições qualitativas em métricas.

Objetivo:
Detectar quando uma mesma métrica ou construto (latência, custo, acurácia, overhead)
é descrita com tendências ou qualificadores opostos (aumento vs. redução) dentro
de uma janela contextual (especialmente sob marcadores adversativos) ou transversalmente
entre Introdução e Conclusão/Discussão.

Não substitui o G4.5 (academic-data-validator), que valida números exatos de tabelas.
Este script foca na congruência narrativa e na coerência de direção de tendência.
"""

import argparse
import json
import os
import re
from typing import Any, Dict, List, Optional, Tuple

try:
    from parsers import MarkdownParser
except ImportError:
    from .parsers import MarkdownParser


METRIC_KEYWORDS = {
    "latencia": ["latência", "latency", "tempo de resposta", "response time", "delay", "atraso"],
    "custo": ["custo", "cost", "tokens", "gasto", "despesa", "budget", "consumo"],
    "acuracia": ["acurácia", "accuracy", "precisão", "precision", "desempenho", "performance", "taxa de acerto", "score"],
    "overhead": ["overhead", "sobrecarga", "esforço de coordenação", "coordination overhead", "atrito"],
    "erros": ["taxa de erro", "error rate", "alucinação", "hallucination", "falhas", "failures"]
}

TREND_UP = [
    "aumento", "aumentou", "aumenta", "maior", "cresceu", "crescimento", "elevação",
    "elevou", "superior", "alto", "alta", "expandiu", "subiu",
    "increased", "increase", "higher", "grew", "growth", "rose", "rising", "elevated", "expanded"
]

TREND_DOWN = [
    "redução", "reduziu", "reduz", "menor", "caiu", "queda", "diminuiu", "diminuição",
    "decréscimo", "inferior", "baixo", "baixa",
    "decreased", "decrease", "lower", "dropped", "drop", "fell", "reduction", "declined", "diminished"
]

ADVERSATIVE_MARKERS = [
    "no entanto", "contudo", "todavia", "entretanto", "porém", "apesar de", "não obstante",
    "however", "although", "nevertheless", "nonetheless", "yet", "despite", "in contrast", "whereas"
]


class NumericTensionChecker:
    def __init__(self):
        self.parser = MarkdownParser()

    def _extract_metric_trend(self, sentence: str) -> List[Tuple[str, str, str]]:
        """
        Retorna lista de tuplas: (categoria_metrica, tendencia ['UP'/'DOWN'], termo_encontrado)
        """
        results = []
        s_lower = sentence.lower()

        for cat, keywords in METRIC_KEYWORDS.items():
            kw_match = any(re.search(r"\b" + re.escape(kw) + r"\b", s_lower) for kw in keywords)
            if not kw_match:
                continue

            # Checar direção
            up_match = any(re.search(r"\b" + re.escape(u) + r"\b", s_lower) for u in TREND_UP)
            down_match = any(re.search(r"\b" + re.escape(d) + r"\b", s_lower) for d in TREND_DOWN)

            if up_match and not down_match:
                results.append((cat, "UP", sentence.strip()))
            elif down_match and not up_match:
                results.append((cat, "DOWN", sentence.strip()))
            elif up_match and down_match:
                # Contém ambos na mesma frase
                results.append((cat, "MIXED", sentence.strip()))

        return results

    def check_adversative_tensions(self, text: str, filename: str = "") -> List[Dict[str, Any]]:
        """Busca sentenças com conectivos adversativos que alternam a polaridade da métrica de forma não-explicada."""
        findings = []
        raw_paras = text.split("\n\n")

        for para in raw_paras:
            p_clean = para.strip()
            if not p_clean or p_clean.startswith("#"):
                continue

            sentences = [s.strip() for s in re.split(r"(?<=[.!?])\s+", p_clean) if len(s.strip()) > 10]
            if len(sentences) < 2:
                continue

            for i in range(len(sentences) - 1):
                s1 = sentences[i]
                s2 = sentences[i + 1]
                s2_lower = s2.lower()

                has_adversative = any(re.search(r"\b" + re.escape(adv) + r"\b", s2_lower) for adv in ADVERSATIVE_MARKERS)
                if not has_adversative:
                    continue

                trends1 = self._extract_metric_trend(s1)
                trends2 = self._extract_metric_trend(s2)

                for cat1, dir1, _ in trends1:
                    for cat2, dir2, _ in trends2:
                        if cat1 == cat2 and dir1 in ("UP", "DOWN") and dir2 in ("UP", "DOWN") and dir1 != dir2:
                            findings.append({
                                "file": filename,
                                "issue_code": "NUM-02",
                                "severity": "WARNING",
                                "metric": cat1,
                                "type": "Tensão adversativa de polaridade",
                                "direction_1": dir1,
                                "direction_2": dir2,
                                "snippet_1": s1[:90],
                                "snippet_2": s2[:90],
                                "suggestion": f"A métrica '{cat1}' muda de polaridade ({dir1} -> {dir2}) sob conectivo adversativo. Verifique se a nuance causal está plenamente explicada para não soar contraditório."
                            })

        return findings

    def check_cross_section_tensions(self, sections: Dict[str, str]) -> List[Dict[str, Any]]:
        """Compara afirmações de Introdução/Abstract com Achados/Conclusão."""
        findings = []
        sec_trends: Dict[str, List[Tuple[str, str, str]]] = {}

        for sec_name, content in sections.items():
            sentences = [s.strip() for s in re.split(r"(?<=[.!?])\s+", content) if len(s.strip()) > 15]
            trends = []
            for s in sentences:
                trends.extend(self._extract_metric_trend(s))
            sec_trends[sec_name] = trends

        intro_keys = [k for k in sections.keys() if any(x in k.lower() for x in ["intro", "abstract"])]
        findings_keys = [k for k in sections.keys() if any(x in k.lower() for x in ["finding", "result", "discussion", "conclusion"])]

        for ik in intro_keys:
            for fk in findings_keys:
                for cat1, dir1, s1 in sec_trends.get(ik, []):
                    for cat2, dir2, s2 in sec_trends.get(fk, []):
                        if cat1 == cat2 and dir1 in ("UP", "DOWN") and dir2 in ("UP", "DOWN") and dir1 != dir2:
                            # Apenas registrar se as frases não forem exatamente a mesma
                            if s1 != s2:
                                findings.append({
                                    "issue_code": "NUM-01",
                                    "severity": "CRITICAL",
                                    "metric": cat1,
                                    "section_a": ik,
                                    "direction_a": dir1,
                                    "snippet_a": s1[:90],
                                    "section_b": fk,
                                    "direction_b": dir2,
                                    "snippet_b": s2[:90],
                                    "suggestion": f"Potencial contradição transversal na métrica '{cat1}': descrita como {dir1} em '{ik}', mas como {dir2} em '{fk}'. Reconcilie a narrativa empírica."
                                })

        return findings

    def analyze_file(self, filepath: str) -> Dict[str, Any]:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
        fname = os.path.basename(filepath)
        tensions = self.check_adversative_tensions(content, filename=fname)
        return {
            "file": fname,
            "total_tensions": len(tensions),
            "findings": tensions
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
                    res = self.analyze_file(fpath)
                    file_results[file] = res
                    total_issues += res["total_tensions"]

        cross_findings = self.check_cross_section_tensions(sections)
        # Deduplicar cross-findings por métrica e seção
        dedup_cross = []
        seen = set()
        for c in cross_findings:
            key = (c["metric"], c["section_a"], c["section_b"], c["direction_a"], c["direction_b"])
            if key not in seen:
                seen.add(key)
                dedup_cross.append(c)

        total_issues += len(dedup_cross)

        return {
            "total_issues": total_issues,
            "cross_section_tensions": dedup_cross,
            "file_results": file_results
        }


def main():
    parser = argparse.ArgumentParser(description="Verificador determinístico de tensões e coerência narrativa de métricas.")
    parser.add_argument("path", help="Caminho para arquivo markdown ou pasta de draft.")
    parser.add_argument("--json", action="store_true", help="Saída em formato JSON.")
    args = parser.parse_args()

    checker = NumericTensionChecker()

    if os.path.isdir(args.path):
        results = checker.analyze_directory(args.path)
        if args.json:
            print(json.dumps(results, indent=2, ensure_ascii=False))
        else:
            print(f"=== Auditoria de Tensões Narrativas e Coerência de Métricas ({args.path}) ===")
            print(f"Total de alertas encontrados: {results['total_issues']}\n")

            if results["cross_section_tensions"]:
                print(f"🚨 TENSÕES TRANSVERSAIS ENTRE SEÇÕES ({len(results['cross_section_tensions'])} casos):")
                for t in results["cross_section_tensions"]:
                    print(f"   [{t['issue_code']}] [{t['severity']}] Métrica: '{t['metric'].upper()}'")
                    print(f"      {t['section_a']} ({t['direction_a']}): '{t['snippet_a']}...'")
                    print(f"      {t['section_b']} ({t['direction_b']}): '{t['snippet_b']}...'")
                    print(f"      -> {t['suggestion']}\n")

            for fname, res in results["file_results"].items():
                if res["total_tensions"] > 0:
                    print(f"⚠️  {fname}: {res['total_tensions']} tensões adversativas locais")
                    for f in res["findings"]:
                        print(f"      [{f['issue_code']}] Métrica: {f['metric']} ({f['direction_1']} -> {f['direction_2']})")
                        print(f"         1: {f['snippet_1']}...")
                        print(f"         2: {f['snippet_2']}...")
                        print(f"         -> {f['suggestion']}")
    else:
        res = checker.analyze_file(args.path)
        if args.json:
            print(json.dumps(res, indent=2, ensure_ascii=False))
        else:
            print(f"=== Auditoria de Tensões: {res['file']} ===")
            print(f"Total de alertas: {res['total_tensions']}")
            for f in res["findings"]:
                print(f"   [{f['issue_code']}] [{f['severity']}] Métrica: {f['metric']} ({f['direction_1']} -> {f['direction_2']})")
                print(f"      -> {f['suggestion']}")


if __name__ == "__main__":
    main()
