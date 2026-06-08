from __future__ import annotations

import re
import zipfile
from collections import Counter
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from typing import Any
from xml.etree import ElementTree as ET


BASE_DIR = Path(__file__).resolve().parent
QUIZ_PATH = BASE_DIR / "quiz_options.xlsx"
WORKS_PATH = BASE_DIR / "works.xlsx"

SPREADSHEET_NS = {
    "a": "http://schemas.openxmlformats.org/spreadsheetml/2006/main",
    "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
}
TAG_FIELDS = ("情绪标签", "风格标签", "主题标签", "观看人格标签")
QUESTION_WEIGHTS = {
    "Q1": 1.5,
    "Q2": 1.2,
    "Q3": 1.5,
    "Q4": 1.0,
    "Q5": 1.2,
    "Q6": 1.1,
    "Q7": 1.3,
    "Q8": 1.0,
    "Q9": 1.2,
    "Q10": 1.4,
}
QUESTION_ORDER = ["Q1", "Q2", "Q3", "Q4", "Q5", "Q6", "Q7", "Q8", "Q9", "Q10"]
QUESTION_ORDER_RANK = {
    question_id: index for index, question_id in enumerate(QUESTION_ORDER)
}
FIELD_WEIGHTS = {
    "情绪标签": 2.0,
    "风格标签": 2.4,
    "主题标签": 2.2,
    "观看人格标签": 2.8,
}
DIFFICULTY_LEVELS = {"入门": 0, "中级": 1, "高级": 2}
DIFFICULTY_BONUS = {0: 4.0, 1: 1.5, 2: -3.0}
TAG_NORMALIZATION = {
    "人物关系": "人物",
    "关系": "人物",
    "历史感": "历史",
    "生命力": "生命",
    "开放结局": "实验",
    "开放解释": "实验",
    "时间感": "时间",
}
AnswerValue = str | list[str]


@dataclass(frozen=True)
class QuizOption:
    question_id: str
    question_text: str
    option_id: str
    option_text: str
    tags: tuple[str, ...]


@dataclass(frozen=True)
class QuizQuestion:
    question_id: str
    question_text: str
    options: tuple[QuizOption, ...]


@dataclass(frozen=True)
class Work:
    row: dict[str, str]
    tags_by_field: dict[str, set[str]]

    @property
    def work_id(self) -> str:
        return self.row["作品ID"]

    @property
    def title(self) -> str:
        return self.row["作品名"]

    @property
    def difficulty(self) -> str:
        return self.row["观看难度"]

    @property
    def is_chinese(self) -> bool:
        region = self.row.get("地区", "")
        work_type = self.row.get("类型", "")
        style_tags = self.tags_by_field["风格标签"]
        chinese_markers = {
            "中国舞",
            "中国古典舞",
            "民间舞",
            "山东秧歌",
            "东北秧歌",
            "花鼓灯转化",
            "闽南非遗",
            "塔吉克族舞蹈",
        }
        return "中国" in region or "中国台湾" in region or any(
            marker in style_tags or marker in work_type for marker in chinese_markers
        )


def col_to_index(cell_ref: str) -> int:
    letters = "".join(ch for ch in cell_ref if ch.isalpha())
    index = 0
    for char in letters:
        index = index * 26 + (ord(char.upper()) - 64)
    return max(index - 1, 0)


def load_shared_strings(workbook: zipfile.ZipFile) -> list[str]:
    if "xl/sharedStrings.xml" not in workbook.namelist():
        return []

    root = ET.fromstring(workbook.read("xl/sharedStrings.xml"))
    strings: list[str] = []
    for string_item in root.findall("a:si", SPREADSHEET_NS):
        parts = [node.text or "" for node in string_item.findall(".//a:t", SPREADSHEET_NS)]
        strings.append("".join(parts))
    return strings


def first_sheet_path(workbook: zipfile.ZipFile) -> str:
    workbook_root = ET.fromstring(workbook.read("xl/workbook.xml"))
    first_sheet = workbook_root.find("a:sheets/a:sheet", SPREADSHEET_NS)
    if first_sheet is None:
        raise ValueError("Workbook does not contain any sheets.")

    rel_id = first_sheet.attrib[
        "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id"
    ]
    relationships = ET.fromstring(workbook.read("xl/_rels/workbook.xml.rels"))
    for relation in relationships:
        if relation.attrib.get("Id") == rel_id:
            return f"xl/{relation.attrib['Target']}"
    raise ValueError("Could not resolve the first sheet path.")


