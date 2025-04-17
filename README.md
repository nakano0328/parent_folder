# Cooking Agent

ユーザーが提供した材料に基づいて料理のレシピを提案したり、季節に応じた旬の食材を提案したりする Python エージェントです。

## 概要

このプロジェクトは、`google-adk` ライブラリを使用して構築された料理提案エージェントを提供します。主な機能は以下の2つです。

1.  **レシピ提案:** ユーザーが入力した材料（カンマ区切り）に基づいて、簡単なレシピを提案します。
2.  **季節の食材提案:** 指定された季節（春、夏、秋、冬）に応じた旬の食材リストを提案します。

エージェントは `gemini-1.5-flash` モデルを利用するように設定されています。

## 機能

*   **`suggest_recipe(ingredients: str) -> dict`**:
    *   カンマ区切りの材料文字列を受け取り、レシピ（料理名、材料、手順）を含む辞書を返します。
    *   入力が空の場合はエラーメッセージを返します。
    *   特定の材料の組み合わせ（例: 卵とご飯、豚肉とキャベツ）に対しては定義済みのレシピを返します。
    *   それ以外の場合は、入力された材料を使った汎用的なレシピを生成します。
*   **`get_seasonal_ingredients(season: str) -> dict`**:
    *   季節名（"春", "夏", "秋", "冬"）を受け取り、その季節の旬の食材リストを含む辞書を返します。
    *   無効な季節名が入力された場合はエラーメッセージを返します。

## 前提条件

*   Python 3.x
*   `google-adk` ライブラリ

## インストール

1.  **リポジトリをクローンします（もしリポジトリがある場合）:**
    ```bash
    git clone https://github.com/your_username/cooking_agent.git
    cd cooking_agent
    ```
    リポジトリがない場合は、プロジェクトディレクトリを作成してください。

2.  **仮想環境を作成して有効化します:**
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    # Windows の場合: .venv\Scripts\activate
    ```

3.  **必要なライブラリをインストールします:**
    ```bash
    pip install google-adk
    ```
    (もし `requirements.txt` があれば `pip install -r requirements.txt` を使用)

4.  **.env ファイルを作成します:**
    プロジェクトのルートディレクトリに `.env` ファイルを作成し、以下のいずれかの形式で必要な情報を入力します。

    *   **Vertex AI を使用しない場合:**
        ```properties
        GOOGLE_GENAI_USE_VERTEXAI=FALSE
        GOOGLE_API_KEY=your-api-key
        ```
        `your-api-key` には、Google Cloud Platform で取得した API キーを設定してください。

    *   **Vertex AI を使用する場合:**
        ```properties
        GOOGLE_GENAI_USE_VERTEXAI=TRUE
        GOOGLE_CLOUD_PROJECT=your-project
        GOOGLE_CLOUD_LOCATION=your-location
        ```
        `your-project` には Google Cloud プロジェクト ID、`your-location` にはリージョン（例: `asia-northeast1`）を設定してください。

## 使い方

### エージェントとして利用する

`agent.py` 内で定義されている `root_agent` をインポートして利用できます。

```python
# filepath: /Users/nakanomitsuki/HIBARI/parent_folder/main.py
from cooking_agent.agent import root_agent

# 例: 材料からレシピを提案させる
# ユーザーからの入力をシミュレート
user_input_ingredients = "卵, ご飯"
# エージェントに処理を依頼 (実際のADKの実行方法に合わせてください)
# response = root_agent.execute(f"材料「{user_input_ingredients}」でレシピを教えて")
# print(response)

# 例: 季節の食材を尋ねる
# ユーザーからの入力をシミュレート
user_input_season = "秋"
# エージェントに処理を依頼 (実際のADKの実行方法に合わせてください)
# response = root_agent.execute(f"{user_input_season}の旬の食材は？")
# print(response)

# 注意: 上記の root_agent.execute の部分は、google-adk の
#       具体的なエージェント実行方法に応じて調整が必要です。
```

### 関数を直接利用する

個別の機能を直接呼び出すことも可能です。

```python
# filepath: /Users/nakanomitsuki/HIBARI/parent_folder/example.py
from cooking_agent.agent import suggest_recipe, get_seasonal_ingredients

# レシピ提案
recipe_result = suggest_recipe("豚肉, キャベツ, ピーマン")
if recipe_result["status"] == "success":
    print("提案レシピ:")
    print(f"  料理名: {recipe_result['recipe']['name']}")
    print(f"  材料: {recipe_result['recipe']['ingredients']}")
    print("  手順:")
    for step in recipe_result['recipe']['instructions']:
        print(f"    {step}")
else:
    print(f"エラー: {recipe_result['error_message']}")

print("-" * 20)

# 季節の食材提案
seasonal_result = get_seasonal_ingredients("冬")
if seasonal_result["status"] == "success":
    print("冬の旬の食材:")
    for ingredient in seasonal_result["ingredients"]:
        print(f"  - {ingredient}")
else:
    print(f"エラー: {seasonal_result['error_message']}")

# エラーケース
invalid_season_result = get_seasonal_ingredients("梅雨")
if invalid_season_result["status"] == "error":
    print(f"エラー: {invalid_season_result['error_message']}")

```

## エージェント設定 (`root_agent`)

`agent.py` で定義されている `root_agent` の設定は以下の通りです。

*   **`name`**: `recipe_suggestion_agent`
*   **`model`**: `gemini-1.5-flash`
*   **`description`**: ユーザーが提供した材料から料理のレシピを提案するエージェント。
*   **`instruction`**: あなたは料理のプロフェッショナルです。ユーザーが提供した材料からおいしい料理のレシピを提案してください。また、季節の食材についての質問にも答えることができます。
*   **`tools`**:
    *   `suggest_recipe`
    *   `get_seasonal_ingredients`
