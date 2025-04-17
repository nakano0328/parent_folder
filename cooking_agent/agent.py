from google.adk.agents import Agent

def suggest_recipe(ingredients: str) -> dict:
    """材料からレシピを提案します。

    Args:
        ingredients (str): カンマ区切りの材料リスト

    Returns:
        dict: ステータスとレシピの提案結果
    """
    # 入力を検証
    if not ingredients or ingredients.strip() == "":
        return {
            "status": "error",
            "error_message": "材料を入力してください。"
        }
    
    # 簡単なレシピの例（実際の実装ではデータベースやLLMを使うことが多い）
    ingredient_list = [i.strip().lower() for i in ingredients.split(",")]
    
    # 基本的な料理パターンの例
    if "卵" in ingredient_list and "ご飯" in ingredient_list:
        return {
            "status": "success",
            "recipe": {
                "name": "オムライス",
                "ingredients": "卵、ご飯、玉ねぎ、ケチャップ、塩、胡椒、バター",
                "instructions": [
                    "1. 玉ねぎをみじん切りにし、バターで炒める",
                    "2. ご飯を加えて炒め、ケチャップで味付けする",
                    "3. 卵を溶いて、塩胡椒で味付けする",
                    "4. フライパンで薄焼き卵を作り、ケチャップライスを包む"
                ]
            }
        }
    elif "豚肉" in ingredient_list and "キャベツ" in ingredient_list:
        return {
            "status": "success",
            "recipe": {
                "name": "豚キャベツ炒め",
                "ingredients": "豚肉、キャベツ、塩、胡椒、醤油、ごま油",
                "instructions": [
                    "1. 豚肉を一口大に切る",
                    "2. キャベツを食べやすい大きさに切る",
                    "3. フライパンで豚肉を炒め、火が通ったらキャベツを加える",
                    "4. 塩、胡椒、醤油で味付けし、最後にごま油を回しかける"
                ]
            }
        }
    else:
        # 汎用的なレシピ提案
        return {
            "status": "success",
            "recipe": {
                "name": f"{', '.join(ingredient_list[:3])}を使った簡単料理",
                "ingredients": ingredients,
                "instructions": [
                    "1. 材料を食べやすい大きさに切る",
                    "2. フライパンで炒め合わせる",
                    "3. 塩、胡椒で味を調える",
                    "4. お好みで醤油やケチャップなどを加える"
                ]
            }
        }

def get_seasonal_ingredients(season: str) -> dict:
    """季節の食材を提案します。

    Args:
        season (str): 季節（春、夏、秋、冬）

    Returns:
        dict: ステータスと季節の食材リスト
    """
    seasons = {
        "春": ["アスパラガス", "新玉ねぎ", "菜の花", "たけのこ", "いちご"],
        "夏": ["トマト", "なす", "きゅうり", "とうもろこし", "すいか"],
        "秋": ["さつまいも", "きのこ", "さんま", "栗", "かぼちゃ"],
        "冬": ["白菜", "大根", "ほうれん草", "みかん", "牡蠣"]
    }
    
    if season in seasons:
        return {
            "status": "success",
            "ingredients": seasons[season]
        }
    else:
        return {
            "status": "error",
            "error_message": f"'{season}' は有効な季節ではありません。春、夏、秋、冬のいずれかを指定してください。"
        }

root_agent = Agent(
    name="recipe_suggestion_agent",
    model="gemini-1.5-flash",
    description=(
        "ユーザーが提供した材料から料理のレシピを提案するエージェント。"
    ),
    instruction=(
        "あなたは料理のプロフェッショナルです。ユーザーが提供した材料からおいしい料理のレシピを提案してください。"
        "また、季節の食材についての質問にも答えることができます。"
    ),
    tools=[suggest_recipe, get_seasonal_ingredients],
)