def read_cell_value(cell: ET.Element, shared_strings: list[str]) -> str:
    value_node = cell.find("a:v", SPREADSHEET_NS)
    cell_type = cell.attrib.get("t")

    if cell_type == "inlineStr":
        return "".join(
            node.text or "" for node in cell.findall(".//a:t", SPREADSHEET_NS)
        ).strip()
    if value_node is None or value_node.text is None:
        return ""
    if cell_type == "s":
        return shared_strings[int(value_node.text)].strip()
    return value_node.text.strip()


def load_xlsx_rows(path: Path) -> list[dict[str, str]]:
    with zipfile.ZipFile(path) as workbook:
        shared_strings = load_shared_strings(workbook)
        sheet_path = first_sheet_path(workbook)
        root = ET.fromstring(workbook.read(sheet_path))
        raw_rows: list[list[str]] = []
        for row in root.findall(".//a:sheetData/a:row", SPREADSHEET_NS):
            values_by_index: dict[int, str] = {}
            for cell in row.findall("a:c", SPREADSHEET_NS):
                ref = cell.attrib.get("r", "")
                values_by_index[col_to_index(ref)] = read_cell_value(cell, shared_strings)
            max_index = max(values_by_index, default=-1)
            raw_rows.append([values_by_index.get(index, "") for index in range(max_index + 1)])

    if not raw_rows:
        return []

    headers = [str(header).strip() for header in raw_rows[0]]
    parsed_rows: list[dict[str, str]] = []
    for raw_row in raw_rows[1:]:
        row_values = raw_row + [""] * max(0, len(headers) - len(raw_row))
        row = {
            header: str(row_values[index]).strip() if index < len(row_values) else ""
            for index, header in enumerate(headers)
            if header
        }
        if any(value for value in row.values()):
            parsed_rows.append(row)
    return parsed_rows


def split_semicolon_values(text: str) -> list[str]:
    values: list[str] = []
    for item in re.split(r"[；;]", text or ""):
        normalized = item.strip()
        if normalized and normalized not in values:
            values.append(normalized)
    return values


def normalize_tag(tag: str) -> str:
    return TAG_NORMALIZATION.get(tag.strip(), tag.strip())


def split_tags(text: str) -> list[str]:
    tags: list[str] = []
    for raw_tag in split_semicolon_values(text):
        tag = normalize_tag(raw_tag)
        if tag and tag not in tags:
            tags.append(tag)
    return tags


def question_sort_key(question_id: str) -> int:
    return QUESTION_ORDER_RANK.get(question_id, 999)


@lru_cache(maxsize=1)
def load_quiz_questions() -> tuple[QuizQuestion, ...]:
    grouped: dict[str, dict[str, Any]] = {}
    for row in load_xlsx_rows(QUIZ_PATH):
        question_id = row["问题ID"]
        group = grouped.setdefault(
            question_id,
            {"question_text": row["问题"], "options": []},
        )
        group["options"].append(
            QuizOption(
                question_id=question_id,
                question_text=row["问题"],
                option_id=row["选项ID"],
                option_text=row["选项内容"],
                tags=tuple(split_tags(row["映射标签"])),
            )
        )

    questions = []
    for question_id in sorted(grouped, key=question_sort_key):
        group = grouped[question_id]
        questions.append(
            QuizQuestion(
                question_id=question_id,
                question_text=group["question_text"],
                options=tuple(group["options"]),
            )
        )
    return tuple(questions)


@lru_cache(maxsize=1)
def load_works() -> tuple[Work, ...]:
    works: list[Work] = []
    for row in load_xlsx_rows(WORKS_PATH):
        works.append(
            Work(
                row=row,
                tags_by_field={
                    field: set(split_tags(row.get(field, ""))) for field in TAG_FIELDS
                },
            )
        )
    return tuple(works)


@lru_cache(maxsize=1)
def question_lookup() -> dict[str, QuizQuestion]:
    return {question.question_id: question for question in load_quiz_questions()}


@lru_cache(maxsize=1)
def option_lookup() -> dict[str, QuizOption]:
    options: dict[str, QuizOption] = {}
    for question in load_quiz_questions():
        for option in question.options:
            options[option.option_id] = option
    return options


@lru_cache(maxsize=1)
def work_lookup() -> dict[str, Work]:
    return {work.work_id: work for work in load_works()}


