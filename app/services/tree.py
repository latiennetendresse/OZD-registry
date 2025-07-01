from typing import Dict, List

from app.models.activity import Activity


class ActivityTreeService:
    """
    Сервис для работы с иерархией видов деятельности.
    Позволяет собирать всех потомков узла на заданную глубину.
    """

    def __init__(self, activities: List[Activity]):
        # Создаём маппинг id -> объект для быстрого доступа
        self._activities: Dict[int, Activity] = {
            act.id: act for act in activities
        }

    def gather_descendant_ids(
        self,
        root_id: int,
        max_level: int = 3
    ) -> List[int]:
        """
        Собрать ID всех узлов дерева, лежащих внутри узла с root_id,
        до глубины max_level (включительно).
        """

        result: List[int] = []

        def _dfs(current_id: int, level: int):
            if level > max_level or current_id not in self._activities:
                return
            result.append(current_id)
            for child in self._activities[current_id].children:
                _dfs(child.id, level + 1)

        _dfs(root_id, 1)
        return result
