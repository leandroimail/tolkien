#!/usr/bin/env python3
"""
check_ai_markers.py - Detecção determinística de vocabulário e padrões de IA (EN e PT-BR).

Base empírica:
- Kobak et al. (Science Advances 2025): excess style words.
- WikiProject AI Cleanup: negative parallelisms, throat-clearing, superficial participles.
- Corpus PT-BR acadêmico: fórmulas de transição e clichês de IA em português.

Classificação por Tiers:
- Tier 1 (Crítico/Alto): delve, underscores, pivotal, crucial, ademais, além disso, desempenha papel fundamental, tapeçaria.
- Tier 2 (Estrutura/Falso Contraste): it's not just X it's Y, throat-clearing ("vale ressaltar", "in today's world").
- Tier 3 (Contextual): robust, comprehensive, fomento, alavancar, seamless.
"""

import argparse
import json
import os
import re
import sys
from typing import Any, Dict, List, Tuple

try:
    from parsers import MarkdownParser, get_parser
except ImportError:
    from .parsers import MarkdownParser, get_parser


TIER_1_PATTERNS = [
    # English (Kobak et al., top excess words)
    (r"\bdelv(e|es|ed|ing)\b", "delve", "EN", "AIM-01", "Substitua por investigate, examine, analyze"),
    (r"\bunderscor(e|es|ed|ing)\b", "underscore", "EN", "AIM-01", "Substitua por emphasize, show, indicate"),
    (r"\bshowcas(e|es|ed|ing)\b", "showcase", "EN", "AIM-01", "Substitua por present, demonstrate, report"),
    (r"\bpivotal\b", "pivotal", "EN", "AIM-01", "Substitua por central, key, important"),
    (r"\btapestry\b", "tapestry (figurativo)", "EN", "AIM-01", "Metáfora de IA: use structure, collection, system"),
    (r"\btestament\b", "testament to", "EN", "AIM-01", "Substitua por evidence of, indicates that"),
    (r"\bbeacon\b", "beacon", "EN", "AIM-01", "Substitua por model, example"),
    (r"\bintricac(y|ies)\b", "intricacy", "EN", "AIM-01", "Substitua por detail, complexity"),
    
    # Portuguese (Clichês recorrentes de LLM)
    (r"\bdesempenha\s+um\s+papel\s+(crucial|fundamental|preponderante|essencial)\b", "desempenha papel crucial", "PT", "AIM-01", "Fórmula vazia: explique diretamente o que o elemento faz"),
    (r"\bvale\s+(ressaltar|destacar|lembrar|notar)\s+que\b", "vale ressaltar que", "PT", "AIM-03", "Throat-clearing: remova e inicie diretamente pela informação"),
    (r"\bé\s+(mister|imperativo|crucial|fundamental)\s+destacar\b", "é mister destacar", "PT", "AIM-03", "Pedantismo de IA: remova e apresente o dado"),
    (r"\bno\s+cenário\s+(atual|contemporâneo)\b", "no cenário atual", "PT", "AIM-03", "Abertura vazia de IA: contextualize com dados ou remova"),
    (r"\bno\s+mundo\s+(globalizado|em\s+rápida\s+evolução)\b", "no mundo globalizado", "PT", "AIM-03", "Clichê introdutório: vá direto ao gap de pesquisa"),
    (r"\btapeçaria\b", "tapeçaria (figurativo)", "PT", "AIM-01", "Metáfora clássica traduzida de IA"),
    (r"\boutrossim\b", "outrossim", "PT", "AIM-01", "Vocabulário artificialmente arcaico: use além disso ou conecte logicamente"),
]