def selected_option_ids(answer_value: AnswerValue | None) -> list[str]:
    if answer_value is None:
        return []
    if isinstance(answer_value, str):
        return [answer_value] if answer_value else []

    selected: list[str] = []
    for option_id in answer_value:
        if option_id and option_id not in selected:
            selected.append(option_id)
    return selected


def build_profile(answer_option_ids: dict[str, AnswerValue]) -> list[dict[str, Any]]:
    option_map = option_lookup()
    weighted_tags: Counter[str] = Counter()
    for question_id, answer_value in answer_option_ids.items():
        if question_id == "Q4":
            continue
        option_ids = selected_option_ids(answer_value)
        if not option_ids:
            continue
        weight = QUESTION_WEIGHTS.get(question_id, 1.0) / len(option_ids)
        for option_id in option_ids:
            option = option_map.get(option_id)
            if not option:
                continue
            for tag in option.tags:
                weighted_tags[tag] += weight

    profile = []
    for tag, score in weighted_tags.most_common(8):
        profile.append({"tag": tag, "score": round(score, 1)})
    return profile


def difficulty_alignment(selected_difficulty: str, work_difficulty: str) -> tuple[float, str]:
    selected_level = DIFFICULTY_LEVELS.get(selected_difficulty)
    work_level = DIFFICULTY_LEVELS.get(work_difficulty)
    if selected_level is None or work_level is None:
        return 0.0, ""

    gap = abs(selected_level - work_level)
    score = DIFFICULTY_BONUS[gap]
    if gap == 0:
        return score, "难度刚好合适"
    if gap == 1:
        return score, "难度接近你的预期"
    return score, "这部作品会比你此刻想要的更有挑战"


def cultural_bonus(selected_option_id: str, work: Work) -> tuple[float, str]:
    if selected_option_id == "Q7_A":
        return (4.0, "中国题材偏好") if work.is_chinese else (-2.5, "")
    if selected_option_id == "Q7_B":
        return (4.0, "外国题材偏好") if not work.is_chinese else (-2.5, "")
    return 0.0, ""


def polish_option_text(text: str) -> str:
    return re.sub(r"\s+", "、", (text or "").strip())


def choice_clause_from_hit(hit: dict[str, Any]) -> str:
    question_id = hit["question_id"]
    option_text = polish_option_text(hit["option_text"])

    if question_id == "Q1":
        return f"想找一部能让你{option_text}的作品"
    if question_id == "Q2":
        return f"偏爱{option_text}的表达"
    if question_id == "Q3":
        return option_text if option_text.startswith("想") else f"现在更接近{option_text}的情绪"
    if question_id == "Q5":
        return f"也容易被{option_text}的舞蹈吸引"
    if question_id == "Q7":
        return f"此刻更想看{option_text}"
    if question_id == "Q8":
        culture_text = option_text.split("：", 1)[-1]
        return f"如果看中国题材，会更容易被{culture_text}这样的文化气质吸引"
    if question_id == "Q9":
        return f"题材上更想先进入{option_text}"
    if question_id == "Q10":
        return f"也最容易被{option_text}打动"
    return ""


def join_choice_clauses(clauses: list[str]) -> str:
    normalized = [clause.lstrip("也") for clause in clauses if clause]
    if not normalized:
        return ""
    if len(normalized) == 1:
        return normalized[0]
    if len(normalized) == 2:
        return f"{normalized[0]}，也{normalized[1]}"
    return f"{normalized[0]}，也{normalized[1]}，同时{normalized[2]}"


def adapt_reason_text(reason_text: str) -> str:
    cleaned = (reason_text or "").strip().rstrip("。")
    if not cleaned:
        return ""
    if cleaned.startswith("适合"):
        cleaned = cleaned.removeprefix("适合")
        cleaned = cleaned.replace("的观众", "的你")
        cleaned = cleaned.replace("观众", "你")
        return f"它尤其适合{cleaned}。"
    return f"它{cleaned}。"


def adapt_difficulty_note(difficulty_note: str) -> str:
    if difficulty_note == "难度刚好合适":
        return "观看门槛也会比较友好，你可以很自然地走进去。"
    if difficulty_note == "难度接近你的预期":
        return "观看门槛和你现在想投入的状态也比较贴近。"
    if difficulty_note:
        return "如果你愿意多给它一点耐心，这部作品也会慢慢把力量递出来。"
    return ""


