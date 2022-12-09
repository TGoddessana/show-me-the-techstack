from io import BytesIO
from flask import Blueprint, render_template, request
import requests
from bs4 import BeautifulSoup
import re
import matplotlib.pyplot as plt
import base64


bp = Blueprint("main", __name__, url_prefix="/")


@bp.route("/")
def index():
    return render_template("index.html")


@bp.route("/subject/")
def get_lagnuage_ratio_by_word():
    # 검색어
    subject = request.args.get("search")
    if not subject:
        return "잘못된 접근입니다."

    # Github 언어 그래프 그리기
    url = f"https://github.com/search?q={subject}"
    soup = BeautifulSoup(requests.get(url).text, "html.parser")
    tech_stacks_information_list = soup.find_all("a", {"class": "filter-item"})
    tech_list = []
    count_list = []
    for tech_stack in tech_stacks_information_list:
        tech_stack_name = " ".join(
            re.findall(
                "[a-zA-Z]+",
                tech_stack.get_text().replace("\n", "").replace(" ", ""),
            )
        )
        count = int(
            (tech_stack.find("span", class_="count").getText()).replace(
                ",", ""
            )
        )
        tech_list.append(tech_stack_name)
        count_list.append(count)
    plt.rc("font", size=10)
    plt.figure(figsize=(10, 10))
    plt.pie(
        count_list,
        labels=tech_list,
        autopct="%.1f%%",
    )
    buf = BytesIO()
    plt.savefig(buf, format="png", transparent=True)
    buf.seek(0)
    buf.flush()
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    language_graph = f"<img src='data:image/png;base64,{data}'/>"

    # 가장 유명한 Repository
    url = f"https://github.com/search?o=desc&q={subject}&s=stars&type=Repositories"
    soup = BeautifulSoup(requests.get(url).text, "html.parser")
    repo_list = soup.find_all(
        "ul",
        {"class": "repo-list"},
    )

    return render_template(
        "domain_search_result.html",
        language_graph=language_graph,
        tech_list=tech_list,
        query=subject,
        repo_list=repo_list,
    )