TIER_2_PATTERNS = [
    # Negative parallelisms (WikiProject AI Cleanup)
    (r"\b(it is|it's)\s+not\s+(just|only)\s+[^,;—\n]+[,;—]\s*(it is|it's|but)\b", "It's not just X, it's Y", "EN", "AIM-02", "Falso contraste de IA: apresente a constatação objetiva diretamente"),
    (r"\bnão\s+(se\s+trata\s+apenas|apenas)\s+de\s+[^,;—\n]+[,;—]\s*(mas\s+sim|mas\s+também)\b", "Não apenas X, mas sim Y", "PT", "AIM-02", "Falso contraste de IA: descreva a contribuição concreta"),
    (r"\bnot\s+only\s+[^,;—\n]+[,;—]\s*but\s+(also)?\b", "Not only X, but Y", "EN", "AIM-02", "Paralelismo retórico oco: prefira afirmação direta"),
    (r"\bno\s+x[.,]\s*no\s+y[.,]\s*just\s+z\b", "No X. No Y. Just Z.", "EN", "AIM-02", "Retórica publicitária de IA"),
    
    # Participle closings (Superficial insight)
    (r",\s*(underscoring|highlighting|reflecting|marking)\s+the\s+(importance|need|shift|significance)\b", "Particípio pendurado", "EN", "AIM-05", "Fecho genérico de IA: explicite a implicação teórica ou prática concreta"),
    (r",\s*(destacando|evidenciando|ressaltando|sublinhando)\s+a\s+(importância|necessidade|relevância)\b", "Particípio pendurado", "PT", "AIM-05", "Fecho genérico de IA: explicite a implicação teórica ou prática concreta"),
]

TIER_3_PATTERNS = [
    # Context-dependent words (Excess in LLMs)
    (r"\brobust(ly)?\b", "robust", "EN", "AIM-01", "Palavra hiper-utilizada por LLMs: use sound, reliable ou justifique estatisticamente"),
    (r"\bcomprehensive\b", "comprehensive", "EN", "AIM-01", "Verifique se a análise é realmente exaustiva"),
    (r"\bfoster(s|ing|ed)?\b", "foster", "EN", "AIM-01", "Use promote, encourage, produce"),
    (r"\bleverag(e|es|ed|ing)\b", "leverage", "EN", "AIM-01", "Use apply, utilize, employ"),
    (r"\bseamless(ly)?\b", "seamless", "EN", "AIM-01", "Adjetivo hiperbólico: descreva como a integração ocorre sem adjetivar"),
    (r"\brobusto(s)?\b", "robusto", "PT", "AIM-01", "Verifique se há justificativa metodológica para chamar de robusto"),
    (r"\bfomento\b", "fomento", "PT", "AIM-01", "Use incentivo, promoção, apoio"),
    (r"\balavancar\b", "alavancar", "PT", "AIM-01", "Jargão corporativo/IA: use impulsionar, potencializar ou ampliar"),
]