def explain_recommendation(
    work: Work,
    top_tags: list[str],
    strongest_hits: list[dict[str, Any]],
    difficulty_note: str,
) -> str:
    _ = top_tags
    clauses: list[str] = []
    used_question_ids: set[str] = set()
    for hit in strongest_hits:
        if hit["question_id"] in {"Q4", "Q6"} or hit["question_id"] in used_question_ids:
            continue
        clause = choice_clause_from_hit(hit)
        if not clause:
            continue
        clauses.append(clause)
        used_question_ids.add(hit["question_id"])
        if len(clauses) == 3:
            break

    intro = join_choice_clauses(clauses)
    if intro:
        first_sentence = f"如果你这次{intro}，下面推荐的这部作品会比较适合你。"
    else:
        first_sentence = "下面推荐的这部作品，会比较贴近你这次的观看状态。"

    reason_sentence = adapt_reason_text(work.row.get("为什么推荐", ""))
    difficulty_sentence = adapt_difficulty_note(difficulty_note)

    return " ".join(
        sentence for sentence in [first_sentence, reason_sentence, difficulty_sentence] if sentence
    ).strip()


def recommend(answer_option_ids: dict[str, AnswerValue], top_n: int = 3) -> dict[str, Any]:
    questions = question_lookup()
    options = option_lookup()
    works = load_works()
    selected_difficulty = ""
    if "Q4" in answer_option_ids:
        difficulty_ids = selected_option_ids(answer_option_ids["Q4"])
        difficulty_option = options.get(difficulty_ids[0]) if difficulty_ids else None
        if difficulty_option:
            selected_difficulty = difficulty_option.option_text

    results: list[dict[str, Any]] = []
    for work in works:
        total_score = 0.0
        matched_scores: Counter[str] = Counter()
        matched_tags: set[str] = set()
        question_hits: list[dict[str, Any]] = []

        for question_id, answer_value in answer_option_ids.items():
            if question_id == "Q4":
                continue
            option_ids = selected_option_ids(answer_value)
            if not option_ids:
                continue

            question_weight = QUESTION_WEIGHTS.get(question_id, 1.0) / len(option_ids)

            for option_id in option_ids:
                option = options.get(option_id)
                if not option:
                    continue

                per_question_score = 0.0
                per_question_tags: set[str] = set()

                for field_name, field_weight in FIELD_WEIGHTS.items():
                    hits = set(option.tags) & work.tags_by_field[field_name]
                    if not hits:
                        continue
                    field_score = len(hits) * question_weight * field_weight
                    per_question_score += field_score
                    per_question_tags.update(hits)
                    share = field_score / len(hits)
                    for tag in hits:
                        matched_scores[tag] += share
                        matched_tags.add(tag)

                if question_id == "Q7":
                    extra_score, extra_label = cultural_bonus(option_id, work)
                    per_question_score += extra_score
                    if extra_label:
                        matched_scores[extra_label] += max(extra_score, 0)
                        per_question_tags.add(extra_label)

                if per_question_score > 0:
                    question_hits.append(
                        {
                            "question_id": question_id,
                            "question_text": questions[question_id].question_text,
                            "option_text": option.option_text,
                            "score": round(per_question_score, 2),
                            "tags": sorted(per_question_tags),
                        }
                    )
                total_score += per_question_score

        difficulty_score, difficulty_note = difficulty_alignment(
            selected_difficulty,
            work.difficulty,
        )
        total_score += difficulty_score

        related_titles: list[str] = []
        for related_id in split_semicolon_values(work.row.get("相似作品ID", "")):
            if related_id == work.work_id:
                continue
            related_work = work_lookup().get(related_id)
            if related_work:
                related_titles.append(related_work.title)

        strongest_hits = sorted(
            question_hits,
            key=lambda item: item["score"],
            reverse=True,
        )
        top_tags = [tag for tag, _ in matched_scores.most_common(5)]
        results.append(
            {
                "work": work,
                "score": round(total_score, 2),
                "difficulty_note": difficulty_note,
                "matched_tags": top_tags,
                "matched_tag_count": len(matched_tags),
                "question_hits": strongest_hits,
                "summary": explain_recommendation(
                    work,
                    top_tags=top_tags,
                    strongest_hits=strongest_hits,
                    difficulty_note=difficulty_note,
                ),
                "related_titles": related_titles[:3],
            }
        )

    results.sort(
        key=lambda item: (
            item["score"],
            item["matched_tag_count"],
            -DIFFICULTY_LEVELS.get(item["work"].difficulty, 0),
        ),
        reverse=True,
    )
    return {
        "results": results[:top_n],
        "all_results": results,
        "profile": build_profile(answer_option_ids),
    }
