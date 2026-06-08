# MBTI Dance

一个基于 Streamlit 的舞蹈作品推荐小站。

## 本地运行

1. 安装依赖

```bash
pip install -r requirements.txt
```

2. 启动项目

```bash
streamlit run app.py
```

## 项目文件

- `app.py`：页面与交互
- `recommender.py`：问卷读取与推荐逻辑
- `quiz_options.xlsx`：问卷题目与选项
- `works.xlsx`：作品库
- `assets/`：页面背景图片

## 部署到公开网站

推荐使用 GitHub + Streamlit Community Cloud：

1. 将整个项目上传到 GitHub 公开仓库
2. 登录 <https://share.streamlit.io/>
3. 选择你的 GitHub 仓库
4. 将 `Main file path` 设为 `app.py`
5. 点击 `Deploy`

部署成功后会生成一个公开访问链接。