class AIMarkerChecker:
    def __init__(self):
        self.parser = MarkdownParser()

    def _strip_ignored_blocks(self, content: str) -> List[Tuple[int, str]]:
        """
        Retorna linhas limpas (número da linha 1-indexed e texto visível),
        ignorando blocos de código fenced, fórmulas matemáticas e comentários.
        """
        lines = content.splitlines()
        cleaned_lines = []
        in_code_block = False
        in_math_block = False

        for idx, line in enumerate(lines, start=1):
            stripped = line.strip()
            # Fenced code block toggle
            if stripped.startswith("```") or stripped.startswith("~~~"):
                in_code_block = not in_code_block
                continue
            if in_code_block:
                continue

            # Display math block toggle
            if stripped.startswith("$$"):
                in_math_block = not in_math_block
                continue
            if in_math_block:
                continue

            # Skip HTML comments
            if stripped.startswith("<!--") and stripped.endswith("-->"):
                continue

            # Strip inline math $...$
            clean_line = re.sub(r"\$[^$]+\$", " ", line)
            # Strip markdown links [text](url) -> text
            clean_line = re.sub(r"\[([^\]]+)\]\([^\)]+\)", r"\1", clean_line)
            # Strip LaTeX citations \cite{...}
            clean_line = re.sub(r"\\cite[a-z]*\{[^}]+\}", " ", clean_line)
            # Strip inline code `code`
            clean_line = re.sub(r"`[^`]+`", " ", clean_line)

            cleaned_lines.append((idx, clean_line))

        return cleaned_lines

    def check_text(self, content: str, filename: str = "") -> Dict[str, Any]:
        cleaned_lines = self._strip_ignored_blocks(content)
        findings = []

        all_rules = [
            (TIER_1_PATTERNS, "CRITICAL", "Tier 1 (Alto Marcador de IA)"),
            (TIER_2_PATTERNS, "WARNING", "Tier 2 (Falso Contraste / Estrutura)"),
            (TIER_3_PATTERNS, "ADVISORY", "Tier 3 (Contextual / Estilo)"),
        ]

        for line_num, line_text in cleaned_lines:
            if not line_text.strip():
                continue

            for patterns, severity, tier_desc in all_rules:
                for regex_pattern, marker_name, lang, issue_code, suggestion in patterns:
                    matches = list(re.finditer(regex_pattern, line_text, re.IGNORECASE))
                    for m in matches:
                        matched_str = m.group(0)
                        start_col = m.start() + 1
                        
                        # Extrair snippet de contexto (±40 caracteres)
                        snip_start = max(0, m.start() - 30)
                        snip_end = min(len(line_text), m.end() + 30)
                        snippet = line_text[snip_start:snip_end].strip()

                        findings.append({
                            "file": filename,
                            "line": line_num,
                            "column": start_col,
                            "issue_code": issue_code,
                            "severity": severity,
                            "tier": tier_desc,
                            "marker": marker_name,
                            "matched_text": matched_str,
                            "snippet": f"...{snippet}...",
                            "suggestion": suggestion,
                            "language": lang
                        })

        summary = {
            "total_markers": len(findings),
            "tier1_count": sum(1 for f in findings if "Tier 1" in f["tier"]),
            "tier2_count": sum(1 for f in findings if "Tier 2" in f["tier"]),
            "tier3_count": sum(1 for f in findings if "Tier 3" in f["tier"]),
            "findings": findings
        }
        return summary

    def check_file(self, filepath: str) -> Dict[str, Any]:
        if not os.path.exists(filepath):
            return {"error": f"Arquivo não encontrado: {filepath}"}
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
        return self.check_text(content, filename=os.path.basename(filepath))


def main():
    parser = argparse.ArgumentParser(description="Verificador determinístico de marcadores de IA em texto acadêmico.")
    parser.add_argument("path", help="Caminho para o arquivo markdown ou diretório.")
    parser.add_argument("--json", action="store_true", help="Imprimir saída em formato JSON.")
    args = parser.parse_args()

    checker = AIMarkerChecker()
    files_to_check = []

    if os.path.isdir(args.path):
        for root, _, files in os.walk(args.path):
            for file in sorted(files):
                if file.endswith((".md", ".markdown", ".tex")):
                    files_to_check.append(os.path.join(root, file))
    else:
        files_to_check.append(args.path)

    all_results = {}
    total_markers = 0

    for fpath in files_to_check:
        res = checker.check_file(fpath)
        all_results[fpath] = res
        if "total_markers" in res:
            total_markers += res["total_markers"]

    if args.json:
        print(json.dumps(all_results, indent=2, ensure_ascii=False))
    else:
        print(f"=== Auditoria de Marcadores de IA ({len(files_to_check)} arquivos analisados) ===")
        print(f"Total de marcadores encontrados: {total_markers}\n")
        for fpath, res in all_results.items():
            if "error" in res:
                print(f"[{fpath}] ERRO: {res['error']}")
                continue
            if res["total_markers"] == 0:
                print(f"✅ {os.path.basename(fpath)}: Nenhum marcador detectado.")
                continue
            print(f"⚠️  {os.path.basename(fpath)}: {res['total_markers']} marcadores (T1: {res['tier1_count']}, T2: {res['tier2_count']}, T3: {res['tier3_count']})")
            for f in res["findings"]:
                print(f"   L{f['line']}: [{f['issue_code']}] [{f['severity']}] '{f['matched_text']}' -> {f['suggestion']}")


if __name__ == "__main__":
    main()
